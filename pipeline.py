from xml.sax.handler import all_features

import requests, csv

URL = "https://services7.arcgis.com/xuAg12SDp2ow0Fb8/arcgis/rest/services/UpdatedPub150/FeatureServer/0/query"

def fetch_json(url, params):
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    if "error" in data:
        raise RuntimeError(data)
    return data


def get_count(url):
    params = {
        "where": "1=1",
        "returnCountOnly": "true",
        "f": "json",
        }
    data = fetch_json(url, params)
    return data["count"]


def get_page(url, offset, page_size):
    params = {
        "where": "1=1",
        "outFields": "*",
        "resultOffset": offset,
        "resultRecordCount": page_size,
        "f": "geojson",
        }
    data = fetch_json(url, params)
    return data["features"]


def flatten(feature):
    properties = feature.get("properties", {})
    geometry = feature.get("geometry") or {}
    coords = geometry.get("coordinates")
    if coords:
        lon, lat = coords[0], coords[1]
    else:
        lon, lat = None, None
    
    flattened = {**properties, "lon": lon, "lat": lat}
    return flattened

   
def write_csv(rows, path):
    FIELDS = ["Main_Port_Name", "Country_Code", "Harbor_Size", "Harbor_Type", "lon", "lat"]
    if not rows:
        print("No data to write.")
        return

    with open(path, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=FIELDS, extrasaction="ignore")
        dict_writer.writeheader()
        dict_writer.writerows(rows)

def get_all_features(url, page_size=1000):
    offset = 0
    all_features = []
    while True:
        features = get_page(url, offset, page_size)
        if not features:
            break
        all_features.extend(features)
        offset += len(features)
    return all_features


def main():
    total = get_count(URL)
    print(f"Total Features: {total}")

    features = get_all_features(URL)
    print(f"Fetched {len(features)} features")

    if len(features) != total:
        print(f"Warning: expected {total}, got {len(features)}")

    rows = [flatten(feature) for feature in features]
    write_csv(rows, "ports_all.csv")


if __name__ == "__main__":
    main()
    
