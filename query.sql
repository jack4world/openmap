SELECT 
  o.ogc_fid as office_id, 
  COALESCE(o.name, 'Unnamed Office ' || o."@id") as office_name,
  COUNT(c.ogc_fid) as starbucks_count
FROM 
  pois o
JOIN 
  pois c
ON 
  ST_Contains(ST_Buffer(o.wkb_geometry::geography, 1000)::geometry, c.wkb_geometry)
WHERE 
  o.building = 'office' 
  AND c.amenity = 'cafe'
GROUP BY 
  o.ogc_fid, o.name, o."@id"
HAVING 
  COUNT(c.ogc_fid) > 5
ORDER BY 
  starbucks_count DESC;
