from typing import Optional 
import json 
import requests 
import fastapi 

app = fastapi.FastAPI()

test_url = "http://timeseriesdb:9000/exec"
test_sql = "SELECT * FROM users;"

@app.get("/")
def read_root():
    query_params = {
        'query': test_sql,
        'fmt': 'json'
    }
    res = requests.post(test_url, params = query_params)
    print(res.status_code)
    json_res = json.loads(res.content)
    return json_res 