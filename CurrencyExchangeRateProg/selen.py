from selenium import webdriver
import ctypes


class OpenFile:
    def __init__(self, file_name: str, mode: str):
        __tmp_file = open(file_name, 'r')
        self.__tmp_file_content = __tmp_file.read()
        __tmp_file.close()
        self.__tmp_filename = file_name
        try:
            self.file_obj = open(file_name, mode)
        except FileNotFoundError:
            self.file_obj = open(file_name, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file_obj.close()
        if exc_type is None:
            return True
        tmp_file = open(self.__tmp_filename, 'w')
        tmp_file.write(self.__tmp_file_content)
        tmp_file.close()
        return True

    def __enter__(self):
        return self.file_obj


class CurrencyExchange:
    def __init__(self, this_currency: str, another_currency: str):
        self.this_currency = this_currency
        self.another_currency = another_currency
        self.data_from_source: list
        self.driver: webdriver

    def create_url(self):
        return f'https://exchangerates.org.uk/{self.this_currency}-{self.another_currency}-exchange-rate-history.html'

    def open_driver_and_get_data(self):
        self.driver = webdriver.Chrome()
        self.driver.set_window_position(-2000, 0)
        self.driver.get(self.create_url())
        table_row = self.driver.find_elements_by_xpath('//*[@id="hd-maintable"]')
        data = [[td.text for td in row.find_elements_by_class_name('colone') + row.find_elements_by_class_name('coltwo')] for row in table_row][0]
        self.data_from_source = [f'{self.this_currency}/{self.another_currency},{a[-10:]},{a[a.find(f"{self.this_currency} = ") + 6:][:7]}' for a in data]
        # self.data_from_source.sort()


def create_str_from_list(lst_to_str: list) -> str:
    """
    create and return string, which return all values from list
    :param lst_to_str: must be list type
    :return: return str
    """
    return ''.join(map(lambda x: '\n' + x, lst_to_str))[1:]


def refresh_data(currency_instance: CurrencyExchange, file_to_refresh_data: str):
    currency_instance.open_driver_and_get_data()
    with OpenFile(file_to_refresh_data, 'r') as file:
        data_in_file = list(map(lambda x: x.replace("\n", ""), file.readlines()))
        # data_in_file.sort()

    with OpenFile(file_to_refresh_data, 'w') as file:
        result_lst = data_in_file + list(set(currency_instance.data_from_source) - set(data_in_file))
        # result_lst.sort()
        file.write(create_str_from_list(result_lst))

    currency_instance.driver.quit()


try:
    usd_uah = CurrencyExchange('USD', 'UAH')
    eur_uah = CurrencyExchange('EUR', 'UAH')
    for i in (usd_uah, eur_uah):
        refresh_data(i, 'ex.txt')
    ctypes.windll.user32.MessageBoxW(0, 'Готово', 'Поновлення курсу валют', 1)
except:
    ctypes.windll.user32.MessageBoxW(0, 'Сталась помилка! Файл не змінено', 'Поновлення курсу валют', 1)
