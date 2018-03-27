import requests
import json

# TODO: replace with your own app_id and app_key
app_id = 'e94904db'
app_key = '25a83eec3bcd55a917ea1cd654a8696b'

language = 'en'
word_id = 'Ace'

url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word_id.lower()

r = requests.get(url, headers={'app_id': app_id, 'app_key': app_key})
print(r.json()['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0])

print("code {}\n".format(r.status_code))
print("text \n" + r.text)
print("json \n" + json.dumps(r.json()))
