import requests
token = "G2LNN3ApusueIRgPpvo3Urw1mXlVah7BoqA3RR3Dl8T"
endpoint = "https://notify-api.line.me/api/notify"
headers = {"Authorization": "Bearer " + token}
params = {"message": "test message"}
requests.post(endpoint, headers=headers, data=params)