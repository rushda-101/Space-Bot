# Space-Bot

# 🚀 Space Bot API Investigation Sheet
**Total Marks: 30**
**Part 1: Collect Required API Documentation**
This investigation sheet helps you gather key technical information from the three
APIs required for the Space Bot project: **Webex Messaging API**, **ISS Current
Location API**, and a **Geocoding API** (LocationIQ or Mapbox or other), plus the
Python time module.
---
## Section 1: Webex Messaging API (7 marks)✅
| Criteria | Details |
|---------|---------|
| API Base URL | `https://webexapis.com/v1/` |
| Authentication Method | `Bot Access Token (Bearer Token in HTTP header)` |
| Endpoint to list rooms | `/rooms` |
| Endpoint to get messages | `/messages?roomId={roomId}` |
| Endpoint to send message | `/messages` |
| Required headers | `Authorization: Bearer {ACCESS_TOKEN} Content-Type: application/json` |
| Sample full GET or POST request | `POST https://webexapis.com/v1/messages Body: ```json{	"roomId": "Y2lzY29zcGFyazovL3VzL1JPT00v123456789",	"text": "Hello from SpaceBot!"	}` |
---
## Section 2: ISS Current Location API (3 marks)
| Criteria | Details |
|---------|---------|
| API Base URL | `http://api.open-notify.org/` |
| Endpoint for current ISS location | `/iss-now.json` |
| Sample response format (example JSON) |
```
{
"timestamp": 1713105632,
"iss_position": {
"latitude": "47.6062",
"longitude": "-122.3321"
},
"message": "success"
}
```
|
---
## Section 3: Geocoding API (LocationIQ or Mapbox or other) (6 marks)
| Criteria | Details |
|---------|---------|
| Provider used (circle one) | `Mapbox` |
| API Base URL | `https://api.mapbox.com/geocoding/v5/` |
| Endpoint for reverse geocoding | `/mapbox.places/{longitude},{latitude}.json` |
| Authentication method | `Access Token (`access_token=YOUR_MAPBOX_TOKEN` |
| Required query parameters | `longitude`, `latitude`, `access_token` |
| Sample request with latitude/longitude | `https://api.mapbox.com/geocoding/v5/mapbox.places/100.75,1.5.json?access_token=YOUR_MAPBOX_TOKEN` |
| Sample JSON response (formatted example) |
```
{
"type": "FeatureCollection",
"query": [100.75, 1.5],
"features": [
{
"place_name": "Singapore, Republic of Singapore"
}
]
}
```
|
---
## 🚀 Section 4: Epoch to Human Time Conversion (Python time module) (2 marks)
| Criteria | Details |
|---------|---------|
| Library used | `time` |
| Function used to convert epoch | `time.strftime()` and `time.localtime()` |
| Sample code to convert timestamp |
```
import time
timestamp = 1713105632
readable_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
print(readable_time)
```
|
| Output (human-readable time) | `2024-04-14 06:40:32` |
---
## 🚀 Section 5: Web Architecture & MVC Design Pattern (12 marks)
### 🚀 Web Architecture – Client-Server Model
- **Client**:
- **Server**:
- (Explain the communication between them & include a block diagram )
### 🚀 RESTful API Usage
-
-
-
### 🚀 MVC Pattern in Space Bot
| Component | Description |
|------------|-------------|
| **Model** | Handles data – retrieves and stores ISS and geocoding data. |
| **View** | The Webex chat output. The user sees formatted messages. |
| **Controller** | The main Python logic that connects APIs and decides what message to send back. |
#### Example:
- Model: ISS API + Geocoding API calls
- View: “The ISS is currently over Singapore at 2024-04-14 06:40:32.”
- Controller: Receives Webex message “Where is the ISS?”, triggers API calls, and formats the reply.
---
### 🚀 Notes
- Use official documentation for accuracy (e.g. developer.webex.com, locationiq.com
or Mapbox, open-notify.org or other ISS API).
- Be prepared to explain your findings to your instructor or demo how you retrieved
them using tools like Postman, Curl, or Python scripts.
---
### Total: /30
