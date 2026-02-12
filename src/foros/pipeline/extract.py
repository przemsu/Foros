import requests

def get_nip(nip_user_input: str, data: str):
    '''GET API call for given ids - NIP'''
      
    url = f'https://wl-api.mf.gov.pl/api/search/nip/{nip_user_input}?date={data}'

    response = requests.get(url)
    resp_code = response.status_code

    if resp_code != 200:
        return None, None, None, None, None, None, None
    
    result = response.json().get('result', {})
    subject = result.get('subject', {})

    name = subject.get('name')
    nip_value = subject.get('nip')
    status = subject.get('statusVat')
    regon = subject.get('regon')
    adres = subject.get('residenceAddress')
    registration_date = subject.get('registrationLegalDate')
    acc_number = subject.get('accountNumbers')

    return name, nip_value, status, regon, adres, registration_date, acc_number

def get_regon(regon_user_input: str, data: str):
    '''GET API call for given ids - REGON'''

    url = f'https://wl-api.mf.gov.pl/api/search/regon/{regon_user_input}?date={data}'

    response = requests.get(url)
    resp_code = response.status_code

    if resp_code != 200:
        return None, None, None, None, None, None, None
    
    result = response.json().get('result', {})
    subject = result.get('subject')
    
    name = subject.get('name')
    nip_value = subject.get('nip')
    status = subject.get('statusVat')
    regon = subject.get('regon')
    address = subject.get('residenceAddress')
    registration_date = subject.get('registrationLegalDate')
    acc_number = subject.get('accountNumbers')

    return name, nip_value, status, regon, address, registration_date, acc_number