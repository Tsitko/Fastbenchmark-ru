import requests
import json

# change this if your service started not at localhost
host = 'http://localhost'
# change this if your server started not at 8000 port
port = 8000

service_url = str(host) + ':' + str(port) + '/'

# here should be the json with data for prediction
data = {
%data_part%
}

params = json.dumps({"predict": {"data": str(json.dumps(data))}})
responce = requests.get(service_url, data=params)
result = json.loads(responce.json())
if result['state'] == 'error':
    print('wrong data format:\n')
    print(result['error_log'])
else:
    prediction = result['prediction']['prediction']
    probability = result['prediction']['probability']
    print('prediction = ' + str(prediction) + '\t with probability = ' + str(probability))