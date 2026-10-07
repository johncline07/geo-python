import requests

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

def main():
    total = get_count(URL)
    features = get_page(URL, 0, 5)
    print("Total Features: {total}")
    print (f"Fetched {len(features)} features")


if __name__ == "__main__":
    main()
    
