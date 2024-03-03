import requests
import json

API_HOST = "https://solved.ac/api/v3"

def send_api(path, method, body=None):
    
    url = API_HOST + path
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, data=json.dumps(body, ensure_ascii=False, indent="\t"))
        
        json_data = json.loads(response.text)
        print("response status %r" % response.status_code)
        print_json("response text ", json_data)
        
        return response.status_code, json_data
    except Exception as ex:
        print(ex)
  
  
def get_problem_stats(path, user, method):
    query = "?handle=" + user
    path = path + query
    
    return send_api(path, method)

def print_json(prompt, json_data):
    print(prompt + json.dumps(json_data, indent=3, ensure_ascii=False))
    



    
    
    
response_code, json_data = get_problem_stats("/user/problem_stats", "jwt2719", "GET")



