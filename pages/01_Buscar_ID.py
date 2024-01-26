import streamlit as st
import components.show as show
import components.authenticate as authenticate

st.set_page_config(
    page_title="Buscar ID", 
    page_icon="favicon.ico", 
    # layout="wide",
    initial_sidebar_state="expanded",
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
    with st.sidebar:
            st.divider()
            authenticate.button_logout()
    if (st.session_state["authenticated"] and "Superuser" in st.session_state["user_cognito_groups"]):
        show.show_id()
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

