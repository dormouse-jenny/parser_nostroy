# -*- coding: utf-8 -*-
import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

BASE_URL = 'http://reestr.nostroy.ru'
# список полей таблицы СРО
# записывается в файл sro.csv
SRO_KEYS = ['Полное наименование',
    'Сокращенное наименование',
    'Номер в гос. реестре',
    'ИНН',
    'ОГРН',
    'ОКРУГ',
    'Адрес местонахождения',
    'Телефон',
    'E-mail',
    'Адрес сайта',
    'Руководитель коллегиального органа СРО',
    'Руководитель исполнительного органа СРО',
    'Статус'
    ]
# список полей таблицы членов СРО
# записывается в файл sro_members.csv
MEMBER_KEYS = [
    'СРО',
    'Тип члена СРО',
    'Полное наименование',
    'Сокращенное наименование',
    'Статус члена',
    'Регистрационный номер члена в реестре СРО',
    'Дата регистрации в реестре СРО',
    'Дата прекращения членства',
    'Основание прекращения членства',
    'ОГРН',
    'ИНН',
    'Дата государственной регистрации',
    'Номер контактного телефона',
    'Адрес местонахождения юридического лица',
    'ФИО, осуществляющего функции единоличного исполнительного органа юридического лица и (или) руководителя коллегиального исполнительного органа юридического лица',
    'Сведения о соответствии члена СРО условиям членства в СРО, предусмотренным законодательством РФ и (или) внутренними документами СРО',
    'Размер взноса в компенсационный фонд СРО',
    'Обновлено'
    ]
# у ИП на странице члена СРО другие названия полей.
# это их соответствие полям из MEMBER_KEYS
IP_OOO_MAP = {
'ОГРНИП': 'ОГРН',
'Адрес места фактического осуществления деятельности индивидуального предпринимателя':'Адрес местонахождения юридического лица',
'ФИО (при наличии) индивидуального предпринимателя':'ФИО, осуществляющего функции единоличного исполнительного органа юридического лица и (или) руководителя коллегиального исполнительного органа юридического лица'
} 

# список полей таблицы свидетельств о допуске членов СРО 
# (совпадающие поля берутся из таблицы членов СРО)
# записывается в файл sro_certificates.csv
CERTIFICATE_KEYS = [
    'СРО',
    'Тип члена СРО',
    'Полное наименование',
    'Сокращенное наименование',
    'Статус члена',
    'Регистрационный номер члена в реестре СРО',
    'Дата регистрации в реестре СРО',
    'Дата прекращения членства',
    'Основание прекращения членства',
    'ОГРН',
    'ИНН',
    'Дата государственной регистрации',
    'Номер контактного телефона',
    'Адрес местонахождения юридического лица',
    'ФИО, осуществляющего функции единоличного исполнительного органа юридического лица и (или) руководителя коллегиального исполнительного органа юридического лица',
    'Сведения о соответствии члена СРО условиям членства в СРО, предусмотренным законодательством РФ и (или) внутренними документами СРО',
    'Размер взноса в компенсационный фонд СРО',
    'Обновлено',# <-- заполняется из таблицы членов СПО| сведения о свидетельстве -->
    'Номер свидетельства',
    'Дата выдачи',
    'Основание выдачи свидетельства',
    'Стоимость работ по одному договору ГП',
    'Статус действия свидетельства'
    ]
# список полей таблицы страхования членов СРО 
# (совпадающие поля берутся из таблицы членов СРО)
# записывается в файл sro_insurance.csv
INSURANCE_KEYS = [
    'СРО',
    'Тип члена СРО',
    'Полное наименование',
    'Сокращенное наименование',
    'Статус члена',
    'Регистрационный номер члена в реестре СРО',
    'Дата регистрации в реестре СРО',
    'Дата прекращения членства',
    'Основание прекращения членства',
    'ОГРН',
    'ИНН',
    'Дата государственной регистрации',
    'Номер контактного телефона',
    'Адрес местонахождения юридического лица',
    'ФИО, осуществляющего функции единоличного исполнительного органа юридического лица и (или) руководителя коллегиального исполнительного органа юридического лица',
    'Сведения о соответствии члена СРО условиям членства в СРО, предусмотренным законодательством РФ и (или) внутренними документами СРО',
    'Размер взноса в компенсационный фонд СРО',
    'Обновлено',# <-- заполняется из таблицы членов СПО| сведения о сстраховании -->
    'Номер договора страхования',
    'Начало действия договора',
    'Окончание действия договора',
    'Размер страховой суммы',
    'Наименование страховой компании',
    'Лицензия',
    'Местонахождение',
    'Контактные телефоны'
    ]
