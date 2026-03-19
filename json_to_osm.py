import json

def convert_to_osm():
    with open('xuhui_roads.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    elements = data.get('elements', [])
    
    with open('xuhui_roads.osm', 'w', encoding='utf-8') as out:
        out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        out.write('<osm version="0.6" generator="python_script">\n')
        
        for elem in elements:
            if elem['type'] == 'node':
                out.write(f'  <node id="{elem["id"]}" lat="{elem["lat"]}" lon="{elem["lon"]}"/>\n')
            elif elem['type'] == 'way':
                out.write(f'  <way id="{elem["id"]}">\n')
                for nid in elem.get('nodes', []):
                    out.write(f'    <nd ref="{nid}"/>\n')
                for k, v in elem.get('tags', {}).items():
                    k_clean = str(k).replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;').replace('&', '&amp;')
                    v_clean = str(v).replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;').replace('&', '&amp;')
                    out.write(f'    <tag k="{k_clean}" v="{v_clean}"/>\n')
                out.write('  </way>\n')
                
        out.write('</osm>\n')
    print("Successfully converted xuhui_roads.json to xuhui_roads.osm")

if __name__ == '__main__':
    convert_to_osm()
