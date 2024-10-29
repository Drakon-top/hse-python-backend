from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from faker import Faker
from faker.generator import random

faker = Faker()
path = "http://localhost:8000/cart"


def create_cart():
    for _ in range(500):
        response = requests.post(path)
        print(response)


def get_cart():
    for _ in range(500):
        response = requests.post(f"{path}/{random.choice([1, 100])}")
        print(response)


with ThreadPoolExecutor() as executor:
    futures = {}

    for i in range(15):
        futures[executor.submit(create_cart)] = f"create-cart-{i}"

    for future in as_completed(futures):
        print(f"completed {futures[future]}")

    future = {}

    for i in range(15):
        futures[executor.submit(get_cart)] = f"get-cart-{i}"

    for future in as_completed(futures):
        print(f"completed {futures[future]}")
