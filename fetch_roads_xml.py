import urllib.request
import urllib.parse
import time

overpass_url = "http://overpass-api.de/api/interpreter"

overpass_query = """
[out:xml][timeout:180][bbox:31.09,121.38,31.23,121.47];
(
  way["highway"]["highway"!~"motorway|motorway_link|trunk|trunk_link"];
);
(._;>;);
out body;
"""

print("Fetching OSM XML road networks from Overpass API...")
start_time = time.time()
data = urllib.parse.urlencode({'data': overpass_query}).encode('utf-8')
req = urllib.request.Request(overpass_url, data=data)

try:
    with urllib.request.urlopen(req) as response:
        elapsed = time.time() - start_time
        if response.status == 200:
            result = response.read().decode('utf-8')
            output_file = "xuhui_roads.osm"
            
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(result)
                
            print(f"Successfully saved OSM XML to {output_file} in {elapsed:.2f} seconds.")
        else:
            print(f"Error HTTP {response.status}")
except Exception as e:
    print(f"Request failed: {e}")
