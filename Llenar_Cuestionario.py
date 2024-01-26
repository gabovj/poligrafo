import streamlit as st
import components.forms as preguntas
import components.authenticate as authenticate

st.set_page_config(
    page_title="Home", 
    page_icon="favicon.ico", 
    # layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Report a bug': "mailto:gabriel.vapp@gmail.com",
        'About': "# Centro Especializado en Poligrafía e investigación Estratégica!"
    }
    )

authenticate.set_st_state_vars()

# Page start here
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False


if st.session_state["authenticated"]:
    email = st.session_state['email_user']
    # coach_name = st.session_state['user_name']
    with st.sidebar:
            # st.write(f'Ahoj, {coach_name}!')
            st.divider()
            authenticate.button_logout()

    st.markdown('Hola, si ya tienes un folio asignado ingresalo aquí')
    preguntas.set_session_state_folio()
    st.markdown('O si quieres iniciar un nuevo cuestionario haz clic en el botón')
    preguntas.start_new_questionnaire()
    preguntas.print_folio_session_state()

    with st.expander('#### :orange[Datos Generales]'):
        preguntas.datos_generales()
    with st.expander('#### :orange[Datos Laborales]'):
        preguntas.datos_laborales()
    with st.expander('#### :orange[Historia Medica]'):
        preguntas.historia_medica()
    with st.expander('#### :orange[Aspectos Emocionales]'):
        preguntas.aspectos_emocionales()
    with st.expander('#### :orange[Aspectos Económicos]'):
        preguntas.aspectos_economicos()
    with st.expander('#### :orange[Discusión y Desarrollo]'):
        preguntas.discusion_desarrollo()
else:
    st.write("# Por favor inicia sesión")
    # st.write(st.session_state)
    with st.sidebar:
        st.divider()
        authenticate.button_login()