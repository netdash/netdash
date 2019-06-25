import requests


def get_devices(base_url):
    return requests.get(f'{base_url}/dcim/devices/').json()['results']


def get_device(base_url, pk):
    return requests.get(f'{base_url}/dcim/devices/{pk}/').json()
