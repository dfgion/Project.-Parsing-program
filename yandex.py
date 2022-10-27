import logging
import requests
from vk import VKUser

class YandexUser:
    """Действия с API Yandex"""
    def __init__(self, vk_id, token, vk_token):
        self.token = token
        self.vk_id = vk_id
        self.token_vk = vk_token

    def headers(self):
        headers = {'Content-Type': 'application/json',
                   'Authorization': f'OAuth {self.token}'}
        return headers

    def function_upload(self, element_path, url):
        try:
            logging.info('YANDEX. Url has received and will be use for upload to disk')
            link_to_upload = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
            path = 'course_project/' + element_path
            params = {'path': path,
                      'url': url}
            logging.info('YANDEX. Params for request have generate')
            response = requests.post(link_to_upload, params = params, headers = self.headers())
            if response.status_code == 202:
                logging.info('YANDEX. Code 202, request has sent')
        except Exception: 
            logging.error('YANDEX. Failed upload to disk. Incorrect data.', exc_info = True)

    def get_photo_to_upload(self):
        try:
            logging.info('Program was start to upload the photos on disk')
            help_vk=VKUser(self.vk_id, self.token_vk)
            logging.info('YANDEX. Process for receive the url of photos has activated')
            for element in help_vk.dict_to_yandex():
                self.function_upload(element_path=element['file_name'], url = element['url'])
        except Exception:
            logging.error('YANDEX. Failed received data or dictionary.', exc_info = True)
            