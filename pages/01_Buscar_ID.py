import streamlit as st
import components.show as show
import components.authenticate as authenticate

authenticate.set_st_state_vars()

# Page start here
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False


if st.session_state["authenticated"]:
    email = st.session_state['email_user']
    coach_name = st.session_state['user_name']
    with st.sidebar:
            st.write(f'Ahoj, {coach_name}!')
            st.divider()
            authenticate.button_logout()

    show.show_id()

else:
    st.write("# Please Log In")
    # st.write(st.session_state)
    with st.sidebar:
        st.divider()
        authenticate.button_login()

