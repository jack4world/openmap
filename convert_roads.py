import json

def convert_roads():
    with open('xuhui_roads.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    elements = data.get('elements', [])
    
    nodes = {}
    for elem in elements:
        if elem['type'] == 'node':
            nodes[elem['id']] = (elem['lon'], elem['lat'])
            
    features = []
    
    for elem in elements:
        if elem['type'] == 'way':
            tags = elem.get('tags', {})
            coords = []
            for nid in elem.get('nodes', []):
                if nid in nodes:
                    coords.append(nodes[nid])
            if len(coords) >= 2:
                features.append({
                    "type": "Feature",
                    "properties": {
                        "osm_id": elem['id'],
                        "highway": tags.get('highway', ''),
                        "name": tags.get('name', ''),
                        "oneway": tags.get('oneway', '')
                    },
                    "geometry": {
                        "type": "LineString",
                        "coordinates": coords
                    }
                })
                
    geojson = {"type": "FeatureCollection", "features": features}
    with open('xuhui_roads.geojson', 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)
    print(f"Converted {len(features)} road segments to geojson.")

if __name__ == '__main__':
    convert_roads()
