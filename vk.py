import configparser
import vk_api
import json
from datetime import datetime
import os
import os.path
import time

config = configparser.ConfigParser()
config.read('config.ini')

base_dir = os.getcwd()
json_files_directory = os.path.join(base_dir, 'json_files')

if not os.path.exists(json_files_directory):
    os.makedirs(json_files_directory)


vk_max_count_images = config['VK']['max_count_images']

vk_token = config['VK']['token']

vk_session = vk_api.VkApi(token=vk_token, api_version='5.131')
vk = vk_session.get_api()
def search(size, list):
    return [element for element in list if element['type'] == size]

def get_filename(photos_list, likes):
    if len(photos_list) > 0:
        for item in photos_list:
            if f"{likes}.jpg" in item:
                today = datetime.today().strftime('%Y-%m-%d')
                return f"{likes}_{today}.jpg"
    return f"{likes}.jpg"


def get_vk_images(vk_id, max_count=vk_max_count_images, album='profile') -> list:
    data = vk.photos.get(owner_id=vk_id, album_id=album,
                         extended='1', count=max_count)
    photos_list = []
    info = []

    for photo in data['items']:
        photos_dict = {}
        likes = photo['likes']['count']
        file_name = get_filename(photos_list, likes)
        for size in ['w', 'z', 'y', 'r', 'q', 'p', 'o', 'x', 'm', 's']:
            search_size = search(size, photo['sizes'])
            if len(search_size) > 0:
                photos_dict[file_name] = search_size[0]['url']
                info.append({'file_name': file_name, 'size': size})
                break
        photos_list.append(photos_dict)
    jsonfile_path = os.path.join(
        json_files_directory, f"info_id{vk_id}_{album}_{str(time.time())}.json")
    with open(jsonfile_path, 'w') as json_file:
        json.dump(info, fp=json_file, ensure_ascii=False, indent=4)
    return photos_list
