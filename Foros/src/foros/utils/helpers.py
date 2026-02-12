'''Skrypt zawierający funkcję pomocne w bezawaryjnym działaniu pipeline-u.'''

import re
import streamlit as st

def nip_suma_kontrolna(nip: str):
    '''Funkcja sprawdzająca czy NIP podany przez uytkownika jest poprawny'''
    nip = re.sub('[^0-9]', '', nip)
    if (len(nip) != 10 and (int(nip[0])*6 + int(nip[1])*5 + int(nip[2])*7 + int(nip[3])*2 + int(nip[4])*3 + int(nip[5])*4 + int(nip[6])*5 + int(nip[7])*6 + int(nip[8])*7)%11 != int(nip[-1])):
        st.warning('Brak danych do wyświetlenia. Prawdopodobnie błędny NIP lub zła data. Popraw dane.', icon='🚨') 
    else: 
        return nip
        
def regon_suma_kontrolna(regon: str):
    '''Funkcja sprawdzająca czy REGON podany przez uytkownika jest poprawny'''
    regon = re.sub('[^0-9]', '', regon)
    if (len(regon) != 9 and (int(regon[0])*8 + int(regon[1])*9 + int(regon[2])*2 + int(regon[3])*3 + int(regon[4])*4 + int(regon[5])*5 + int(regon[6])*6 + int(regon[7])*7)%11 != int(regon[-1])) and (len(regon) != 14 and (int(regon[0])*2 + int(regon[1])*4 + int(regon[2])*8 + int(regon[3])*5 + int(regon[4])*0 + int(regon[5])*9 + int(regon[6])*7 + int(regon[7])*3 + int(regon[7])*6 + int(regon[7])*1 + int(regon[7])*2 + int(regon[7])*4 + int(regon[7])*8)%11 != int(regon[-1])):
        st.warning('Brak danych do wyświetlenia. Prawdopodobnie błędny REGON lub zła data. Popraw dane.', icon='🚨')
    else:
        return regon