import urllib.request
import urllib.parse
import json
import time

overpass_url = "http://overpass-api.de/api/interpreter"

# query for Xuhui District, Shanghai
# amenity=cafe and (Starbucks or 星巴克)
# building=office
overpass_query = """
[out:json][timeout:180];
area["name"="徐汇区"]->.searchArea;
(
  node["building"="office"](area.searchArea);
  way["building"="office"](area.searchArea);
  relation["building"="office"](area.searchArea);
  
  node["amenity"="cafe"]["name"~"Starbucks|星巴克",i](area.searchArea);
  way["amenity"="cafe"]["name"~"Starbucks|星巴克",i](area.searchArea);
  relation["amenity"="cafe"]["name"~"Starbucks|星巴克",i](area.searchArea);
);
out body;
>;
out skel qt;
"""

print("Fetching data from Overpass API for Xuhui District...")
start_time = time.time()
data = urllib.parse.urlencode({'data': overpass_query}).encode('utf-8')
req = urllib.request.Request(overpass_url, data=data)

try:
    with urllib.request.urlopen(req) as response:
        elapsed = time.time() - start_time
        if response.status == 200:
            result = json.loads(response.read().decode('utf-8'))
            output_file = "xuhui_data.json"
            
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
                
            elements = result.get('elements', [])
            offices = [e for e in elements if e.get('tags', {}).get('building') == 'office']
            cafes = [e for e in elements if e.get('tags', {}).get('amenity') == 'cafe']
            
            print(f"Successfully saved data to {output_file} in {elapsed:.2f} seconds.")
            print(f"Total elements retrieved: {len(elements)}")
            print(f"Offices found: {len(offices)}")
            print(f"Starbucks/Cafes found: {len(cafes)}")
        else:
            print(f"Error HTTP {response.status}")
except urllib.error.HTTPError as e:
    print(f"HTTPError: {e.code} - {e.reason}")
    print(e.read().decode('utf-8')[:500])
except Exception as e:
    print(f"Request failed: {e}")
