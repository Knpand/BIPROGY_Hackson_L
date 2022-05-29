import requests
token = "アプリのTOKENを入力"
endpoint = "https://notify-api.line.me/api/notify"
headers = {"Authorization": "Bearer " + token}
params = {"message": "test message"}
requests.post(endpoint, headers=headers, data=params)
