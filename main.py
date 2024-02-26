import requests
import json
import configparser
import vk_api
from tqdm import tqdm
import time
import os

json_files_directory = 'json_files'
if not os.path.exists(json_files_directory):
    os.makedirs(json_files_directory)

config = configparser.ConfigParser()
config.read('config.ini')
vk_max_count_images = config['VK']['max_count_images']

vk_id = input('Введите id vk: ')
yandex_token = input('Введите yandex token: ')

vk_token = config['VK']['token']


class YandexApi:
    url_base = 'https://cloud-api.yandex.net'
        
    yandex_headers = {
        'Authorization': f'OAuth {yandex_token}'
    }

    def __init__(self, token):
        self.token = token
    
    def get_info(self, url_base=url_base, headers=yandex_headers):
        url_get_info = f'{url_base}/v1/disk/'
        response = requests.get(url_get_info, headers=headers)
        print(response.json())

    def _create_folder(self, folder_name, headers=yandex_headers, url_base=url_base):
        url_create_dir = f'{url_base}/v1/disk/resources'
        params = {
            'path': f'{folder_name}'
            }
        response = requests.put(url_create_dir,
                         params=params,
                         headers=headers)

    def upload_files(self, vk_id, photos_list, url_base=url_base, headers=yandex_headers):
        self._create_folder(vk_id)
        url_upload = f'{url_base}/v1/disk/resources/upload'
        for photo in tqdm(photos_list):
            for image_name, image_url in photo.items():
                response = requests.get(image_url)
                image_name = f'{image_name}.jpg'
                params = {
                        'path': f'{vk_id}/{image_name}',
                        'url': image_url
                        }
                
                response = requests.post(url_upload,
                                        params=params,
                                        headers=headers)
                print(response.status_code)
        

vk_session = vk_api.VkApi(token=vk_token, api_version = '5.131')
vk = vk_session.get_api()
yandex_api = YandexApi(token=yandex_token)


def search(size, list):
    return [element for element in list if element['type'] == size]

def get_vk_images(max_count=vk_max_count_images, owner_id=vk_id, album='profile') -> list:
    data = vk.photos.get(owner_id = owner_id, album_id = album, extended = '1', count = max_count)
    photos_list = []
    info = []

    for photo in data['items']:
        photos_dict = {}
        likes = photo['likes']['count']
        for size in ['w','z','y','r','q','p','o','x','m','s']:
            search_size = search(size, photo['sizes'])
            if len(search_size) > 0:
                photos_dict[likes] = search_size[0]['url']
                info.append({'file_name':f"{likes}.jpg", 'size':size})
                break

        photos_list.append(photos_dict)
    with open(f'json_files\info_id{vk_id}_{album}_{str(time.time())}.json', 'w') as json_file:
        json.dump(info, fp=json_file, ensure_ascii=False, indent=4)
    return photos_list


if vk_id.isdigit()==True:
    #Получение аваторок
    yandex_api.upload_files(vk_id=vk_id, photos_list=get_vk_images())

    #Получение сохраненных фотографий (часто не работает, т.к. альбом закрыт)
    #yandex_api.upload_files(vk_id=vk_id, photos_list=get_vk_images(album='saved'))

    #Получение фото со стены
    yandex_api.upload_files(vk_id=vk_id, photos_list=get_vk_images(album='wall'))

else:
    print('id VK должен состоять только из цифр!')

#Информация об измененном Я.Диске
yandex_api.get_info()