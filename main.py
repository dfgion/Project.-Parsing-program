from pprint import pprint
from vk import VKUser
from yandex import YandexUser
import logging

def main():
    VK_ID=input('Введите id в vk:\n') #Запрос ID VK
    TOKEN_VK = ""
    TOKEN_YAN = ""
    count_photos = input('Введите количество фотографий на загрузку:\n')
    name_path = input('Введите, как вы хотите назвать папку на YandexDisk. Не используйте имена существующих папок на диске:\n')
    if VK_ID and TOKEN_VK and TOKEN_YAN and name_path: # Проверка на введение ID, token, name_path
        if count_photos:
            pass
        else:
            count_photos = '5'
        logging.info('MAIN. VK ID has received')
        ya = YandexUser(vk_id = VK_ID, token = TOKEN_YAN, vk_token = TOKEN_VK, photos_count = count_photos, name_path = name_path) 
        vk = VKUser(id = VK_ID, token=TOKEN_VK, count = count_photos) 
        vk.outputting_file() # Создаем json-файл с данными о фотографиях
        ya.get_photo_to_upload()  # Начинаем процесс загрузки фотографий на ЯД
    else: 
        logging.info("MAIN. Token or vk_id or photo's count are not detected.")

if __name__ == "__main__":
    main()
