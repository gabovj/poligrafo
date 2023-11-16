import streamlit as st
import components.forms as preguntas

st.set_page_config(
    page_title="Home", 
    page_icon="🆙", 
    # layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Report a bug': "mailto:xxx@xxx.com",
        'About': "# Centro Especializado en Poligrafía e investigación Estratégica!"
    }
    )


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
