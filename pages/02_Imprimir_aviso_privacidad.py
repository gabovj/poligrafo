# import streamlit as st
# from pymongo import MongoClient
# import time
# import components.show as show

# # Use your MongoDB Atlas connection string here
# mongo_uri = st.secrets["mongo_uri"]
# # Create a MongoClient using the provided URI
# client = MongoClient(mongo_uri)
# # Specify the database and collection
# db = client["blanca"]
# collection = db["poligrafia"]

# with st.form("empresa_y_clave"):
#     folio_imprimir = st.text_input(':orange[Folio]')
#     existing_data = collection.find_one({"folio": folio_imprimir})
#     col1, col2 = st.columns(2)
#     with col1:
#         hiring_company = st.text_input('Empresa a presentar los resultados')
#     with col2:
#         key_poligraphist = st.text_input('Clave poligrafista')
#     submit_empresa_y_clave = st.form_submit_button(':orange[Descargar documento]')
#     if submit_empresa_y_clave:
#         empresa_y_clave ={
#             'hiring_company': hiring_company,
#             'key_poligraphist': key_poligraphist,
#         }
#         try:
#             # Update the data in MongoDB
#             collection.update_one({"folio": folio_imprimir}, {"$set": empresa_y_clave}, upsert=True)
#             with st.spinner('Generando Documento'):
#                 time.sleep(5)
#             st.success('Done!')
#         except Exception as e:
#             st.error(f"An error occurred: {e}")

import streamlit as st
from pymongo import MongoClient
import time
import components.show as show  # Assuming create_docx is in this module

# Use your MongoDB Atlas connection string here
mongo_uri = st.secrets["mongo_uri"]
client = MongoClient(mongo_uri)
db = client["blanca"]
collection = db["poligrafia"]

# Initialize the existing_data variable
existing_data = None

# Input for 'folio_imprimir'
folio_imprimir = st.text_input(':orange[Folio]')
if folio_imprimir:
    existing_data = collection.find_one({"folio": folio_imprimir})

# Form for company and poligraphist details
with st.form("empresa_y_clave"):
    col1, col2 = st.columns(2)
    with col1:
        hiring_company = st.text_input('Empresa a presentar los resultados', value=existing_data.get('hiring_company', '') if existing_data else '')
    with col2:
        key_poligraphist = st.text_input('Clave poligrafista', value=existing_data.get('key_poligraphist', '') if existing_data else '')

    # Submit button for the form
    submit_empresa_y_clave = st.form_submit_button(':orange[Descargar documento]')

# Handling form submission
if submit_empresa_y_clave and existing_data:
    empresa_y_clave = {
        'hiring_company': hiring_company,
        'key_poligraphist': key_poligraphist,
    }
    try:
        collection.update_one({"folio": folio_imprimir}, {"$set": empresa_y_clave}, upsert=True)
        updated_data = collection.find_one({"folio": folio_imprimir})  # Fetch updated data
        with st.spinner('Generando Documento'):
            docx_file = show.create_docx(updated_data)  # Use the updated data here
            docx_file.seek(0)
            st.success('Documento generado con éxito!')
            st.session_state['ready_to_download'] = True
            st.session_state['docx_file'] = docx_file
    except Exception as e:
        st.error(f"Ocurrió un error: {e}")

# Download button
if st.session_state.get('ready_to_download', False):
    st.download_button(
        label="Descargar Documento",
        data=st.session_state['docx_file'],
        file_name="custom_document.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
