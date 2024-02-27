from yandex import *
from vk import *

vk_id = input('Введите id vk: ')
yandex_token = input('Введите yandex token: ')
yandex_api = YandexApi(token=yandex_token)


if vk_id.isdigit() == True:
    # Получение аватарок
    yandex_api.upload_files(vk_id=vk_id, photos_list=get_vk_images(vk_id))

    # Получение сохраненных фотографий (часто не работает, т.к. альбом закрыт)
    # yandex_api.upload_files(vk_id=vk_id, photos_list=get_vk_images(album='saved'))

    # Получение фото со стены
    # yandex_api.upload_files(
    #    vk_id=vk_id, photos_list=get_vk_images(album='wall'))

else:
    print('id VK должен состоять только из цифр!')

# Информация об измененном Я.Диске
yandex_api.get_info()