# список полей таблицы проверок членов СРО 
# (совпадающие поля берутся из таблицы членов СРО)
# записывается в файл sro_checks.csv
CHECK_KEYS = [
    'СРО',
    'Тип члена СРО',
    'Полное наименование',
    'Сокращенное наименование',
    'Статус члена',
    'Регистрационный номер члена в реестре СРО',
    'Дата регистрации в реестре СРО',
    'Дата прекращения членства',
    'Основание прекращения членства',
    'ОГРН',
    'ИНН',
    'Дата государственной регистрации',
    'Номер контактного телефона',
    'Адрес местонахождения юридического лица',
    'ФИО, осуществляющего функции единоличного исполнительного органа юридического лица и (или) руководителя коллегиального исполнительного органа юридического лица',
    'Сведения о соответствии члена СРО условиям членства в СРО, предусмотренным законодательством РФ и (или) внутренними документами СРО',
    'Размер взноса в компенсационный фонд СРО',
    'Обновлено',# <-- заполняется из таблицы членов СПО| сведения о проверках -->
    'Дата окончания проверки',
    'Тип проверки',
    'Результат проверки члена СРО',
    'Факты применения мер дисциплинарного воздействия'
    ]

def get_html(url):
    response = urlopen(url)
    return response.read()

def get_page_count(html):
    soup = BeautifulSoup(html,'html.parser')
    pagination = soup.find('ul', class_='pagination')
    last_page = pagination.find_all('li')[-3].a.text
    return int(last_page)

def parse_members_page(html):
    # на странице строго одна запись.
    member = dict.fromkeys(MEMBER_KEYS)
    soup = BeautifulSoup(html,'html.parser')
    table = soup.find('table', class_='items table')
    
    for row in table.find_all('tr'):
        col_name = row.th.text.strip(" :\n")
        # на случай если ето ИП подставляем вместо _не_тех_ имен полей такие же как в ООО
        member[IP_OOO_MAP.get(col_name,col_name)] = row.td.text.strip(" \n")
    
    return member

def parse_sertificates_page(html,member):
    #сертификатов на странице одного члена СРО может быть 0 1 или много
    sertificates_table = []
    soup = BeautifulSoup(html,'html.parser')
    table = soup.find('table', class_='items table')
    header_cols = table.find('tr').find_all('th')
    # две первых строки шапка, после каждой нормальной строки идут две служебных
    for row in table.find_all('tr',)[2::3]:
        #заполняем ключи и общие данные из словаря члена СРО
        sertificate = {key : member.get(key) for key in CERTIFICATE_KEYS}
        row_cols = row.find_all('td')
        for col_num in range(1,6):# Нужны колонки с 2 по 6
            sertificate[header_cols[col_num].text.strip(' :\n')] = \
            row_cols[col_num].text.strip(' \n&downarrow;')
        sertificates_table.append(sertificate)
    
    return sertificates_table

def parse_insurance_page(html,member):
    # страховок на странице одного члена СРО может быть 0 1 или много
    insurance_table = []
    soup = BeautifulSoup(html,'html.parser')
    table = soup.find('table', class_='items table')
    header_cols = table.find_all('tr')[1].find_all('th')#шапка вторая строка
    # три первых строки шапка, остальное данные
    for row in table.find_all('tr',)[3:]:
        #заполняем ключи и общие данные из словаря члена СРО
        insurance = {key : member.get(key) for key in INSURANCE_KEYS}
        row_cols = row.find_all('td')
        for col_num in range(1,9):# Нужны колонки с 2 по 9
            insurance[header_cols[col_num].text.strip(' :\n')] = \
            row_cols[col_num].text.strip(' \n&downarrow;')
        insurance_table.append(insurance)
    
    return insurance_table

def parse_checks_page(html,member):
    # проверок на странице одного члена СРО может быть 0 1 или много
    checks_table = []
    soup = BeautifulSoup(html,'html.parser')
    table = soup.find('table', class_='items table')
    header_cols = table.find('tr').find_all('th')
    # две первых строки шапка, остальное данные
    for row in table.find_all('tr',)[2:]:
        #заполняем ключи и общие данные из словаря члена СРО
        check = {key : member.get(key) for key in CHECK_KEYS}
        row_cols = row.find_all('td')
        for col_num in range(1,5):# Нужны колонки с 2 по 5
            check[header_cols[col_num].text.strip(' :\n')] = \
            row_cols[col_num].text.strip(' \n&downarrow;')
        checks_table.append(check)
    
    return checks_table

