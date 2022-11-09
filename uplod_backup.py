import requests
import time
import json
from tqdm import tqdm
class VK_user:
    def get_info_photo(self):
        self.list_size = ['w', 'z', 'y', 'r', 'q', 'p', 'o', 'x', 'm', 's']
        id_vk = input("Введите id пользователя VK: ")
        url = 'https://api.vk.com/method/photos.get'
        access_token = '1e4b074b1e4b074b1e4b074b781d5a2ea511e4b1e4b074b7d1e2ca05ab7fe5b4fd3ef12'  # сервисный токен VK
        album_id = 'wall'
        extended = '1'
        photo_sizes = '1'
        params = {'access_token': access_token, 'owner_id': id_vk, 'album_id': album_id, 'extended': extended,
                  'photo_sizes': photo_sizes, 'v': 5.131}
        self.res = requests.get(url, params=params).json()
        return self.res

    def enter_data(self):
        while True:
            count_photo = int(input('Введите количестов фотографий для записи на Яндекс Диск: '))
            if count_photo <= self.res['response']['count']:
                break
            print(f'В альбоме пользователя содержится всего {self.res["response"]["count"]} фото')
        return count_photo

    def create_list_info(self):
        self.get_info_photo()
        photo_info = []
        photo_list_names = []
        photos = self.res['response']['items']
        for i in range(self.enter_data()):
            photo_name = str(photos[i]['likes']['count']) + '.jpg'
            photo_list_names.append(photo_name)  # формирование списка имен фотографий, полученных из VK для загрузки
            ph_s = photos[i]['sizes']  # формирование списка значений по ключу "sizes", содержащего размеры, типы, url фото
            photo_list = []
            for i in range(len(ph_s)):
                ph_w = ph_s[i]['type']
                photo_list.append(ph_w)                  # формирование списка типо-размеров фотографий
                for i in range(10):                      # 10 - количество размерного ряда фотографий в VK ("type")
                    if self.list_size[i] in photo_list:  # определение индекса максимального значание в списке типо-размеров
                        photo_id = photo_list.index(self.list_size[i])
                        break
            photo_url = ph_s[photo_id]['url']
            size = ph_s[photo_id]['type']
            # ======================== формирование выходных данных =====================================
            photo_info.append(dict({'file_name': photo_name, 'size': size, 'url': photo_url}))
            for i in range(len(photo_list_names) - 1):  # к одноименному фото добавляем его дату загрузки в альбом
                if photo_info[i]['file_name'] in photo_list_names[i + 1:]:
                    photo_info[i]['file_name'] += '_' + time.strftime("%d%b%Y", time.localtime(
                        self.res['response']['items'][i]['date']))

        return photo_info
class YaUploud:
    def uploud_photo(self):
        token = input('Файлы для загрузки подготовлены, введите токен для доступа к Яндекс.Диск: ')
        # token = '................'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {token}'
        }
        url_folder = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {"path": '/PD-66'}
        response = requests.put(url_folder, headers=headers, params=params)
        if response.status_code == 201 or response.status_code == 409:
            print("<<< Директория создана >>>\nНачинаем загрузку: ")
        else:
            print("Ошибка создания директории")
        url_upload = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        for i in tqdm(range(len(photo_info))):
            path = str(f'/PD-66/{photo_info[i]["file_name"]}')
            url = photo_info[i]["url"]
            params = {"url": url, "path": path, "overwrite": "true"}
            response = requests.post(url_upload, headers=headers, params=params)
            time.sleep(1)
        print("<<< Файлы успешно загружены >>>")
        #pprint(photo_info)
        with open('data.json', 'w') as outfile:  # запись выходного файла
            json.dump(photo_info, outfile, indent=4)

if __name__ == '__main__':
    user = VK_user()
    photo_info = user.create_list_info()
    user = YaUploud()
    user.uploud_photo()