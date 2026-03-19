-- Step 1: Add pgrouting_node column and find nearest nodes for offices and cafes
ALTER TABLE pois ADD COLUMN IF NOT EXISTS pgrouting_node bigint;

-- Snap ONLY if hasn't been snapped yet to avoid redundant work
UPDATE pois p
SET pgrouting_node = (
  SELECT v.id 
  FROM ways_vertices_pgr v
  ORDER BY p.wkb_geometry <-> v.geom 
  LIMIT 1
)
WHERE (p.building = 'office' OR p.amenity = 'cafe') AND p.pgrouting_node IS NULL;

-- Step 2: Use pgRouting to find walking distances <= 1000m
WITH 
offices AS (
  SELECT ogc_fid as office_id, name as office_name, pgrouting_node as source_node
  FROM pois 
  WHERE building = 'office'
),
cafes AS (
  SELECT ogc_fid as cafe_id, pgrouting_node as target_node
  FROM pois 
  WHERE amenity = 'cafe'
),
costs AS (
  SELECT start_vid, end_vid, agg_cost 
  FROM pgr_dijkstraCost(
    'SELECT id, source, target, length_m as cost, length_m as reverse_cost FROM ways',
    (SELECT array_agg(DISTINCT source_node) FROM offices),
    (SELECT array_agg(DISTINCT target_node) FROM cafes),
    directed := false
  )
)
SELECT 
  o.office_id,
  COALESCE(o.office_name, 'Unnamed Office ' || o.office_id) as office_name,
  COUNT(DISTINCT c.cafe_id) as starbucks_count
FROM 
  offices o
JOIN 
  costs ON o.source_node = costs.start_vid
JOIN 
  cafes c ON c.target_node = costs.end_vid
WHERE 
  costs.agg_cost <= 1000 
  AND costs.agg_cost >= 0
GROUP BY 
  o.office_id, o.office_name
HAVING 
  COUNT(DISTINCT c.cafe_id) > 5
ORDER BY 
  starbucks_count DESC;

