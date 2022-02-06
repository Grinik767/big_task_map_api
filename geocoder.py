import requests


class Geocoder:
    def __init__(self, search):
        self.search = search
        self.response = None
        self.geocoder_request()

    def geocoder_request(self):
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": self.search,
            "format": "json"}
        response = requests.get(geocoder_api_server, params=geocoder_params)
        if response:
            self.response = response

    def get_coords_from_json(self):
        json_resp = self.response.json()
        coords = json_resp["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]['pos']
        return ','.join(coords.split())

    def get_address_from_json(self):
        json_resp = self.response.json()
        address = json_resp["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]['metaDataProperty'][
            'GeocoderMetaData']['AddressDetails']['Country']['AddressLine']
        return address


if __name__ == '__main__':
    geo = Geocoder("Тюмень, Московский тракт 88")
    print(geo.get_coords_from_json())
