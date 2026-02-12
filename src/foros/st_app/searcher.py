import streamlit as st
from datetime import datetime
from src.foros.pipeline.extract import get_nip, get_regon
from src.foros.utils.helpers import nip_checksum, regon_checksum
import re

def run():

    st.set_page_config(
        page_title='VAT payers searcher - Foros',
        layout='wide',
        initial_sidebar_state='collapsed'
)
    
    today = datetime.strptime(datetime.now().strftime(f'%Y-%m-%d'), '%Y-%m-%d').date()
    search_timestamp = datetime.now().strftime(f'%Y-%m-%d %H:%M:%S')

    tab1, tab2, tab3 = st.tabs(['VAT', 'In process', 'Search history'])
    with tab1: 
        # Tworzenie sidebar-u do wyszkiwania danych
        nip_val = st.text_input('NIP number', label_visibility='visible')
        regon_val = st.text_input('REGON number', label_visibility='visible')
        date_val = st.date_input('Record date', label_visibility='visible', value=None, max_value='today')
        search = st.button('Search', width='stretch')

        if 'search_history' not in st.session_state:
            st.session_state.search_history = []
        if 'search_id' not in st.session_state:
            st.session_state.search_id = 1

        # Instrukcje warunkowa obsługująca funkcjonowanie aplikacji do wyszukiwania VAT-owców
        if not nip_val and not regon_val and not date_val:
            if search:
                st.info('Find NIP/REGON for given date.')
            return

        if (nip_val or regon_val) and not date_val:
            if search:
                st.info('Choose date to find VAT payers.')
            return

        if date_val and date_val <= today and not nip_val and not regon_val:
            if search:
                st.info('Write NIP/REGON to search.')
            return

        if nip_val and date_val <= today:
            if search:
                nip = nip_checksum(nip_val)
                name, nip_value, status, regon, address, registration_date, acc_number = get_nip(nip, date_val)

                if name:
                    st.session_state.search_history.append({
                            'Id': st.session_state.search_id,
                            'Name': name,
                            'Nip': nip_value, 
                            'Status': status, 
                            'Regon': regon,
                            'Search timestamp': search_timestamp
                    })
                    st.session_state.search_id += 1

                data_labels_upper_row = {
                    'Name': name.title(),
                    'Status': status.title(),
                    'NIP': nip_value,
                    'REGON': regon
                    }
                data_labels_lower_row = {
                    'Registration date': registration_date,
                    'Account number': acc_number[0] if acc_number else '-',
                    'Address': address.title()
                    }

                if name:
                    st.subheader('Search results:')
                    st.divider()
                    cols_upper = st.columns(4)
                    cols_lower = st.columns(4)
                    for col, (key, value) in zip(cols_upper, data_labels_upper_row.items()):
                        col.markdown(f'**{key}:** \n\n{value}')
                    for col, (key, value) in zip(cols_lower, data_labels_lower_row.items()):
                        col.markdown(f'**{key}:** \n\n{value}')

        elif regon_val and date_val <= today:
            if search:
                regon = regon_checksum(regon_val)
                name, nip_value, status, regon_value, adres, registration_date, acc_number = get_regon(regon, date_val)
                
                if name:
                    st.session_state.search_history.append({
                            'Id': st.session_state.search_id,
                            'Name': name.title(),
                            'Nip': nip_value, 
                            'Status': 'Active' if status == 'Czynny' else 'Not active',
                            'Regon': regon,
                            'Search timestamp': search_timestamp
                    })
                    st.session_state.search_id += 1
                
                data_labels_upper_row = {
                    'Name': name.title(),
                    'Status': status.title(),
                    'NIP': nip_value,
                    'REGON': regon_value
                    }
                data_labels_lower_row = {
                    'Registration date': registration_date,
                    'Account number': acc_number[0] if acc_number else '-',
                    'Address': address.title()
                    }

                st.divider()
                if name:
                    st.subheader('Search results:')
                    cols_upper = st.columns(4)
                    cols_lower = st.columns(4)
                    for col, (key, value) in zip(cols_upper, data_labels_upper_row.items()):
                        col.markdown(f'**{key}:** \n\n{value}')
                    for col, (key, value) in zip(cols_lower, data_labels_lower_row.items()):
                        col.markdown(f'**{key}:** \n\n{value}')
        else:
            return

    with tab2:
        st.info('Sanction lits - under construction 🚧')

    with tab3:
        clear_search = st.button('Clear search history', width='stretch')
        if clear_search:
            st.session_state.search_history.clear()
            st.session_state.search_id = 1

        if st.session_state.search_history:
            st.subheader('Search history:')
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