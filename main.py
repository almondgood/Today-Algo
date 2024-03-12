import requests
import json
import datetime
from pathlib import Path
import os

############### api
level_dict = { 
        0:'Unrated',
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
        30:'Ruby I'
    }

API_HOST = "https://solved.ac/api/v3"

def send_api(path, method="GET", body=None):
    
    url = API_HOST + path
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, data=json.dumps(body, ensure_ascii=False, indent="\t"))     
        response.raise_for_status()


        json_data = json.loads(response.text)
        
        return json_data
    except Exception as ex:
        print(ex)
  
  
def send_api_with_query(path, user, method="GET"):
    query = "?handle=" + user
    path = path + query
    
    return send_api(path, method)

def print_json(prompt, json_data):
    print(prompt + json.dumps(json_data, indent=3, ensure_ascii=False))
    

def get_solved(json_data):
    user_data = {}
    for item in json_data:
        level = level_dict[item['level']]
        solved = item['solved']
        user_data[level] = solved
        
    print(user_data)
    return user_data


def validate_user_data(user_data):
    return 1

def get_rating(user):
    json_data = send_api_with_query("/user/show", user)
    return json_data['rating']
    
    
def save_user_file(user, json_data):
    today = datetime.date.today().strftime('%y%m%d')
    filename = f"{user}.json"    
    path = f"data/{today}/{filename}"
    user_data = get_solved(json_data)
    rating = int(get_rating(user))
    
    
    content = {
        "user": f"{user}",
        "date": f"{today}",
        "rating": rating,
        "solved": user_data
               }

    content = json.dumps(content)

    new_directory = Path(f"data/{today}")
    new_directory.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, 'w') as file:
            file.write(content)
        print(f"'{filename}' is successfully saved.")
    except Exception as e:
        print(f"Failed to save '{filename}'.")
        print(f"The cause is {e}.")
        

def read_file(filename, mode):
    if filename.endswith(".txt"):
        data = []
        with open(filename, mode) as f:
            line = f.readline()
            while line:
                data.append(line.strip())
                line = f.readline()
    elif filename.endswith(".json"):
        data = ""
        with open(filename, mode) as f:
            line = f.readline()
            while line:
                data += line.strip()
                line = f.readline()
            
    return data

def compare(today, yesterday):
    diff = { 
        "diff": False,
        "rating" : 0,
        "solved" : {}
        }
    

    diff['rating'] = today['rating'] - yesterday['rating']
    for t, y in zip(today["solved"].items(), yesterday["solved"].items()):
        if t[1] - y[1] > 0:
            diff["solved"][t[0]] = t[1] - y[1]
            diff["diff"] = True
        
    return diff
######################### api


def main():
    users = read_file("users.txt", 'r')

    for user in users:
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(1)
        today, yesterday = (today.strftime('%y%m%d'), yesterday.strftime('%y%m%d'))
        
        filename = f"{user}.json"    
        path_today = os.path.abspath(f"data/{today}/{filename}")
        path_yesterday = os.path.abspath(f"data/{yesterday}/{filename}")

        if not os.path.exists(path_today):
            for user in users:
                json_data = send_api_with_query("/user/problem_stats", user, "GET")
                save_user_file(user, json_data)
                
        if not os.path.exists(path_yesterday):
            break
        

        content_today = json.loads(read_file(path_today, 'r'))
        content_yesterday = json.loads(read_file(path_yesterday, 'r'))


        
        if content_yesterday is not None:

            diff = compare(content_today, content_yesterday)
            rating = diff["rating"]
            
            if diff["diff"]:
                prompt = [f"{user}님이\n", f"를 해결하셨으며\n점수가 {content_today['rating']}점에서 {content_yesterday['rating']}점\n총 {rating}점 올랐습니다."]
                for rank, count in diff["solved"].items():
                    prompt.insert(1, f"{rank} 문제 {count}개\n")
            else:
                prompt = [f"{user}님이 아무 문제도 풀지 않으셨습니다."]    
            
            prompt.insert(0, "```")    
            prompt.append("```")
            prompt = ''.join(prompt)
            
            
            print(prompt)
            message = {"content": prompt}
            discord_url = open("webhook.txt", 'r').readline()
            
            print(requests.post(discord_url, data=message))
            
            

if __name__ == "__main__":
    main()            