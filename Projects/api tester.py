import requests

def get_weather_data(lat, lon):
    """
    Fetch weather data from the National Weather Service API using latitude and longitude.
    """
    url = f"https://api.weather.gov/points/{lat},{lon}"
    headers = {"User-Agent": "PoolCostCalculator/1.0 (your_email@example.com)"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        forecast_url = data['properties']['forecast']
        forecast_response = requests.get(forecast_url, headers=headers)

        if forecast_response.status_code == 200:
            forecast_data = forecast_response.json()
            return forecast_data  # Return full forecast data
        else:
            print(f"Error fetching forecast data: {forecast_response.status_code}")
            return None
    else:
        print(f"Error fetching points data: {response.status_code}")
        return None


def get_lat_lon(address, api_key):
    """
    Use the Google Maps API to convert an address into latitude and longitude.
    """
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get('results'):
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            print("No results returned for the address.")
            return None, None
    else:
        print(f"Error with Google Maps API: {response.status_code}")
        return None, None


def calculate_heating_cost(volume, current_temp, desired_temp, energy_cost):
    """
    Calculate the cost to heat a pool to the desired temperature.
    """
    temperature_change = desired_temp - current_temp
    # Energy required in kWh (specific heat of water: 4.18 J/g°C, 1 kWh = 3600 kJ)
    energy_needed_kwh = (volume * 1000) * temperature_change * 4.18 / 3600
    # Cost calculation
    total_cost = energy_needed_kwh * energy_cost
    return energy_needed_kwh, total_cost


def main():
    """
    Main function to get user input, calculate heating cost, and fetch weather data.
    """
    print("Welcome to the Pool Cost Calculator!")
    address = input("Enter your pool's address: ")
    api_key = input("Enter your Google Maps API key: ")

    # Step 1: Get latitude and longitude
    lat, lon = get_lat_lon(address, api_key)

    if lat is not None and lon is not None:
        print(f"Latitude: {lat}, Longitude: {lon}")
        user_input = input ("Would you like to use the metric system or Imperial?")
    if user_input ==("Imperial"):
        # Step 2: Prompt for pool details
        print("\nEnter your pool dimensions and temperature details:")
        length = float(input("Length (in Feet): "))
        width = float(input("Width (in Feet): "))
        depth = float(input("Depth (in Feet): "))
        current_temp = float(input("Current pool temperature (°F): "))
        desired_temp = float(input("Desired pool temperature (°F): "))
        energy_cost = float(input("Energy cost per kWh (in your currency): "))
    if user_input == ("Metric"):
        print("\nEnter your pool dimensions and temperature details:")
        length = float(input("Length (in meters): "))
        width = float(input("Width (in meters): "))
        depth = float(input("Depth (in meters): "))
        current_temp = float(input("Current pool temperature (°C): "))
        desired_temp = float(input("Desired pool temperature (°C): "))
        energy_cost = float(input("Energy cost per kWh (in your currency): "))

        # Step 3: Calculate pool volume and heating cost
        volume = length * width * depth  # Volume in cubic meters
        energy_needed, total_cost = calculate_heating_cost(volume, current_temp, desired_temp, energy_cost)

        # Step 4: Display results
        print(f"\nPool Volume: {volume:.2f} cubic meters")
        print(f"Energy Needed: {energy_needed:.2f} kWh")
        print(f"Estimated Heating Cost: {total_cost:.2f} (currency)")

        # Optional: Fetch and display weather forecast
        forecast_data = get_weather_data(lat, lon)
        if forecast_data:
            periods = forecast_data['properties']['periods']
            print("\n7-Day Weather Forecast:")
            for period in periods[:7]:  # Limit to 7 days
                print(f"{period['name']}: {period['detailedForecast']}")
    else:
        print("Could not retrieve location. Please check the address or API key.")


if __name__ == "__main__":
    main()
