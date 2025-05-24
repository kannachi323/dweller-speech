import uvicorn
import json

from server import app




with open("../config.json", "r") as f:
    data = json.load(f)
    config = data['stt-server']

    url = config['url']

    host = url['address']
    port = url['port']

if __name__ == '__main__':
    uvicorn.run(app, host=host, port=port)