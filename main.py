###############################################################
#  This program:
# - Asks the user to enter an access token or use the hard coded access token.
# - Lists the user's Webex rooms.
# - Asks the user which Webex room to monitor for "/seconds" of requests.
# - Monitors the selected Webex Team room every second for "/seconds" messages.
# - Discovers GPS coordinates of the ISS flyover using ISS API.
# - Display the geographical location using geolocation API based on the GPS coordinates.
# - Formats and sends the results back to the Webex Team room.



# 1. Import libraries for API requests, JSON formatting, epoch time conversion, and iso3166.

import requests
import json
import time
from iso3166 import countries


# 2. Complete the if statement to ask the user for the Webex access token.
choice = input("Do you wish to use the hard-coded Webex token? (y/n) ")

#<!!!REPLACEME with if statements to ask user for the Webex Access Token!!!>
if choice.lower() == "n":
    accessToken = "Bearer " + input("Enter your Webex Access Token: ")
else:
    accessToken = "Bearer MzE4ZjdjNmUtMGVhMy00NTIyLWEzNTMtMDljYjM5MjU5Nzc2MmYwODcyYWMtOWMy_PE93_d68b3fe9-4c07-4dad-8882-3b3fd6afb92d"


# 3. Provide the URL to the Webex room API.
r = requests.get(
    "https://webexapis.com/v1/rooms",
    headers={"Authorization": accessToken}
    )


#######################################################################################
# DO NOT EDIT ANY BLOCKS WITH r.status_code
if not r.status_code == 200:
    raise Exception("Incorrect reply from Webex API. Status code: {}. Text: {}".format(r.status_code, r.text))
#######################################################################################

# 4. Create a loop to print the type and title of each room.
print("\nList of available rooms:")
rooms = r.json()["items"]
for room in rooms:
    print(f"Room Type: {room['type']} — Room Title: {room['title']}")

#######################################################################################
# SEARCH FOR WEBEX ROOM TO MONITOR
#  - Searches for user-supplied room name.
#  - If found, print "found" message, else prints error.
#  - Stores values for later use by bot.
# DO NOT EDIT CODE IN THIS BLOCK
#######################################################################################

while True:
    roomNameToSearch = input("Which room should be monitored for the /seconds messages? ")
    roomIdToGetMessages = None
    
    for room in rooms:
        if(room["title"].find(roomNameToSearch) != -1):
            print ("Found rooms with the word " + roomNameToSearch)
            print(room["title"])
            roomIdToGetMessages = room["id"]
            roomTitleToGetMessages = room["title"]
            print("Found room: " + roomTitleToGetMessages)
            break

    if(roomIdToGetMessages == None):
        print("Sorry, I didn't find any room with " + roomNameToSearch + " in it.")
        print("Please try again...")
    else:
        break    
######################################################################################
# WEBEX BOT CODE
#  Starts Webex bot to listen for and respond to /seconds messages.
######################################################################################

while True:
    time.sleep(1)
    GetParameters = {
                            "roomId": roomIdToGetMessages,
                            "max": 1
                    }
# 5. Provide the URL to the Webex messages API.    
    r = requests.get("https://webexapis.com/v1/messages", 
                         params = GetParameters, 
                         headers = {"Authorization": accessToken}
                    )
    # verify if the retuned HTTP status code is 200/OK
    if not r.status_code ==  200:
        raise Exception( "Incorrect reply from Webex API. Status code: {}. Text: {}".format(r.status_code, r.text))

    json_data = r.json()
    if len(json_data["items"]) == 0:
        print("No messages found yet.")
        continue  
    
    messages = json_data["items"]
    message = messages[0]["text"]
    print(f"Most recent message: {message}") 
    
    if message.find("/") == 0:    
        if (message[1:].isdigit()):
            seconds = int(message[1:])  
        else:
            print("Error: Message after '/' must be a number.")
            continue
    
    #for the sake of testing, the max number of seconds is set to 5.
        if seconds > 5:
            seconds = 5    
            
        time.sleep(seconds)     
    
# 6. Provide the URL to the ISS Current Location API.         
        r = requests.get("http://api.open-notify.org/iss-now.json")
        
        json_data = r.json()
        
        if not r.status_code == 200:
            print("Error retrieving ISS data.")
            continue