def parse_members_table(html):
    members_table = []
    sertificates_table =[]
    insurance_table =[]
    checks_table = []
    soup = BeautifulSoup(html,'html.parser')
    table = soup.find('table', class_='items table table-selectable-row table-striped')
    
    for row in table.find_all('tr', class_='sro-link'):
        client_url = BASE_URL + row.get('rel')
        member = parse_members_page(get_html(client_url))
        members_table.append(member)
        sertificates = parse_sertificates_page(get_html(client_url+'/certificates'),member)
        sertificates_table.extend(sertificates)
        insurance = parse_insurance_page(get_html(client_url+'/insurance'),member)
        insurance_table.extend(insurance)
        checks = parse_checks_page(get_html(client_url+'/checks'),member)
        checks_table.extend(checks)
        
    return members_table, sertificates_table, insurance_table, checks_table

def parse_SRO_page(html):
    sro = dict.fromkeys(SRO_KEYS)
    soup = BeautifulSoup(html,'html.parser')
    table = soup.find('div', class_='col-md-9 block-content-open-client-data-wrapper')
    for row in table.find_all('div',class_ = re.compile("field-row")):
        sro[row.find('div',class_ = "field-title").text.strip(" :\n")] = \
        row.find('div',class_ = "field-data").text.strip(" \n")
    return sro

def parse_SRO_table(html):
    sro_table = []
    soup = BeautifulSoup(html,'html.parser')
    table = soup.find('table', class_='items table table-striped table-selectable-row ')
    
    for row in table.find_all('tr', class_='sro-link'):
        client_url = BASE_URL + row.get('rel')
        sro = parse_SRO_page(get_html(client_url))
        sro['Статус'] = row.find('td',class_ = 'user-enabled-wrapper').text.strip()
        sro_table.append(sro)
    
    return sro_table

def main():
    csv.register_dialect('opendata', delimiter=',', quotechar='"',quoting=csv.QUOTE_NONNUMERIC)
    # файл парсинга реестра СРО
    sro_file = open('sro.csv', 'w')
    sro_csv = csv.DictWriter(sro_file,dialect = 'opendata',fieldnames=SRO_KEYS)
    sro_csv.writeheader()
    total_pages = get_page_count(get_html(BASE_URL))
    print('Парсинг реестра СРО. Всего %d страниц.' % total_pages)
    for page in range(1, total_pages+1):
        print('Парсинг %d%% (%d/%d)' % (page / total_pages * 100, page, total_pages))
        # читаем страницу данных
        sro_table = \
        parse_SRO_table(get_html(BASE_URL + "?sort=u.registrationnumber&direction=ASC&page=%d" %page))
        #записываем страницу данных в csv
        sro_csv.writerows(sro_table)
    sro_file.close()
    
    # файл парсинга реестра членов СРО
    members_file = open('sro_members.csv', 'w')
    members_csv = csv.DictWriter(members_file,dialect = 'opendata',fieldnames=MEMBER_KEYS)
    members_csv.writeheader()
    # файл парсинга свидетельств о допуске членов СРО
    certificates_file = open('sro_certificates.csv', 'w')
    certificates_csv = csv.DictWriter(certificates_file,dialect = 'opendata',fieldnames=CERTIFICATE_KEYS)
    certificates_csv.writeheader()
    # файл парсинга страхования членов СРО
    insurance_file = open('sro_insurance.csv', 'w')
    insurance_csv = csv.DictWriter(insurance_file,dialect = 'opendata',fieldnames=INSURANCE_KEYS)
    insurance_csv.writeheader()
    # файл парсинга проверок членов СРО
    checks_file = open('sro_checks.csv', 'w')
    checks_csv = csv.DictWriter(checks_file,dialect = 'opendata',fieldnames=CHECK_KEYS)
    checks_csv.writeheader()
    
    total_pages = get_page_count(get_html(BASE_URL+"/reestr"))
    print('Парсинг реестра членов СРО. Всего %d страниц.' % total_pages)
    #total_pages = 70
    for page in range(1, total_pages+1):
        print('Парсинг %d%% (%d/%d)' % (page / total_pages * 100, page, total_pages))
        # читаем страницу данных
        members_table, certificates_table, insurance_table, checks_table = \
        (parse_members_table(get_html(BASE_URL + "/reestr?sort=m.id&direction=asc&page=%d" %page)))
        #записываем страницу данных в csv
        members_csv.writerows(members_table)
        certificates_csv.writerows(certificates_table)
        insurance_csv.writerows(insurance_table)
        checks_csv.writerows(checks_table)
    
    members_file.close()
    certificates_file.close()
    insurance_file.close()
    checks_file.close()
    print('Парсинг завершен')

if __name__ == '__main__':
    main()
