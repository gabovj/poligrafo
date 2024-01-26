import streamlit as st
from pymongo import MongoClient
import time
import components.show as show  
import components.authenticate as authenticate

st.set_page_config(
    page_title="Aviso de privacidad", 
    page_icon="favicon.ico", 
    # layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Report a bug': "mailto:gabriel.vapp@gmail.com",
        'About': "# Centro Especializado en Poligrafía e investigación Estratégica!"
    }
    )

# Use your MongoDB Atlas connection string here
mongo_uri = st.secrets["mongo_uri"]
client = MongoClient(mongo_uri)
db = client["blanca"]
collection = db["poligrafia"]

authenticate.set_st_state_vars()

# Page start here
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False


if st.session_state["authenticated"]:
    with st.sidebar:
            st.divider()
            authenticate.button_logout()
    if (st.session_state["authenticated"] and "Superuser" in st.session_state["user_cognito_groups"]):

        # Initialize the existing_data variable
        existing_data = None

        # Input for 'folio_imprimir'
        folio_imprimir = st.text_input(':orange[Folio]')
        if folio_imprimir:
            existing_data = collection.find_one({"folio": folio_imprimir})

        # Check if existing_data is not None before proceeding
        if existing_data:
            # Form for company and poligraphist details
            with st.form("empresa_y_clave"):
                name_doc = existing_data.get("name", "")
                st.write(f'Nombre: :orange[{name_doc}]')
                col1, col2 = st.columns(2)
                with col1:
                    hiring_company = st.text_input('Empresa a presentar los resultados', value=existing_data.get('hiring_company', ''))
                with col2:
                    key_poligraphist = st.text_input('Clave poligrafista', value=existing_data.get('key_poligraphist', ''))

                # Submit button for the form
                submit_empresa_y_clave = st.form_submit_button(':orange[Generar documento]')

            # Handling form submission
            if submit_empresa_y_clave:
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
            else:
                if folio_imprimir:
                    st.warning("No data found for the provided folio.")

        # Download button
        if st.session_state.get('ready_to_download', False):
            st.download_button(
                label="Descargar Documento",
                data=st.session_state['docx_file'],
                file_name=f"{name_doc}" + "_ap.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
    else:
        if st.session_state["authenticated"]:
            st.write("### No tienes acceso a esta pagina.")
            st.write("### Ve a 'Llenar Cuestionario' :arrow_left:")
else:
    st.write("# Por favor inicia sesión")
    # st.write(st.session_state)
    with st.sidebar:
        st.divider()
        authenticate.button_login()