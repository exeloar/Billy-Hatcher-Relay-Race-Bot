from obswebsocket import obsws, requests

host = "localhost"
port = 4444
password = ""

ws = obsws(host, port)
ws.connect()

ws.call(requests.CreateScene("CONNECTION TEST SUCCESS"))

print("Check OBS for a new scene to confirm test")