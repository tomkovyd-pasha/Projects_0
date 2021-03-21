from selenium import webdriver
import requests
import ctypes

URL = 'https://exchangerates.org.uk/USD-EUR-exchange-rate-history.html'
driver = webdriver.Chrome()
driver.set_window_position(-2000, 0)
driver.get(URL)

table_row = driver.find_elements_by_xpath('//*[@id="hd-maintable"]')

data = [[td.text for td in row.find_elements_by_class_name('colone') + row.find_elements_by_class_name('coltwo')] for row in table_row][0]
data_from_source = [f'USD/EUR,{a[-10:]},{a[a.find("USD = ") + 6:][:7]}' for a in data]
data_from_source.sort()


def create_str_from_list(lst_to_str: list) -> str:
    """
    create and return string, which return all values from list
    :param lst_to_str: must be list type
    :return: return str
    """
    return ''.join(map(lambda x: '\n' + x, lst_to_str))[1:]


with open('ex.txt', 'r') as file:
    data_in_file = list(map(lambda x: x.replace("\n", ""), file.readlines()))  # [file.readlines()]
    data_in_file.sort()

with open('ex.txt', 'w') as file:
    result_lst = data_in_file + list(set(data_from_source) - set(data_in_file))
    result_lst.sort()
    file.write(create_str_from_list(result_lst))

driver.quit()
ctypes.windll.user32.MessageBoxW(0, "Готово", "Поновлення курсу валют", 1)
