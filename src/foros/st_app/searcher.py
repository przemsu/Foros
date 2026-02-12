'''Skrypt budujący dashboard do wyświelania danych z API VAT.'''

import streamlit as st
from datetime import datetime
from src.foros.pipeline.extract import get_nip, get_regon
from src.foros.utils.helpers import nip_suma_kontrolna, regon_suma_kontrolna
import re

def run():

    st.set_page_config(
        page_title='Wyszukiwarka VAT - Foros',
        layout='wide',
        initial_sidebar_state='collapsed'
)
    
    today = datetime.strptime(datetime.now().strftime(f'%Y-%m-%d'), '%Y-%m-%d').date()
    search_timestamp = datetime.now().strftime(f'%Y-%m-%d %H:%M:%S')

    tab1, tab2, tab3 = st.tabs(['VAT', 'In process', 'Historia wyszukiwania'])
    with tab1: 
        # Tworzenie sidebar-u do wyszkiwania danych
        nip_val = st.text_input('Numer NIP', label_visibility='visible')
        regon_val = st.text_input('Numer REGON', label_visibility='visible')
        date_val = st.date_input('Data sprawdzenia', label_visibility='visible', value=None, max_value='today')
        search = st.button('Szukaj', width='stretch')

        if 'search_history' not in st.session_state:
            st.session_state.search_history = []
        if 'search_id' not in st.session_state:
            st.session_state.search_id = 1

        # Instrukcje warunkowa obsługująca funkcjonowanie aplikacji do wyszukiwania VAT-owców
        if not nip_val and not regon_val and not date_val:
            if search:
                st.info('Wpisz numer NIP lub REGON i wybierz datę aby wyszukać.')
            return

        if (nip_val or regon_val) and not date_val:
            if search:
                st.info('Wybierz datę aby sprawdzić płatnika VAT.')
            return

        if date_val and date_val <= today and not nip_val and not regon_val:
            if search:
                st.info('Wpisz NIP lub REGON aby wyszukać.')
            return

        if nip_val and date_val <= today:
            if search:
                nip = nip_suma_kontrolna(nip_val)
                nazwa, nip_value, status, regon, adres, data_rejestracji, numer_konta = get_nip(nip, date_val)

                if nazwa:
                    st.session_state.search_history.append({
                            'Id': st.session_state.search_id,
                            'Nazwa': nazwa,
                            'Nip': nip_value, 
                            'Status': status, 
                            'Regon': regon,
                            'Search timestamp': search_timestamp
                    })
                    st.session_state.search_id += 1

                data_labels_upper_row = {
                    'Imię & nazwisko': nazwa.title(),
                    'Status': status.title(),
                    'NIP': nip_value,
                    'REGON': regon
                    }
                data_labels_lower_row = {
                    'Data rejestracji': data_rejestracji,
                    'Numer konta': numer_konta[0] if numer_konta else '-',
                    'Adres': adres.title()
                    }

                if nazwa:
                    st.subheader('Wyniki wyszukiwania:')
                    st.divider()
                    cols_upper = st.columns(4)
                    cols_lower = st.columns(4)
                    for col, (key, value) in zip(cols_upper, data_labels_upper_row.items()):
                        col.markdown(f'**{key}:** \n\n{value}')
                    for col, (key, value) in zip(cols_lower, data_labels_lower_row.items()):
                        col.markdown(f'**{key}:** \n\n{value}')

        elif regon_val and date_val <= today:
            if search:
                regon = regon_suma_kontrolna(regon_val)
                nazwa, nip_value, status, regon_value, adres, data_rejestracji, numer_konta = get_regon(regon, date_val)
                
                if nazwa:
                    st.session_state.search_history.append({
                            'Id': st.session_state.search_id,
                            'Nazwa': nazwa.title(),
                            'Nip': nip_value, 
                            'Status': status.title(), 
                            'Regon': regon,
                            'Search timestamp': search_timestamp
                    })
                    st.session_state.search_id += 1
                
                data_labels_upper_row = {
                    'Imię & nazwisko': nazwa.title(),
                    'Status': status.title(),
                    'NIP': nip_value,
                    'REGON': regon_value
                    }
                data_labels_lower_row = {
                    'Data rejestracji': data_rejestracji,
                    'Numer konta': numer_konta[0] if numer_konta else '-',
                    'Adres': adres.title()
                    }

                st.divider()
                if nazwa:
                    st.subheader('Wyniki wyszukiwania:')
                    cols_upper = st.columns(4)
                    cols_lower = st.columns(4)
                    for col, (key, value) in zip(cols_upper, data_labels_upper_row.items()):
                        col.markdown(f'**{key}:** \n\n{value}')
                    for col, (key, value) in zip(cols_lower, data_labels_lower_row.items()):
                        col.markdown(f'**{key}:** \n\n{value}')
        else:
            return

    with tab2:
        st.info('Listy sankcyjne - strona w budowie 🚧')

    with tab3:
        clear_search = st.button('Wyczyść historię wyszukiwania', width='stretch')
        if clear_search:
            st.session_state.search_history.clear()
            st.session_state.search_id = 1

        if st.session_state.search_history:
            st.subheader('Historia wyszukiwania:')
            st.divider()
            cols_header = st.columns([0.025, 0.2, 0.2, 0.2, 0.2, 0.2])
            cols_data = st.columns([0.025, 0.2, 0.2, 0.2, 0.2, 0.2])
            for i in st.session_state.search_history:
                for col, key in zip(cols_header, i.keys()):
                    col.markdown(f'**{key}**')
                break
            for i in st.session_state.search_history:
                for col, value in zip(cols_data, i.values()):
                    col.markdown(f'\n\n {value}')