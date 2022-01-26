import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
#response = requests.delete(url)
#print(response.text)

#response = requests.head(url)
#print(response.text)

# response = requests.get(url, params={"method": "GET"})
# print(response.text)

method_x = ["GET", "POST", "PUT", "DELETE"]

for i in method_x:
    response = requests.get(url, params={"method": i})
    print(response.text)

for i in method_x:
    response = requests.post(url, data={"method": i})
    print(response.text)

for i in method_x:
    response = requests.put(url, data={"method": i})
    print(response.text)

for i in method_x:
    response = requests.delete(url, data={"method": i})
    print(response.text)