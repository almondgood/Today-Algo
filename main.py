import requests
import json
import datetime


level_dict = { 0:'Unrated',
        1:'Bronze V',
        2:'Bronze IV',
        3:'Bronze III',
        4:'Bronze II',
        5:'Bronze I',
        6:'Silver V',
        7:'Silver IV',
        8:'Silver III',
        9:'Silver II',
        10:'Silver I',
        11:'Gold V',
        12:'Gold IV',
        13:'Gold III',
        14:'Gold II',
        15:'Gold I',
        16:'Platinum V',
        17:'Platinum IV',
        18:'Platinum III',
        19:'Platinum II',
        20:'Platinum I',
        21:'Diamond V',
        22:'Diamond IV',
        23:'Diamond III',
        24:'Diamond II',
        25:'Diamond I',
        26:'Ruby V',
        27:'Ruby IV',
        28:'Ruby III',
        29:'Ruby II',
        30:'Ruby I'}

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
        #print("response status %r" % response.status_code)
        #print_json("response text ", json_data)
        
        return response.status_code, json_data
    except Exception as ex:
        print(ex)
  
  
def get_problem_stats(path, user, method):
    query = "?handle=" + user
    path = path + query
    
    return send_api(path, method)

def print_json(prompt, json_data):
    print(prompt + json.dumps(json_data, indent=3, ensure_ascii=False))
    

def parse(json_data):
    user_data = {}
    for item in json_data:
        level = level_dict[item['level']]
        solved = item['solved']
        user_data[level] = solved
        
    print(user_data)
    return user_data

def validate_user_data(user_data):
    return 1
    
def save_user_file(user, json_data):
    currunt_date = datetime.date.today().strftime("%y%m%d")
    filename = f"{user}-{currunt_date}.txt"    
    user_data = parse(json_data)
    validate_user_data(user_data)

    content = {
        "user": f"{user}",
        "date": f"{currunt_date}",
        "solved": user_data
               }

    try:
        with open(filename, 'w') as file:
            file.write(content)
        print(f"'{filename}' is successfully saved.")
    except Exception as e:
        print(f"Failed to save '{filename}'.")
        print("The cause is {e}.")
        
            
            


response_code, json_data = get_problem_stats("/user/problem_stats", "jwt2719", "GET")

parse(json_data)
