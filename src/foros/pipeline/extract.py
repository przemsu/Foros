'''Skrypt zawierający funkcję odpytujące API o wskazane identyfikatory.'''

import requests

def get_nip(nip_user_input: str, data: str):
    '''Funkcja pobierająca dane o pojedynczym podmiocie identyfikowanym za pomocą numeru NIP'''
      
    url = f'https://wl-api.mf.gov.pl/api/search/nip/{nip_user_input}?date={data}'

    response = requests.get(url)
    resp_code = response.status_code

    if resp_code != 200:
        return None, None, None, None, None, None, None
    
    result = response.json().get('result', {})
    subject = result.get('subject', {})

    nazwa = subject.get('name')
    nip_value = subject.get('nip')
    status = subject.get('statusVat')
    regon = subject.get('regon')
    adres = subject.get('residenceAddress')
    data_rejestracji = subject.get('registrationLegalDate')
    numer_konta = subject.get('accountNumbers')

    return nazwa, nip_value, status, regon, adres, data_rejestracji, numer_konta

def get_regon(regon_user_input: str, data: str):
    '''Funkcja pobierająca dane o pojedynczym podmiocie identyfikowanym za pomocą numeru REGON'''

    url = f'https://wl-api.mf.gov.pl/api/search/regon/{regon_user_input}?date={data}'

    response = requests.get(url)
    resp_code = response.status_code

    if resp_code != 200:
        return None, None, None, None, None, None, None
    
    result = response.json().get('result', {})
    subject = result.get('subject')
    
    nazwa = subject.get('name')
    nip_value = subject.get('nip')
    status = subject.get('statusVat')
    regon = subject.get('regon')
    adres = subject.get('residenceAddress')
    data_rejestracji = subject.get('registrationLegalDate')
    numer_konta = subject.get('accountNumbers')

    return nazwa, nip_value, status, regon, adres, data_rejestracji, numer_konta