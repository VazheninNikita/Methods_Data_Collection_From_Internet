# https://hh.ru/search/vacancy?area=1&fromSearchLine=true&text=python
import re
from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import json

base_url = 'https://hh.ru/'

keyword = input('Enter keyword: ')

url = base_url + '/search/vacancy?area=1&fromSearchLine=true&text=' + keyword

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15'}

# response = requests.get(url, headers=headers)
# with open('response.html', 'w', encoding='utf-8') as f:
#     f.write(response.text)

html_file = ''
with open('response.html', 'r', encoding='utf-8') as f:
    html_file = f.read()

dom = bs(html_file, 'html.parser')

vacancies = dom.find_all('div', {'class': 'vacancy-serp-item'})

### Определяем кол-во страниц
def max_num():
    mnum = 0
    for item in dom.find_all('a', {'data-qa': 'pager-page'}):
        mnum = list(item.strings)[0].split(" ")[-1]
    return mnum

max_page = int(max_num())

### Собираем данные
def data_collect(pages):
    vacancies_list = []
    for page in range(pages):
        url_p = base_url + 'search/vacancy?clusters=true&area=1&ored_clusters=true&enable_snippets=true&salary=&text=' + keyword + 'python&page=' + str(page) + '&hhtmFrom=vacancy_search_list'
        response_p = requests.get(url_p, headers=headers)
        dom_p = bs(response_p.text, 'html.parser')
        vacancies_p = dom_p.find_all('div', {'class': 'vacancy-serp-item'})
        for vacancy in vacancies_p:
            vacancy_data = {}
            vacancy_link = vacancy.find('a', {'class': 'bloko-link'})['href']
            vacancy_title = vacancy.find('span', {'class': 'resume-search-item__name'}).getText()
            vacancy_employer = vacancy.find('a', {'class': 'bloko-link bloko-link_kind-tertiary'}).getText().replace(' ',' ')
            vacancy_salary = vacancy.find('span', {'class': 'bloko-header-section-3'})
            vacancy_salary_data = {'min_salary': '', 'max_salary': '', 'currency': ''}
            if vacancy_salary is None:
                vacancy_salary_data['min_salary'] = None
                vacancy_salary_data['max_salary'] = None
                vacancy_salary_data['currency'] = None
            else:
                vacancy_salary = vacancy_salary.getText().replace("\u202f", '').split()
                if 'от' in vacancy_salary and 'до' not in vacancy_salary:
                    if 'руб.' in vacancy_salary:
                        vacancy_salary_data['min_salary'] = int(vacancy_salary[1])
                        vacancy_salary_data['max_salary'] = None
                        vacancy_salary_data['currency'] = 'руб.'
                    if 'USD' in vacancy_salary:
                        vacancy_salary_data['min_salary'] = int(vacancy_salary[1])
                        vacancy_salary_data['max_salary'] = None
                        vacancy_salary_data['currency'] = 'USD'
                    if 'EUR' in vacancy_salary:
                        vacancy_salary_data['min_salary'] = int(vacancy_salary[1])
                        vacancy_salary_data['max_salary'] = None
                        vacancy_salary_data['currency'] = 'EUR'
                if 'до' in vacancy_salary and 'от' not in vacancy_salary :
                    if 'руб.' in vacancy_salary:
                        vacancy_salary_data['min_salary'] = None
                        vacancy_salary_data['max_salary'] = int(vacancy_salary[1])
                        vacancy_salary_data['currency'] = 'руб.'
                    if 'USD' in vacancy_salary:
                        vacancy_salary_data['min_salary'] = None
                        vacancy_salary_data['max_salary'] = int(vacancy_salary[1])
                        vacancy_salary_data['currency'] = 'USD'
                    if 'EUR' in vacancy_salary:
                        vacancy_salary_data['min_salary'] = None
                        vacancy_salary_data['max_salary'] = int(vacancy_salary[1])
                        vacancy_salary_data['currency'] = 'EUR'
                if 'от' not in vacancy_salary and 'до' not in vacancy_salary:
                    if 'руб.' in vacancy_salary:
                        vacancy_salary_data['min_salary'] = int(vacancy_salary[0])
                        vacancy_salary_data['max_salary'] = int(vacancy_salary[2])
                        vacancy_salary_data['currency'] = 'руб.'
                    if 'USD' in vacancy_salary:
                        vacancy_salary_data['min_salary'] = int(vacancy_salary[0])
                        vacancy_salary_data['max_salary'] = int(vacancy_salary[2])
                        vacancy_salary_data['currency'] = 'USD'
                    if 'EUR' in vacancy_salary:
                        vacancy_salary_data['min_salary'] = int(vacancy_salary[0])
                        vacancy_salary_data['max_salary'] = int(vacancy_salary[2])
                        vacancy_salary_data['currency'] = 'EUR'
                if 'от' in vacancy_salary and 'до' in vacancy_salary:
                    if 'руб.' in vacancy_salary:
                        vacancy_salary_data['min_salary'] = int(vacancy_salary[1])
                        vacancy_salary_data['max_salary'] = int(vacancy_salary[3])
                        vacancy_salary_data['currency'] = 'руб.'
                    if 'USD' in vacancy_salary:
                        vacancy_salary_data['min_salary'] = int(vacancy_salary[1])
                        vacancy_salary_data['max_salary'] = int(vacancy_salary[3])
                        vacancy_salary_data['currency'] = 'USD'
                    if 'EUR' in vacancy_salary:
                        vacancy_salary_data['min_salary'] = int(vacancy_salary[1])
                        vacancy_salary_data['max_salary'] = int(vacancy_salary[3])
                        vacancy_salary_data['currency'] = 'EUR'
            vacancy_data['vacancy_title'] = vacancy_title
            vacancy_data['vacancy_employer'] = vacancy_employer
            vacancy_data['vacancy_link'] = vacancy_link
            vacancy_data['vacancy_salary'] = vacancy_salary_data
            vacancies_list.append(vacancy_data)
    return vacancies_list


data = data_collect(max_page)

### Запись в json
def data_to_json(data):
    with open('vacancies.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


data_to_json(data)


