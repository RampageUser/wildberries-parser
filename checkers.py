from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def check_existence(driver) -> bool:
    try:
        WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CLASS_NAME, 'not-found-search__title')))
        return False

    except TimeoutException:
        return True


def check_correct(driver) -> bool:
    try:
        item = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.CLASS_NAME, 'searching-results__query')))
        item = item.text.strip('«»')
        print(f'Have been found other product: {item}')
        while True:
            result = input('Can I continue parsing (yes / no): ').lower()
            if result in ['n', 'no']:
                return False
            if result in ['y', 'yes']:
                return True
    except TimeoutException:
        return True
