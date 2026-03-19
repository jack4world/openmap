import csv

def generate_map():
    with open('kepler_connections.csv', 'r', encoding='utf-8') as f:
        csv_data = f.read()

    csv_data = csv_data.replace('`', '\\`').replace('$', '\\$')

    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Xuhui District - Office & Starbucks Walking Clusters</title>
  
  <link href="https://api.tiles.mapbox.com/mapbox-gl-js/v1.1.1/mapbox-gl.css" rel="stylesheet">
  
  <script src="https://unpkg.com/react@16.8.4/umd/react.production.min.js"></script>
  <script src="https://unpkg.com/react-dom@16.8.4/umd/react-dom.production.min.js"></script>
  <script src="https://unpkg.com/redux@3.7.2/dist/redux.js"></script>
  <script src="https://unpkg.com/react-redux@5.1.1/dist/react-redux.min.js"></script>
  <script src="https://unpkg.com/styled-components@4.1.3/dist/styled-components.min.js"></script>
  
  <script src="https://api.tiles.mapbox.com/mapbox-gl-js/v1.1.1/mapbox-gl.js"></script>
  <script src="https://unpkg.com/kepler.gl@2.5.5/umd/keplergl.min.js"></script>
  
  <style>
    body {{ margin: 0; padding: 0; overflow: hidden; }}
    #app {{ width: 100vw; height: 100vh; }}
  </style>
</head>
<body>
  <div id="app"></div>
  <script>
    const MAPBOX_TOKEN = 'PROVIDE_YOUR_MAPBOX_TOKEN_HERE';
    const reducers = (function createReducers(redux, keplerGl) {{
      return redux.combineReducers({{
        keplerGl: keplerGl.keplerGlReducer
      }});
    }}(Redux, KeplerGl));
    const store = Redux.createStore(reducers, {{}}, Redux.applyMiddleware(KeplerGl.taskMiddleware));
    
    const csvData = `{csv_data}`;

    const config = {{
      "version": "v1",
      "config": {{
        "visState": {{
          "filters": [],
          "layers": [
            {{
              "id": "arcs",
              "type": "arc",
              "config": {{
                "dataId": "walking_clusters",
                "label": "Walking Connections (Arcs)",
                "color": [137, 218, 178],
                "columns": {{ "lat0": "source_lat", "lng0": "source_lon", "lat1": "target_lat", "lng1": "target_lon" }},
                "isVisible": true,
                "visConfig": {{
                  "opacity": 0.8,
                  "thickness": 3,
                  "colorRange": {{"name": "Global Warming", "type": "sequential", "category": "Uber", "colors": ["#5A1846", "#900C3F", "#C70039", "#E3611C", "#F1920E", "#FFC300"]}},
                  "sizeRange": [0, 10],
                  "targetColor": [255, 153, 31]
                }}
              }},
              "visualChannels": {{
                "colorField": {{"name": "walking_distance_m", "type": "real"}},
                "colorScale": "quantile"
              }}
            }},
            {{
              "id": "offices",
              "type": "point",
              "config": {{
                "dataId": "walking_clusters",
                "label": "Offices",
                "color": [255, 0, 0],
                "columns": {{"lat": "source_lat", "lng": "source_lon"}},
                "isVisible": true,
                "visConfig": {{"radius": 30}}
              }}
            }},
            {{
              "id": "cafes",
              "type": "point",
              "config": {{
                "dataId": "walking_clusters",
                "label": "Starbucks Cafes",
                "color": [0, 200, 0],
                "columns": {{"lat": "target_lat", "lng": "target_lon"}},
                "isVisible": true,
                "visConfig": {{"radius": 15}}
              }}
            }}
          ],
          "interactionConfig": {{
            "tooltip": {{
              "fieldsToShow": {{
                "walking_clusters": [
                  {{"name": "source_office", "format": null}},
                  {{"name": "target_cafe", "format": null}},
                  {{"name": "walking_distance_m", "format": "0.1f"}}
                ]
              }},
              "enabled": true
            }}
          }}
        }},
        "mapState": {{
          "bearing": 0,
          "latitude": 31.19,
          "longitude": 121.43,
          "pitch": 45,
          "zoom": 13
        }},
        "mapStyle": {{
          "styleType": "dark"
        }}
      }}
    }};

    const App = function() {{
      React.useEffect(() => {{
        store.dispatch(
          KeplerGl.addDataToMap({{
            datasets: {{
              info: {{ label: 'Walking Distance Clusters', id: 'walking_clusters' }},
              data: KeplerGl.processCsvData(csvData)
            }},
            option: {{ centerMap: true, readOnly: false }},
            config: config
          }})
        );
      }}, []);
      return React.createElement(
        ReactRedux.Provider,
        {{store}},
        React.createElement(KeplerGl.KeplerGl, {{
          id: "map",
          mapboxApiAccessToken: MAPBOX_TOKEN,
          width: window.innerWidth,
          height: window.innerHeight
        }})
      );
    }};
    ReactDOM.render(React.createElement(App), document.getElementById('app'));
  </script>
</body>
</html>
"""
    with open('kepler_map.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Kepler Map successfully saved to kepler_map.html")

if __name__ == "__main__":
    generate_map()
