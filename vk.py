from itertools import count
from pprint import pprint
import requests
from datetime import datetime
import logging
import enlighten
import time
import json

class VKUser:
    """Действия с API VK"""
    logging.basicConfig(level = logging.INFO, 
                        filename = "py_log.log",
                        filemode = "w",
                        format = "%(asctime)s %(levelname)s %(message)s",
                        encoding = 'utf-8')

    def __init__(self, id, token, count): # В инициализации прописаны обязательные параметры, показан ID и token, которые нужны для работы во многих методах класса
        self.token = token
        self.id = id
        self.params = {'access_token': self.token,
                       'v': '5.131'}
        self.url = 'https://api.vk.com/method/' 
        self.count = count

    def filter_photo(self, json): # Больший формат из всех всегда лежит последним в списке, поэтому просто берем элемент с индексом -1
        logging.info('VK. Data has sent for filtering')
        manager = enlighten.get_manager() #Создание класса
        pbar = manager.counter(total=100, desc='Ti', unit='ticks') #Выполнение метода для корректной работы програсс бара в log
        for el in json['response']['items']: 
            filter_list = el['sizes'][-1]
            el['sizes'] = filter_list
        for i in range(1, 11):
            logging.info("VK. Processing step %s" % i)
            time.sleep(0.25)
            pbar.update()
        return json

    def get_photos(self,): # Метод выполняет основную задачу: выполняет запрос методом GET и получает json с необходимой информацией
        logging.info('VK. Function for getting photos has activated.')
        photos_url = self.url + 'photos.get'
        logging.info('VK. Request URL was received.')
        photos_params = {'owner_id': self.id,  
                       'album_id': 'profile',
                       'count': self.count,
                       'extended': 1}
        logging.info('VK. Params have generated.')
        response=requests.get(photos_url, params = {**self.params, **photos_params}).json()
        logging.info('VK. Request has sent.')
        self.filter_photo(response) # Вызываем метод класса для того, чтобы оставить только самый большой формат фотографии
        return response
        
    def outputting_file(self): # Метод служит для вывода пользователю результата запроса в виде словаря, в котором прописано имя, размер и при необходимости дата
        try:
            logging.info('VK. First function has activated. Token and ID were initialed.')
            result = self.get_photos()['response']['items'] # Берется json по основному методу get_photos
            list_photos = []
            manager = enlighten.get_manager()
            pbar = manager.counter(total=  100, desc = 'Ti', unit = 'ticks')
            logging.info('VK. Filtered data was receive to create a dictionary')
            for el in result:
                dict_photo = {'file_name': self.name_formation(result, name = el['likes']['count'], date = datetime.utcfromtimestamp(int(el['date'])).strftime('%Y-%m-%d')), # метод из класса формирует имя(включает дату в название файла или оставляет только кол-во лайков), а второй метод из библиотеки datetime, который преобразовывает дату из Unix в привычный нам формат
                              'size': '{}'.format(el['sizes']['type'])}   
                list_photos.append(dict_photo)
            for i in range(1, 11):
                logging.info("VK. Processing step %s" % i)
                time.sleep(0.25)
                pbar.update()
            with open('data about uploaded photos.json', 'w') as f:
                json_data = json.dumps(list_photos, indent = 1)
                f.write(json_data)
            logging.info('File with data has created')
        except KeyError:
            logging.error("VK. Received data was incorrect. Couldn't get the correct dictionary. The program is deactivated.", exc_info=True)
            return 'Не удалось найти информацию по человеку с таким id'

    def dict_to_yandex(self):
        try:
            result = self.get_photos()['response']['items']
            list_photos = []
            for el in result:
                dict_photo = {'file_name': self.name_formation(result, name = el['likes']['count'], date = datetime.utcfromtimestamp(int(el['date'])).strftime('%Y-%m-%d')),
                              'url': '{}'.format(el['sizes']['url'])}   
                list_photos.append(dict_photo)
            return list_photos
        except KeyError:
            logging.error("VK. Received data was incorrect. Couldn't get the correct dictionary. The program is deactivated.")
            return 'Не удалось найти информацию по человеку с таким id'

    def name_formation(self, list, name, date):
        logging.info('VK. Funtion for create correct name for value has activated')
        list_of_likes = [element['likes']['count'] for element in list] # формируется список, элементами которого являются показатели количества лайков с каждой фотографии
        help_name = name # создается переменная для грамотного удаления
        list_of_likes.remove(help_name) # Происходит удаления значения из списка и тем самым, если такое же значение будет, то количество лайков на фотографии не уникально
        if name in list_of_likes: # Проверка условия выше
            logging.info('VK. The value has been generated and date and to name')
            return f"{name}.{date}.jpg" # Если имя не уникально, то добавляется дата
        logging.info('VK. The value has been generated without date')
        return f"{name}.jpg" 
        
        
        
            
        
        
        
            
        
        
        

        
        
        
        
        
        

