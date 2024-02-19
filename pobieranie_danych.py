import config
import requests

response = requests.get("https://api.um.warszawa.pl/api/action/busestrams_get/?resource_id=%20f2e5503e-927d-4ad3-9500-4ab9e55deb59&apikey="+config.apiKey+"&type=1")

J=response.json()

print(response)

print(len(J['result']))
for line in J['result']:
    print(line)
