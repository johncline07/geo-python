import requests, csv

URL = "https://services7.arcgis.com/xuAg12SDp2ow0Fb8/arcgis/rest/services/UpdatedPub150/FeatureServer/0/query"

def get_count(url):
    params = {
        "where": "1=1",
        "returnCountOnly": "true",
        "f": "json"
    }
    response = requests.get(url, params=params, timeout=30)
    if response.status_code == 200:
        data = response.json()
        return data.get("count", 0)
    else:
        print(f"Error fetching count: {response.status_code}")
        return 0

def get_page(url, offset, page_size):
    params = {
        "where": "1=1",
        "outFields": "*",
        "resultOffset": offset,
        "resultRecordCount": page_size,
        "f": "geojson"
    }
    response = requests.get(url, params=params, timeout=30)
    if response.status_code == 200:
        data = response.json()
        return data.get("features", [])
    else:
        print(f"Error fetching page: {response.status_code}")
        return []


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

def main():
    total = get_count(URL)
    print(f"Total Features: {total}")

    features = get_page(URL, 0, 5)
    print(f"Fetched {len(features)} features")

    if features:
        first = features[0]["properties"].keys()
        print(f"Feature keys: {list(first)}")

    rows = [flatten(feature) for feature in features]
    write_csv(rows, "ports_sample.csv")


if __name__ == "__main__":
    main()
    
