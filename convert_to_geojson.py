import json
import os

def overpass_to_geojson(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    elements = data.get('elements', [])
    
    # Extract nodes and ways for reference
    nodes = {}
    ways = {}
    
    for elem in elements:
        if elem['type'] == 'node':
            nodes[elem['id']] = (elem['lon'], elem['lat'])
        elif elem['type'] == 'way':
            ways[elem['id']] = elem
            
    features = []
    
    # Convert elements with tags into GeoJSON features
    for elem in elements:
        tags = elem.get('tags', {})
        if not tags:
            continue
            
        geom = None
        properties = {**tags, "@id": f"{elem['type']}/{elem['id']}"}
        
        try:
            if elem['type'] == 'node':
                geom = {"type": "Point", "coordinates": [elem['lon'], elem['lat']]}
                
            elif elem['type'] == 'way':
                coords = []
                for nid in elem.get('nodes', []):
                    if nid in nodes:
                        coords.append(nodes[nid])
                        
                if coords:
                    if coords[0] == coords[-1] and len(coords) >= 4:
                        geom = {"type": "Polygon", "coordinates": [coords]}
                    else:
                        geom = {"type": "LineString", "coordinates": coords}
                        
            elif elem['type'] == 'relation':
                # Basic MultiPolygon support for relations
                if tags.get('type') == 'multipolygon':
                    polygons = []
                    for member in elem.get('members', []):
                        if member['type'] == 'way' and member['role'] == 'outer':
                            wid = member['ref']
                            if wid in ways:
                                w = ways[wid]
                                coords = []
                                for nid in w.get('nodes', []):
                                    if nid in nodes:
                                        coords.append(nodes[nid])
                                        
                                if coords and coords[0] == coords[-1] and len(coords) >= 4:
                                    polygons.append([coords])
                    if polygons:
                        geom = {"type": "MultiPolygon", "coordinates": polygons}
        except Exception as e:
            print(f"Error processing {elem['type']}/{elem['id']}: {e}")
            
        if geom:
            features.append({
                "type": "Feature",
                "properties": properties,
                "geometry": geom
            })
            
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully converted {len(features)} features to GeoJSON.")
    print(f"Saved to: {output_path}")

if __name__ == "__main__":
    input_file = '/Users/jackworld/.gemini/antigravity/scratch/overpass_data/xuhui_data.json'
    output_file = '/Users/jackworld/.gemini/antigravity/scratch/overpass_data/xuhui_data.geojson'
    
    overpass_to_geojson(input_file, output_file)
