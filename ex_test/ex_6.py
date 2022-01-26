from json.decoder import JSONDecodeError
import json
import requests
import array
from collections import Counter

response = requests.get("https://playground.learnqa.ru/api/long_redirect")
print(response.text)
array = response.history
print(response.history)

def get_number_of_elements(array):
    count = 0
    for element in array:
        count += 1
    return count
#Вывод числа редиректов
print("Number of elements in the list: ", get_number_of_elements(array))
#Вывод конечного URL
print(response.url)