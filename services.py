from selenium import webdriver
import time
from bs4 import BeautifulSoup as BS
import json


def get_operations():
    urls = {
        'Investmeal': 'https://snowball-income.com/public/portfolios/investmeal#transactions',
        'artydev & Co': 'https://snowball-income.com/public/portfolios/THgGwOeEua#transactions'
    }
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=chrome_options)

    with open('operations.json', 'r', encoding='utf-8') as f:
        try:
            all_operations = json.load(f)
        except:
            all_operations = {}

    for author, url in urls.items():
        try:
            driver.get(url=url)

            time.sleep(3)

            with open('page-source.html', 'w', encoding='utf-8') as file:
                file.write(driver.page_source)

            with open('page-source.html', 'r', encoding='utf-8') as file:
                src = file.read()

            soup = BS(src, 'lxml')
            items_trs = soup.find('table', class_='table-head-custom').find_all('tr')

            for tr in items_trs:
                items_tds = tr.find_all('td')

                operation = []
                json_operation = {}
                for td in items_tds:
                    operation.append(td.text)

                if operation:
                    json_operation['name'] = operation[0]
                    json_operation['organization'] = operation[1][0:-4]
                    json_operation['ticket'] = operation[1][-4:]
                    json_operation['date'] = operation[2]
                    json_operation['amount'] = operation[3]
                    json_operation['price'] = operation[4]
                    json_operation['commission'] = operation[5]
                    json_operation['sum'] = operation[6]
                    json_operation['profit'] = operation[7]
                    json_operation['author'] = author
                    json_operation['is_new'] = True

                    id = json_operation['organization'] + json_operation['date']

                    if id not in all_operations:
                        all_operations[id] = json_operation

        except:
            pass

        with open('operations.json', 'w', encoding='utf-8') as f:
            json.dump(all_operations, f, indent=4, ensure_ascii=False)

    time.sleep(5)

    driver.quit()
