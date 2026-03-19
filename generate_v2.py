import pandas as pd
from keplergl import KeplerGl

def create_map():
    # Read CSV
    df = pd.read_csv('kepler_connections.csv')

    # Configure Kepler map
    config = {
      "version": "v1",
      "config": {
        "visState": {
          "layers": [
            {
              "id": "arcs",
              "type": "arc",
              "config": {
                "dataId": "Walking Clusters",
                "label": "Walking Connections",
                "color": [137, 218, 178],
                "columns": {
                  "lat0": "source_lat",
                  "lng0": "source_lon",
                  "lat1": "target_lat",
                  "lng1": "target_lon"
                },
                "isVisible": True,
                "visConfig": {
                  "opacity": 0.8,
                  "thickness": 3,
                  "colorRange": {"name": "Global Warming", "type": "sequential", "category": "Uber", "colors": ["#5A1846", "#900C3F", "#C70039", "#E3611C", "#F1920E", "#FFC300"]},
                  "sizeRange": [0, 10],
                  "targetColor": [255, 153, 31]
                }
              },
              "visualChannels": {
                "colorField": {"name": "walking_distance_m", "type": "real"},
                "colorScale": "quantile"
              }
            },
            {
              "id": "offices",
              "type": "point",
              "config": {
                "dataId": "Walking Clusters",
                "label": "Offices",
                "color": [255, 0, 0],
                "columns": {"lat": "source_lat", "lng": "source_lon"},
                "isVisible": True,
                "visConfig": {"radius": 20}
              }
            },
            {
              "id": "cafes",
              "type": "point",
              "config": {
                "dataId": "Walking Clusters",
                "label": "Starbucks Cafes",
                "color": [0, 200, 0],
                "columns": {"lat": "target_lat", "lng": "target_lon"},
                "isVisible": True,
                "visConfig": {"radius": 10}
              }
            }
          ]
        },
        "mapState": {
          "latitude": 31.19,
          "longitude": 121.43,
          "zoom": 13
        }
      }
    }

    map_1 = KeplerGl(height=800, data={"Walking Clusters": df}, config=config)
    map_1.save_to_html(file_name='kepler_map_v2.html')
    print("Successfully generated kepler_map_v2.html via Python package.")

if __name__ == "__main__":
    create_map()
