from tqdm import tqdm
import requests


class YandexApi:
    url_base = 'https://cloud-api.yandex.net'

    def __init__(self, token):
        self.yandex_headers = {
        'Authorization': f'OAuth {token}'
    }


    def get_info(self):
        url_get_info = f'{self.url_base}/v1/disk/'
        response = requests.get(url_get_info, headers=self.yandex_headers)
        print(response.json())

    def _create_folder(self, folder_name):
        url_create_dir = f'{self.url_base}/v1/disk/resources'
        params = {
            'path': f'{folder_name}'
        }
        response = requests.put(url_create_dir,
                                params=params,
                                headers=self.yandex_headers)

    def upload_files(self, vk_id, photos_list):
        self._create_folder(vk_id)
        url_upload = f'{self.url_base}/v1/disk/resources/upload'
        for photo in tqdm(photos_list):
            for image_name, image_url in photo.items():
                response = requests.get(image_url)
                image_name = f'{image_name}'
                params = {
                    'path': f'{vk_id}/{image_name}',
                    'url': image_url
                }
                response = requests.post(url_upload,
                                         params=params,
                                         headers=self.yandex_headers)
                # print(response.status_code)
