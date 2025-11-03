###############################################################
#  Webex ISS Tracker & SpaceX Launch Info Bot
#  ------------------------------------------------------------
# This program:
# - Asks the user to enter an access token or use the hard coded access token.
# - Lists the user's Webex rooms.
# - Asks the user which Webex room to monitor for "/seconds" of requests.
# - Monitors the selected Webex Team room every second for "/seconds" messages.
# - Discovers GPS coordinates of the ISS flyover using ISS API.
# - Display the geographical location using geolocation API based on the GPS coordinates.
# - Formats and sends the results back to the Webex Team room.
# - Displays the next SpaceX launch details.
# - Includes full error handling, modularity, and readability.
###############################################################

import requests
import json
import time
from iso3166 import countries


# -----------------
# Functions
# -----------------

def get_webex_rooms(access_token):
    """Retrieve and return a list of Webex rooms."""
    try:
        response = requests.get(
            "https://webexapis.com/v1/rooms",
            headers={"Authorization": access_token},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        return data.get("items", [])
    except requests.exceptions.RequestException as e:
        print("Error fetching Webex rooms:", e)
        return []


def get_latest_message(room_id, access_token):
    # Retrieve the most recent message in a Webex room.
    try:
        params = {"roomId": room_id, "max": 1}
        r = requests.get("https://webexapis.com/v1/messages",
                         params=params,
                         headers={"Authorization": access_token},
                         timeout=10)
        r.raise_for_status()
        json_data = r.json()
        items = json_data.get("items", [])
        if items:
            return items[0].get("text", "")
        return None
    except requests.exceptions.RequestException as e:
        print("Error fetching messages:", e)
        return None


def get_iss_location():
    # Fetch current ISS location and return lat, lng, timestamp.
    try:
        r = requests.get("http://api.open-notify.org/iss-now.json", timeout=10)
        r.raise_for_status()
        data = r.json()
        lat = data["iss_position"]["latitude"]
        lng = data["iss_position"]["longitude"]
        timestamp = data["timestamp"]
        return lat, lng, timestamp
    except (requests.exceptions.RequestException, KeyError) as e:
        print("Error fetching ISS data:", e)
        return None, None, None


def get_geocode(lat, lng, api_key):
    # Use OpenWeather reverse geocoding API to get location info.
    try:
        r = requests.get(
            "http://api.openweathermap.org/geo/1.0/reverse",
            params={"lat": lat, "lon": lng, "limit": 1, "appid": api_key},
            timeout=10
        )
        r.raise_for_status()
        data = r.json()
        if len(data) == 0:
            return {"country": "XZ", "state": "Unknown", "name": "Unknown"}
        return data[0]
    except requests.exceptions.RequestException as e:
        print("Error with Geolocation API:", e)
        return {"country": "XZ", "state": "Unknown", "name": "Unknown"}


def post_to_webex(room_id, access_token, message):
    # Send a message to a Webex room.
    try:
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }
        post_data = {"roomId": room_id, "text": message}
        r = requests.post("https://webexapis.com/v1/messages",
                          data=json.dumps(post_data),
                          headers=headers,
                          timeout=10)
        if r.status_code == 200:
            print("Message successfully sent to Webex room.")
        else:
            print(f" Error posting to Webex: {r.status_code} - {r.text}")
    except requests.exceptions.RequestException as e:
        print("Error sending message to Webex:", e)


def get_spacex_next_launch():
    # Fetch and return details about the next SpaceX launch.
    try:
        # Get next launch data
        r = requests.get("https://api.spacexdata.com/v4/launches/next", timeout=10)
        r.raise_for_status()
        launch_data = r.json()

        mission_name = launch_data.get("name", "Unknown Mission")
        date_utc = launch_data.get("date_utc", "Unknown Date")

        # Get rocket details
        rocket_id = launch_data.get("rocket")
        rocket_name = "Unknown Rocket"
        if rocket_id:
            r_rocket = requests.get(f"https://api.spacexdata.com/v4/rockets/{rocket_id}", timeout=10)
            if r_rocket.status_code == 200:
                rocket_name = r_rocket.json().get("name", "Unknown Rocket")

        # Get launchpad details
        pad_id = launch_data.get("launchpad")
        launchpad_name = "Unknown Launchpad"
        if pad_id:
            r_pad = requests.get(f"https://api.spacexdata.com/v4/launchpads/{pad_id}", timeout=10)
            if r_pad.status_code == 200:
                pad_data = r_pad.json()
                launchpad_name = pad_data.get("name", "Unknown Launchpad")
                location = pad_data.get("locality", "Unknown Location")
            else:
                location = "Unknown"
        else:
            location = "Unknown"

        message = (f"*Next SpaceX Launch Info*\n\n"
                   f"Mission: {mission_name}\n"
                   f"Rocket: {rocket_name}\n"
                   f"Launch Date (UTC): {date_utc}\n"
                   f"Launchpad: {launchpad_name}, {location}")

        return message
    except requests.exceptions.RequestException as e:
        print("Error fetching SpaceX data:", e)
        return "Error retrieving SpaceX launch information."


# ------------------
# Main Program
# ------------------

def main():

    # Access Token
    choice = input("Do you wish to use the hard-coded Webex token? (y/n) ")
    if choice.lower() == "n":
        access_token = "Bearer " + input("Enter your Webex Access Token: ")
    else:
        access_token = "Bearer MzZhOWYyZGYtNjllYy00OTYzLWFlOTAtMGQxNWNmMjA0NjA2NWIzZjFkY2YtZDJl_PE93_d68b3fe9-4c07-4dad-8882-3b3fd6afb92d"

    # Get Rooms
    rooms = get_webex_rooms(access_token)
    if not rooms:
        print("No rooms available.")
        return

    print("\nList of available rooms:")
    for room in rooms:
        print(f"- {room.get('title', 'Untitled')}")

    # Choose Room
    room_id = None
    while not room_id:
        room_name = input("\nWhich room should be monitored? ")
        for r in rooms:
            if room_name.lower() in r["title"].lower():
                room_id = r["id"]
                print("Monitoring room:", r["title"])
                break
        if not room_id:
            print("Room not found. Try again.")

    geo_key = "37d0569718539a79bbe689e6249a8791"

    print("\nBot is now monitoring the room for commands (/seconds or /spacex)...\n")

    # Bot Loop
    while True:
        time.sleep(2)
        message = get_latest_message(room_id, access_token)
        if not message:
            continue

        print(f"Most recent message: {message}")

        # /seconds Command
        if message.startswith("/"):
            if message.startswith("/spacex"):
                spacex_info = get_spacex_next_launch()
                post_to_webex(room_id, access_token, spacex_info)

            elif message[1:].isdigit():
                seconds = int(message[1:])
                if seconds > 5:
                    seconds = 5
                time.sleep(seconds)

                lat, lng, timestamp = get_iss_location()
                if not lat or not lng:
                    continue
                time_string = time.ctime(timestamp)
                geo = get_geocode(lat, lng, geo_key)

                country = geo.get("country", "XZ").upper()
                state = geo.get("state", "Unknown")
                city = geo.get("name", "Unknown")

                if country != "XZ":
                    try:
                        country = countries.get(country).name
                    except Exception:
                        pass

                if country == "XZ":
                    msg = f"On {time_string}, the ISS was flying over a body of water at latitude {lat}° and longitude {lng}°."
                else:
                    msg = f"On {time_string}, the ISS was flying over {city}, {state}, {country} ({lat}°, {lng}°)."

                post_to_webex(room_id, access_token, msg)

        time.sleep(3)



# Main
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBot stopped by user.")
