import json
import random
from datetime import datetime, timedelta

# Listes d'exemples de produits et villes
products = [
    "Laptop", "Smartphone", "Tablet", "Headphones", "Keyboard",
    "Mouse", "Monitor", "Webcam", "USB Cable", "Charger"
]

cities = [
    "Istanbul", "Ankara", "Izmir", "Bursa", "Antalya",
    "Adana", "Gaziantep", "Konya", "Mersin", "Diyarbakir"
]

countries = ["Turkey", "Germany", "France", "UK", "Spain"]

# Générer 500 données de commandes
orders = []
for i in range(500):
    order = {
        "orderID": f"ORD{1000 + i}",
        "customerID": f"CUST{random.randint(100, 999)}",
        "productName": random.choice(products),
        "price": round(random.uniform(10.0, 999.99), 2),
        "quantity": random.randint(1, 5),
        "orderDate": (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d %H:%M:%S"),
        "city": random.choice(cities),
        "country": random.choice(countries),
        "status": random.choice(["Completed", "Pending", "Shipped", "Cancelled"])
    }
    orders.append(order)

# Enregistrer au format JSON Lines (chaque ligne est un JSON)
with open('orders_data.json', 'w', encoding='utf-8') as f:
    for order in orders:
        f.write(json.dumps(order, ensure_ascii=False) + '\n')

print(f"✅ {len(orders)} données de commandes créées : orders_data.json")