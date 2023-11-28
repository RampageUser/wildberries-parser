import time
import csv
from fake_useragent import UserAgent

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def prepare_price(data: str) -> str:
    return data.strip().replace(" ", "").replace("₽", "")


def prepare_name(data: str) -> str:
    return data.replace("/", "").strip()


def get_data(item) -> dict:
    name = item.find_element(By.CLASS_NAME, "product-card__name").text
    name = prepare_name(data=name)
    brand = item.find_element(By.CLASS_NAME, "product-card__brand").text
    price = item.find_element(By.CLASS_NAME, "price__lower-price").text
    price = prepare_price(data=price)
    rate = item.find_element(By.CLASS_NAME, "address-rate-mini").text
    if not rate:
        rate = 0
    link = item.find_element(By.CLASS_NAME, "product-card__link").get_attribute("href")
    data: dict = {
        "name": name,
        "brand": brand,
        "price": price,
        "rate": rate,
        "link": link,
    }
    return data


def create_csv():
    with open("wb.csv", "w") as file:
        writer = csv.DictWriter(
            file, fieldnames=["name", "brand", "price", "rate", "link"]
        )
        writer.writerow({
            "name": "name",
            "brand": "brand",
            "price": "price",
            "rate": "rate",
            "link": "link",
        })


def save_to_csv(data):
    with open("wb.csv", "a") as file:
        writer = csv.DictWriter(
            file, fieldnames=["name", "brand", "price", "rate", "link"]
        )
        writer.writerow(data)


def parsing(product: str):
    fake_user = UserAgent()
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument(f"--user-agent={fake_user.random}")
    page: int = 1

    with webdriver.Chrome(options=options) as driver:

        while True:
            uri: str = f'https://www.wildberries.ru/catalog/0/search.aspx?page={page}&search={product}'
            print(uri)
            driver.get(uri)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "product-card-list")))
            items = driver.find_element(By.CLASS_NAME, 'product-card-list').find_elements(By.CLASS_NAME, "product-card__wrapper")
            if items:
                cards = driver.find_element(By.CLASS_NAME, 'product-card-list').find_element(By.CLASS_NAME, "product-card__link")

                while True:
                    for _ in range(70):
                        cards.send_keys(Keys.DOWN)
                    loaded_items = driver.find_element(By.CLASS_NAME, 'product-card-list').find_elements(By.CLASS_NAME, "product-card__wrapper")
                    if len(items) < len(loaded_items):
                        items = loaded_items
                    else:
                        break
                for item in items:
                    data = get_data(item=item)
                    save_to_csv(data=data)
                page += 1
            else:
                break
