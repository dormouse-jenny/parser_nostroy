# parser_nostroy
Парсинг данных из реестра http://reestr.nostroy.ru/reestr

Собирает данные из реестра СРО. Поля: (
    'Полное наименование',
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
) и сохраняет в файл sro.csv

Собирает данные из реестра членов СРО. Поля: (
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
 ) и сохраняет в файл sro_members.csv
 
 Собирает данные о свидетельствах о допуске членов СРО. Поля: (
    'Номер свидетельства',
    'Дата выдачи',
    'Основание выдачи свидетельства',
    'Стоимость работ по одному договору ГП',
    'Статус действия свидетельства'
) дополняет каждую строку полями с информацией из реестра членов СРО и сохраняет в файл sro_certificates.csv

Собирает данные о страховании членов СРО. Поля: (
    'Номер договора страхования',
    'Начало действия договора',
    'Окончание действия договора',
    'Размер страховой суммы',
    'Наименование страховой компании',
    'Лицензия',
    'Местонахождение',
    'Контактные телефоны'
) дополняет каждую строку полями с информацией из реестра членов СРО и сохраняет в файл sro_insurance.csv

Собирает данные о проверках членов СРО. Поля: (
    'Дата окончания проверки',
    'Тип проверки',
    'Результат проверки члена СРО',
    'Факты применения мер дисциплинарного воздействия'
) дополняет каждую строку полями с информацией из реестра членов СРО и сохраняет в файл sro_checks.csv
    
    
