import requests

def get_lat_lon(address, api_key):
    """
    Function to get latitude and longitude from a given address.
    Uses the Google Maps Geocoding API.
    """
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            print("Address not found.")
            return None, None
    else:
        print(f"Error: {response.status_code} - {response.reason}")
        return None, None

def main():
    """
    Main function to prompt user for input and call the geocoding function.
    """
    print("Welcome to the Pool Cost Calculator!")
    address = input("Enter your pool's address: ")
    api_key = input("Enter your Google Maps API key: ")

    lat, lon = get_lat_lon(address, api_key)

    if lat is not None and lon is not None:
        print(f"Latitude: {lat}, Longitude: {lon}")
    else:
        print("Could not retrieve location. Please check the address or API key.")

if __name__ == "__main__":
    main()
