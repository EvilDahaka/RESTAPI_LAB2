import requests 
import json

#Налаштування
BASE_URL = "https://api.thecatapi.com/v1"
API_KEY = "live_AyPsIzjF6cieRjQSEw1xeMuvPfwkSdQXdufU61RwGjFzQVENjrAI7airz8bVnJ5m"  

#Функції для HTTP-запитів та Інтерактивного Виведення 
def get_random_image():
    """
    GET-запит 1: Отримання випадкового зображення кота
    """
    print("\n--- Виконання GET запиту: Отримання випадкового зображення ---")
    
    endpoint = f"{BASE_URL}/images/search"
    
    try:
        response = requests.get(endpoint)
        
        # Перевірка статусу відповіді та інтерактивне виведення
        if response.status_code == 200:
            data = response.json()
            print(f"Успіх! Статус-код: {response.status_code}")
            
            if data:
                cat_info = data[0]
                image_id = cat_info.get("id")
                image_url = cat_info.get("url")
                
                print(f"  ID зображення: **{image_id}**")
                print(f"  URL зображення: {image_url}")
                return image_id
            else:
                print("   Не отримано даних із сервера.")
        else:
            print(f"Помилка! Статус-код: **{response.status_code}**")
            print(f"Тіло відповіді (помилка): {response.text}")
    
    except requests.exceptions.RequestException as e:
        print(f"Помилка підключення: {e}")
    
    return None


def get_breeds():
    """
    GET-запит 2: Отримання списку порід
    """
    print("\n--- Виконання GET запиту: Отримання списку порід ---")
    
    endpoint = f"{BASE_URL}/breeds"
    
    try:
        # Обмежуємо 3 породами для чистоти консолі
        response = requests.get(endpoint, params={'limit': 3}) 
        
        if response.status_code == 200:
            breeds = response.json()
            print(f"Успіх! Статус-код: {response.status_code}")
            print(f"Отримано {len(breeds)} порід:")
            for breed in breeds:
                print(f"   **{breed['name']}** (ID: {breed['id']})")
        else:
            print(f"Помилка! Статус-код: **{response.status_code}**")
    except requests.exceptions.RequestException as e:
        print(f"Помилка підключення: {e}")


def create_favourite(image_id):
    """
    POST-запит: Додавання зображення в обране
    """
    print("\n--- Виконання POST запиту: Додавання в обране (Зміна Ресурсу) ---")

    if not API_KEY:
        print("Для успішного POST запиту необхідний API Key. Запит виконується без ключа")
        # Для демонстрації POST-запиту навіть без ключа
    
    endpoint = f"{BASE_URL}/favourites"
    headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}
    payload = {"image_id": image_id, "sub_id": "lab_user_python"}
    
    try:
        response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 200:
            data = response.json()
            print(f"Успіх! Статус-код: **{response.status_code}**")
            print(f"Повідомлення: **{data.get('message')}**")
            print(f"ID обраного: {data.get('id')}")
        elif response.status_code == 400:
            print(f"Помилка! Статус-код: **{response.status_code}** (Помилка Клієнта)")
            print(f"Тіло відповіді: {response.json().get('message', 'Немає повідомлення')}")
        else:
            print(f"Помилка! Статус-код: **{response.status_code}**")
            print(f"Тіло відповіді: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"Помилка підключення: {e}")

#Головна функція
def main():
    print("Cat api(Лабораторна 2)")

    #Виконання першого GET-запиту 
    image_id = get_random_image()

    #Виконання другого GET-запиту 
    get_breeds()
    
    #Виконання POST-запиту 
    if image_id:
        # Для POST використовуємо ID, отриманий у першому запиті
        create_favourite(image_id)
    
    print("Програма завершила роботу")


if __name__ == "__main__":
    main()