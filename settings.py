import time
from fake_useragent import UserAgent
import database
import checkers

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


def make_uri(product:list, page:int) -> str:
    if page == 1:
        space: str = '%20'
        current_page: str = ''
        sort: str = ''
    else:
        space: str = '+'
        current_page: str = f'page={page}'
        sort: str = '&sort=popular'
    current_product: str = space.join(product)
    uri: str = f'https://www.wildberries.ru/catalog/0/search.aspx?{current_page}{sort}&search={current_product}'
    return uri


def count_items(driver:webdriver) -> int:
    quantity = driver.find_element(
        By.CSS_SELECTOR, '#catalog > div > div.catalog-page__searching-results.searching-results > div > span > span:nth-child(1)'
    )
    quantity_items = int(quantity.text.replace(' ', ''))
    print(f'Have been found {quantity_items} product cards')
    return quantity_items


def smooth_scroll(driver, scrolls=3) -> None:
    for _ in range(scrolls):
        actions = ActionChains(driver)
        actions.send_keys(Keys.END)
        actions.perform()
        time.sleep(0.8)


def prepare_name(data: str) -> str:
    return data.replace("/", "").strip()


def prepare_price(data: str) -> int:
    return int(data.strip().replace(" ", "").replace("₽", ""))


def get_data(driver:webdriver) -> list[dict]:
    list_of_products: list = []
    products = driver.find_element(By.CLASS_NAME, 'product-card-list').find_elements(By.CLASS_NAME, 'product-card__wrapper')
    for product in products:
        name = product.find_element(By.CLASS_NAME, 'product-card__name').text
        name = prepare_name(data=name)
        brand = product.find_element(By.CLASS_NAME, 'product-card__brand').text
        if not brand:
            brand: str = 'NULL'
        price = product.find_element(By.CLASS_NAME, 'price__lower-price').text
        price = prepare_price(data=price)
        rate = product.find_element(By.CLASS_NAME, 'address-rate-mini--sm').text
        if not rate:
            rate: int = 0
        link = product.find_element(By.CLASS_NAME, 'product-card__link').get_attribute('href')
        data: dict = {
            "name": name,
            "brand": brand,
            "price": price,
            "rate": rate,
            "link": link,
        }
        list_of_products.append(data)
    return list_of_products


def parsing(product: list) -> None:
    fake_user = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument(f"--user-agent={fake_user.random}")
    page: int = 1

    with webdriver.Chrome(options=options) as driver:
        driver.get(make_uri(product=product, page=page))
        print('Wait please')
        is_exist: bool = checkers.check_existence(driver=driver)
        if is_exist:
            is_correct: bool = checkers.check_correct(driver=driver)
            if is_correct:
                database.create_csv()
                quantity_items: int = count_items(driver=driver)
                counter: int = 0

                while True:
                    print('Start parsing' if page == 1 else f'Page № {page}')
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-card-list')))
                    smooth_scroll(driver=driver)
                    list_of_items: list[dict] = get_data(driver=driver)
                    if list_of_items:
                        database.save_to_csv(data=list_of_items)
                        counter += len(driver.find_element(By.CLASS_NAME, 'product-card-list').find_elements(
                            By.CLASS_NAME, 'product-card__wrapper'
                        ))
                        if counter != quantity_items:
                            page += 1
                            driver.get(make_uri(product=product, page=page))
                        else:
                            print('Done')
                            break
                    else:
                        print('End')
                        break
            else:
                print('Parsing interruption')
        else:
            print('Product did not find')