# 7. Record the ISS GPS coordinates and timestamp.

        lat = json_data["iss_position"]["latitude"]
        lng = json_data["iss_position"]["longitude"]
        timestamp = json_data["timestamp"]

# 8. Convert the timestamp epoch value to a human readable date and time.
        # Use the time.ctime function to convert the timestamp to a human readable date and time.
        timeString = time.ctime(timestamp)      
   
# 9. Provide your Geoloaction API consumer key.
    
        geo_key = "37d0569718539a79bbe689e6249a8791"
    
        mapsAPIGetParameters = { 
                "lat": lat,
                "lon": lng,
                "format": "json",
                "apiKey": geo_key
                }

# 10. Use OpenWeather Reverse Geocoding API instead of OpenCage
        r = requests.get("http://api.openweathermap.org/geo/1.0/reverse",
                 params={
                     "lat": lat,
                     "lon": lng,
                     "limit": 1,
                     "appid": geo_key
                     })

        if not r.status_code == 200:
            print("Error: Geolocation API request failed.")
            continue

        json_data = r.json()

        if len(json_data) == 0:
            print("Error: No geolocation data found.")
            continue

# 11. Store the location received from the API
        location = json_data[0]
        CountryResult = location.get("country", "XZ").upper()
        StateResult = location.get("state", "Unknown")
        CityResult = location.get("name", "Unknown")
        StreetResult = "Unknown"  # OpenWeather doesn't return street-level data

# Convert ISO country code to full name
        if CountryResult != "XZ":
            CountryResult = countries.get(CountryResult).name


# 12. Complete the code to format the response message.
#     Example responseMessage result: In Austin, Texas the ISS will fly over on Thu Jun 18 18:42:36 2020 for 242 seconds.

        if CountryResult == "XZ":
            responseMessage = "On {}, the ISS was flying over a body of water at latitude {}° and longitude {}°.".format(timeString, lat, lng)
        else:
            responseMessage = "On {}, the ISS was flying over the following location: \n{} \n{}, {} \n{}\n({}°, {}°)".format(timeString, StreetResult, CityResult, StateResult, CountryResult, lat, lng)
        
#<!!!REPLACEME with if statements to compose the message to display the current ISS location in the Webex Team room!!!>
        if CountryResult == "XZ":
            responseMessage = "On {}, the ISS was flying over a body of water at latitude {}° and longitude {}°.".format(timeString, lat, lng)
        elif StreetResult != "Unknown":
            responseMessage = "On {}, the ISS was flying over the following location: \n{} \n{}, {} \n{}\n({}°, {}°)".format(timeString, StreetResult, CityResult, StateResult, CountryResult, lat, lng)
        elif CityResult != "Unknown":
            responseMessage = "On {}, the ISS was flying over the following location: \n{}, {} \n{}\n({}°, {}°)".format(timeString, CityResult, StateResult, CountryResult, lat, lng)
        elif StateResult != "Unknown":
            responseMessage = "On {}, the ISS was flying over the following location: \n{} \n{}\n({}°, {}°)".format(timeString, StateResult, CountryResult, lat, lng)
        else:
            responseMessage = "On {}, the ISS was flying over the following country: {}\n({}°, {}°)".format(timeString, CountryResult, lat, lng)

        # print the response message
        print("Sending to Webex: " + responseMessage)

# 13. Complete the code to post the message to the Webex room.         
        # the Webex HTTP headers, including the Authoriztion and Content-Type
        HTTPHeaders = { 
            "Authorization": accessToken,
            "Content-Type": "application/json"
            }
        
        PostData = {
            "roomId": roomIdToGetMessages,
            "text": responseMessage
            }

        # Post the call to the Webex message API.
        r = requests.post("https://webexapis.com/v1/messages", 
                          data=json.dumps(PostData), 
                          headers=HTTPHeaders)
        
        #<!!!REPLACEME with code for error handling in case request not successfull>
        if not r.status_code == 200:
            print("Error posting message to Webex. Status code:", r.status_code)
        else:
            print("Message successfully sent to Webex room.")