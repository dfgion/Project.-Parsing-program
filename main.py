from pprint import pprint
from vk import VKUser
from yandex import YandexUser
import logging

def main():
    VK_ID=input('Введите id в vk:\n') #Запрос ID VK
    TOKEN_VK = ""
    TOKEN_YAN = ""
    if VK_ID and TOKEN_VK and TOKEN_YAN: # Проверка на введение ID
        logging.info('MAIN. VK ID has received')
        ya = YandexUser(vk_id = VK_ID, token = TOKEN_YAN, vk_token = TOKEN_VK) 
        vk = VKUser(id = VK_ID, token=TOKEN_VK) 
        pprint(vk.output()) # Выводим словарь с именем файла и его размером\
        ya.get_photo_to_upload()  # Начинаем процесс загрузки фотографий на ЯД
    else: 
        logging.info('MAIN. Token or vk_id not are not detected.')

if __name__ == "__main__":
    main()
