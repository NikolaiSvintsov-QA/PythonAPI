import requests
import json
from pprint import pprint
import uuid
import random

BASE_URL = "https://simple-books-api.click"


# response = requests.get(f"{BASE_URL}/status")
#
# print("Status Code: ", response.status_code)
# print("Response body:" , response.json)
#
# params = {
#     "type": "fiction",
#     "limit": 3
# }
# response = requests.get(f"{BASE_URL}/books" , params=params) # если не указывать params  - то он выведет все не применив параметры.
# print("Books:", response.json())

# book_id = 3
# response = requests.get(f"{BASE_URL}/books/{book_id}")
# print("Book Details:", response.json())
"""
- import uuid 'одна из маленьких, но очень полезных' библиотек Python
uuid — это стандартная библиотека Python (входит в базовую поставку).
Название расшифровывается как 'Universal Unique IDentifier' —
«универсальный уникальный идентификатор».
"""
unique_id = uuid.uuid4().hex[:6] #Что делает [:6] срезание строки — берём только первые 6 символов из всей строки .hex
"""
🔹Что делает .hex
uuid.uuid4() возвращает объект UUID, а у него есть свойство .hex,
которое превращает его в строку из 32 шестнадцатеричных символов "без дефисов".
"""
client_name = f"NikFer{unique_id}"
client_email = f"NikFer{unique_id}@yandex.ru"

headers = {
    "Content-Type": "application/json"
}
payload = {
    "clientName": f"{client_name}",
    "clientEmail": f"{client_email}"
}
response = requests.post(f"{BASE_URL}/api-clients", headers=headers, data=json.dumps(payload))
"""
Комментарий, что такое dumps!!!
json — это встроенный модуль Python, который умеет:
превращать Python-объекты → в JSON-строку (через json.dumps);
и наоборот, JSON-строку → в Python-объект (через json.loads).
"""
if response.status_code == 201:
    access_token = response.json().get("accessToken")
    print(response.status_code)
    print("Access Token: ",access_token)
    print("Clint Email: ", client_email)
    print("Clint Name", client_name)
else:
    raise "Failed to get access token"

headers = {
    "Authorization": f"Bearer {access_token}",
"Content-Type": "application/json"
}

order_payload = {
    "bookId" :1,
    "customerName":f"{client_name}"
}

response = requests.post(f"{BASE_URL}/orders", headers=headers, data= json.dumps(order_payload))

order = response.json()
print("Order Created", order)



response = requests.get(f"{BASE_URL}/orders",
                        headers=headers)
print("Orders:", response.json())

order_id = order["orderId"]
response = requests.get(f"{BASE_URL}/orders/{order_id}",
                        headers=headers)
print("Order Details:", response.json())
print("Customer Name", response.json().get("customerName"))

unique_new_users =uuid.uuid4().hex[:6]
new_customer_name = f"Updated Customer_{unique_new_users}"

headers = {
    "Authorization": f"Bearer {access_token}",
"Content-Type": "application/json"
}

update_payload = {
    "customerName": f"{new_customer_name}"
}

response = requests.patch(f"{BASE_URL}/orders/{order_id}",
                          headers=headers,
                          data=json.dumps(update_payload))
print("Patch Status Code:", response.status_code)
print("Name of new Customers", new_customer_name)

response = requests.get(f"{BASE_URL}/orders/{order_id}",
                        headers=headers)

delete_response = requests.delete(f"{BASE_URL}/orders/{order_id}", headers=headers)

print("Deleted Code: ", response.status_code)




