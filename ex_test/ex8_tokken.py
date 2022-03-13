import requests
import time
from json.decoder import JSONDecodeError

response1 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")

try:
    answer_json1 = response1.json()
except JSONDecodeError:
    print("Response is not a JSON format")

seconds_key = "seconds"
token_key = "token"

if answer_json1 is not None and seconds_key in answer_json1 and token_key in answer_json1:
    seconds = answer_json1[seconds_key]
    token = answer_json1[token_key]
    response2 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={'token':token})
    try:
        answer_json2 = response2.json()
    except JSONDecodeError:
        print("Response is not a JSON format")
    status_key = "status"
    if answer_json2 is not None and status_key in answer_json2:
        check_status = answer_json2[status_key]
        if check_status == "Job is NOT ready":
            print(check_status)
        else:
            print("Статус не соответствует Job is NOT ready")
        time.sleep(seconds+1)
        response3 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={'token':token})
        try:
            answer_json3 = response3.json()
        except JSONDecodeError:
            print("Response is not a JSON format")
        result_key = "result"
        if answer_json3 is not None and status_key in answer_json3 and result_key in answer_json3:
            check_status2 = answer_json3[status_key]
            check_result = answer_json3[result_key]
            if check_status2 == "Job is ready":
                print(check_status2)
            else:
                print("Статус не соответствует Job is ready")
            if check_result is not None:
                print(f"Результат: {check_result}")
            else:
                print("Результата нет")
        else:
            print(f"Ключa {status_key} и/или {result_key} в JSON нет")
    else:
        print(f"Ключa {status_key} в JSON нет")
else:
    print(f"Ключa {seconds_key} и/или {token_key} в JSON нет")