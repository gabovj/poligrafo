import streamlit as st
from datetime import datetime
from pymongo import MongoClient
import uuid
import logging

# Use your MongoDB Atlas connection string here
mongo_uri = st.secrets["mongo_uri"]
# Create a MongoClient using the provided URI
client = MongoClient(mongo_uri)
# Specify the database and collection
db = client["blanca"]
collection = db["poligrafia"]

# Set up basic configuration for logging
logging.basicConfig(
    level=logging.INFO,
    filename='app.log',
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def start_new_questionnaire():
    start_button = st.button(':orange[Iniciar NUEVO cuestionario]')
    if start_button:
        folio = str(uuid.uuid4())

        existing_folio = collection.find_one({'folio': folio})
        if existing_folio is not None:
            logging.warning(f'Duplicate folio detected: {folio}')
            st.error("Duplicate folio detected. Please try again.")
            return None

        try:
            start_item = {
                'folio': folio,
                'timestamp': datetime.now()
            }
            collection.insert_one(start_item)
            st.session_state['folio'] = folio
            st.success("Folio generado exitosamente!")
            logging.info(f'New folio generated: {folio}')
            return st.session_state['folio']
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            st.error(f"An error occurred: {e}")
            return None

def set_session_state_folio():
    col1, col2 = st.columns([1.3,.7])
    with col1:
        set_folio = st.text_input('Ingresa tu folio y haz clic en continuar cuestionario')
        
    with col2:
        st.markdown('####')
        set_folio_button = st.button(':orange[Continua cuestionario]')
        if set_folio_button:
            set_folio = set_folio.replace(' ', '').strip()
            st.session_state['folio'] = set_folio

def print_folio_session_state():
    folio_session_state = None
    try:
        folio_session_state = st.session_state['folio']
    except:
        pass
    if folio_session_state is not None:
        st.write(f'Folio: {folio_session_state}')
    else:
        st.error('🚨 NO HAY FOLIO ASIGNADO')

def datos_generales():
    # Try to retrieve existing data for the user
    if 'folio' in st.session_state:
        existing_data = collection.find_one({"folio": st.session_state['folio']})
        # If existing data is found, use it to pre-fill the form; otherwise, use default values
        prefill_data = existing_data if existing_data else {}
        with st.form(key="datos_generales"):
            # st.title(':orange[Datos Generales]')
            folio_from_db = prefill_data.get('folio', '')
            st.write(f':red[folio:] {folio_from_db}')
            col1, col2 = st.columns(2)
            with col1:
                nombre = st.text_input('Nombre', value=prefill_data.get('name', ''), placeholder='Ingresa tu nombre completo')
            with col2:
                lugar_nacimiento = st.text_input('Lugar de Nacimiento', value=prefill_data.get('birth_place', ''), placeholder='Ingresa tu ciudad de nacimiento')
            
            col1, col2, col3 = st.columns(3)
            with col1:
                dob_str = prefill_data.get('dob', None)
                dob_value = datetime.fromisoformat(dob_str) if dob_str else None
                dob = st.date_input("Fecha de Nacimiento", 
                                    format="DD/MM/YYYY", 
                                    value=dob_value, 
                                    min_value=datetime(1920, 1, 1))
                adress_street = st.text_input('Calle', value=prefill_data.get('street_adress', ''),placeholder='Ingresa el nombre de tu calle')
                phone = st.text_input('Teléfono', value=prefill_data.get('phone', ''), placeholder='Ingresa tu número de teléfono')
            with col2:
                edad = st.number_input('Edad',
                                    min_value=0, 
                                    max_value=100, 
                                    value=prefill_data.get('age', 0), 
                                    step=1)
                adress_number = st.text_input('Número', value=prefill_data.get('street_number', ''), placeholder='Ingresa el número de tu casa')
                email = st.text_input('Correo electrónico', value=prefill_data.get('email', ''), placeholder='Ingresa tu email')
            with col3:
                estado_civil = st.text_input('Estado civil', value=prefill_data.get('marriage_status', ''), placeholder='Ingresa tu estado civil actual')
                adress_neighborhood = st.text_input('Colonia', value=prefill_data.get('neighborhood', ''), placeholder='Ingresa el nombre de tu colonia')
                academic_grade = st.text_input('Grado Academico', value=prefill_data.get('academic_grade', ''), placeholder='Último grado de estudios')
            
            col1, col2 = st.columns(2)
            with col1:
                couple_name = st.text_input('Nombre de tu pareja', value=prefill_data.get('couple_name', ''), placeholder='Ingresa el nombre de tu pareja')
            with col2:
                couple_ocupation = st.text_input('Ocupación de tu pareja', value=prefill_data.get('couple_ocupation', ''), placeholder='Ingresa la ocupación de tu pareja')
            
            col1, col2 = st.columns([0.5,1.5])
            with col1:
                num_hijos = st.number_input('Numero de hijos', 
                                        min_value=0, 
                                        max_value=40, 
                                        value=prefill_data.get('children_number', 0), 
                                        step=1)
                dependientes_economicos = st.number_input('Dependientes Económicos', 
                                        min_value=0, 
                                        max_value=40, 
                                        value=prefill_data.get('economic_dependents', 0), 
                                        step=1)
            with col2:
                nombre_hijos = st.text_area('Nombre de hijos', value=prefill_data.get('children_names', ''), placeholder='Ingresa el nombre de tus hijos',)
            col1, col2 = st.columns(2)
            with col1:
                experiencias_poligraficas = st.text_input('Experiencias Poligráficas', value=prefill_data.get('polygraph_experiences', ''))
            with col2:
                resultado_experiencias_poligraficas = st.text_input('Resultado',value=prefill_data.get('polygraph_experiences_results', ''))
            
            submitted_datos_generales = st.form_submit_button(":orange[Guardar Datos Generales]")
            if submitted_datos_generales:
                try:
                    dob_str = dob.isoformat()
                    datos_generales_item ={
                        '$set': {
                        'name': nombre,
                        'birth_place': lugar_nacimiento,
                        'dob': dob_str,
                        'age': edad,
                        'marriage_status': estado_civil,
                        'street_adress': adress_street,
                        'street_number': adress_number,
                        'neighborhood': adress_neighborhood,
                        'phone': phone,
                        'email': email,
                        'academic_grade': academic_grade,
                        'couple_name': couple_name,
                        'couple_ocupation': couple_ocupation,
                        'children_number': num_hijos,
                        'economic_dependents': dependientes_economicos,
                        'children_names': nombre_hijos,
                        'polygraph_experiences': experiencias_poligraficas,
                        'polygraph_experiences_results': resultado_experiencias_poligraficas,
                    }}
                    # Insert the data into MongoDB
                    collection.update_one({"folio": folio_from_db},datos_generales_item)
                    print('data sent')
                    st.success("Datos guardados exitosamente!")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

def datos_laborales():
    # Try to retrieve existing data for the user
    if 'folio' in st.session_state:
        existing_data = collection.find_one({"folio": st.session_state['folio']})
        # If existing data is found, use it to pre-fill the form; otherwise, use default values
        prefill_data = existing_data if existing_data else {}
        
        # show_datos_laborales()
        with st.form(key='datos_laborales'):
            # st.title(':orange[Datos Laborales]')
            folio_from_db = prefill_data.get('folio', '')
            name_from_db = prefill_data.get('name', '')
            st.write(f':red[folio:] {folio_from_db}')
            st.write(f':red[Nombre:] {name_from_db}')
            col1, col2 = st.columns(2)
            with col1:
                company_name = st.text_input('Empresa', placeholder='Ingresa el nombre de la empresa')
            with col2:
                position = st.text_input('Puesto', placeholder='Ingresa el nombre del puesto')
            
            col1, col2, col3 = st.columns(3)
            with col1:
                start_date = st.date_input('Fecha de ingreso', value=None, format="DD/MM/YYYY", min_value=datetime(1920, 1, 1))
            with col2:
                end_date = st.date_input('Fecha de salida', value=None, format="DD/MM/YYYY", min_value=datetime(1920, 1, 1))
            with col3:
                monthly_salary = st.text_input('Salario', placeholder='Ingresa tu salario mensual')

            reason_exit = st.text_area('Motivo de salida', placeholder='Detalla el motivo por el cual dejaste de laborar en esta empresa')
            best_job_experience = st.text_area('Mejor experiencia o aprendizaje laboral', placeholder='Detalla tu mejor experiencia laboral en esta empresa')
            worst_job_experience = st.text_area('Mala experiencia o aprendizaje laboral', placeholder='Detalla una mala experiencia laboral en esta empresa')
            job_duties = st.text_area('Cuáles eran tus actividades', placeholder='Describe tus actividades laborales en esta empresa')

            submit_datos_laborales = st.form_submit_button(':orange[Guardar Experiencia Laboral]')
            if submit_datos_laborales:
                # Create the 'work_experience' object
                work_experience = {
                    'company_name': company_name,
                    'position': position,
                    'start_date': start_date.isoformat() if start_date is not None else None,
                    'end_date': end_date.isoformat() if end_date is not None else None,
                    'monthly_salary': monthly_salary,
                    'reason_exit': reason_exit,
                    'best_job_experience': best_job_experience,
                    'worst_job_experience': worst_job_experience,
                    'job_duties': job_duties,
                }

                # Prepare the update data for MongoDB
                labor_data_update = {"$push": {"labor_data": work_experience}}

                try:
                    # Update the data in MongoDB
                    collection.update_one({"folio": folio_from_db}, labor_data_update, upsert=True)
                    st.success("Datos Laborales guardados exitosamente!")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        show_datos_laborales()

def show_datos_laborales():
    if 'folio' in st.session_state:
        existing_data = collection.find_one({"folio": st.session_state['folio']})
        prefill_data = existing_data if existing_data else {}
        name_from_db = prefill_data.get('name', '')
        labor_data = existing_data.get("labor_data", [])
        # name_db = company_data.get("company_name", "Unknown Company")
        for index, labor in enumerate(labor_data, start=1):
            # Use columns to layout labor details and delete button
            col1, col2 = st.columns([0.8, 0.1])
            with col1:
                # Display the labor details
                st.markdown(f"**:orange[{index}-]** {labor.get('position', 'N/A')} :orange[/] {labor.get('company_name', 'N/A')}")
                # st.divider()
                
            with col2:
                # Construct a unique key for the button based on the labor details
                button_key = f"delete_{labor['position']}_{labor['company_name']}"
                # Display the delete button next to the labor details with the unique key
                if st.button(":red[Borrar]", key=button_key):
                    delete_dato_laboral(labor)
                    # Refresh the page to see the updated list
                    st.rerun()
    else:
        st.info(f"No labor data saved for {name_from_db}.")

def delete_dato_laboral(work_experience):
    """
    Remove the specified dato from the database.
    """
    try:
        collection.update_one(
            {"folio": st.session_state['folio']},
            {"$pull": {"labor_data": work_experience}}
        )
        st.success("Borrado")
    except Exception as e:
        st.error(f"An error occurred: {e}")

def historia_medica():
    # Try to retrieve existing data for the user
    if 'folio' in st.session_state:
        existing_data = collection.find_one({"folio": st.session_state['folio']})
        # If existing data is found, use it to pre-fill the form; otherwise, use default values
        prefill_data = existing_data if existing_data else {}
        with st.form(key='historia_medica'):
            # st.title(':orange[Historia Medica]')
            folio_from_db = prefill_data.get('folio', '')
            name_from_db = prefill_data.get('name', '')
            st.write(f':red[folio:] {folio_from_db}')
            st.write(f':red[Nombre:] {name_from_db}')
            col1, col2 = st.columns(2)
            with col1:
                health_condition_options = ('Buena', 'Regular', 'Mala')
                health_condition_default = health_condition_options.index(prefill_data.get('health_condition', 'Buena')) if prefill_data.get('health_condition') in health_condition_options else 0
                health_condition = st.selectbox('Condicion general de salud', health_condition_options, index=health_condition_default)
                current_physical_discomfort_options = ('Si', 'No')
                current_physical_discomfort_default = current_physical_discomfort_options.index(prefill_data.get('current_physical_discomfort', 'No')) if prefill_data.get('current_physical_discomfort') in current_physical_discomfort_options else 0
                current_physical_discomfort = st.selectbox('Malestar Físico Actual', current_physical_discomfort_options, index=current_physical_discomfort_default)
                chronic_disease = st.text_input('Enfermedad Crónica', value=prefill_data.get('chronic_disease', ''), placeholder='Especificar enfermedad crónica')
                # Assuming last_meal_time is stored in a format like 'HH:MM:SS' or 'HH:MM'
                last_meal_time_str = prefill_data.get('last_meal_time')
                if last_meal_time_str:
                    try:
                        # Try parsing with seconds included
                        last_meal_time_value = datetime.strptime(last_meal_time_str, '%H:%M:%S').time()
                    except ValueError:
                        # Fallback to parsing without seconds
                        last_meal_time_value = datetime.strptime(last_meal_time_str, '%H:%M').time()
                else:
                    last_meal_time_value = None

                last_meal_time = st.time_input('A qué hora fue la última comida', value=last_meal_time_value)
                nervous_treatment_options = ('Si', 'No')
                nervous_treatment_default = nervous_treatment_options.index(prefill_data.get('nervous_treatment', 'No')) if prefill_data.get('nervous_treatment') in nervous_treatment_options else 0
                nervous_treatment = st.selectbox('Tratamiento nervioso', nervous_treatment_options, index=nervous_treatment_default)
                psychologist_treatment_options = ('Si', 'No')
                psychologist_treatment_default = psychologist_treatment_options.index(prefill_data.get('psychologist_treatment', 'No')) if prefill_data.get('psychologist_treatment') in psychologist_treatment_options else 0
                psychologist_treatment = st.selectbox('Tratamiento psicológico o psiquiátrico', psychologist_treatment_options, index=psychologist_treatment_default)
                
                recent_hospitalizations_options = ('Si', 'No')
                recent_hospitalizations_default = recent_hospitalizations_options.index(prefill_data.get('recent_hospitalizations', 'No')) if prefill_data.get('recent_hospitalizations') in recent_hospitalizations_options else 0
                recent_hospitalizations = st.selectbox('Hospitalizaciones recientes', recent_hospitalizations_options, index=recent_hospitalizations_default)
                recent_surgeries_options = ('Si', 'No')
                recent_surgeries_default = recent_surgeries_options.index(prefill_data.get('recent_surgeries', 'No')) if prefill_data.get('recent_surgeries') in recent_surgeries_options else 0
                recent_surgeries = st.selectbox('Cirugias recientes', recent_surgeries_options, index=recent_surgeries_default)
            with col2:
                specify_health_condition = st.text_input('Si elegiste "REGULAR" o "MALA', value=prefill_data.get('specify_health_condition', ''), placeholder='Especifíca')
                specify_current_physical_discomfort = st.text_input('Si elegiste "SI"', value=prefill_data.get('specify_current_physical_discomfort', ''), placeholder='Especifíca')
                recent_medical_treatment = st.text_input('Tratamiento médico reciente', value=prefill_data.get('recent_medical_treatment', ''), placeholder='Especifíca')
                sleep_hours = st.number_input('¿Cuántas horas duerme aproximadamente?', min_value=0, max_value=24, value=prefill_data.get('sleep_hours', 0), step=1)
                specify_nervous_treatment = st.text_input('Si elegiste "SI"', value=prefill_data.get('specify_nervous_treatment', ''), placeholder='Detalla tu tratamiento nervioso')
                specify_psychologist_treatment = st.text_input('Si elegiste "SI"', value=prefill_data.get('specify_psychologist_treatment', ''), placeholder='Detalla tu tratamiento psicológico o psiquiátrico')
                specify_recent_hospitalizations = st.text_input('Si elegiste "SI"', value=prefill_data.get('specify_recent_hospitalizations', ''), placeholder='Detalla tus hospitalizaciones recientes')
                specify_recent_surgeries = st.text_input('Si elegiste "SI"', value=prefill_data.get('specify_recent_surgeries', ''), placeholder='Detalla tus cirugias recientes')
            st.markdown('##### Problemas:')
            st.markdown('Marque con una :white_check_mark: y especifique')
            col1, col2, col3, col4 = st.columns([0.9,1.1,0.7,1.3])
            with col1:
                respiratory = st.checkbox('Respiratorios', value=prefill_data.get('respiratory', False))
            with col2:
                specify_respiratory = st.text_input('specify_respiratory', value=prefill_data.get('specify_respiratory', ''), label_visibility="collapsed", placeholder='Especificar')
            with col3:
                allergies = st.checkbox('Alergias', value=prefill_data.get('allergies', False))
            with col4:
                specify_allergies = st.text_input('specify_allergies', value=prefill_data.get('specify_allergies', ''), label_visibility="collapsed", placeholder='Especificar')
            col1, col2, col3, col4 = st.columns([0.9,1.1,0.7,1.3])
            with col1:
                heart = st.checkbox('Corazón', value=prefill_data.get('heart', False))
            with col2:
                specify_heart = st.text_input('Especificar Corazón', value=prefill_data.get('specify_heart', ''), label_visibility="collapsed", placeholder='Especificar')
            with col3:
                digestives = st.checkbox('Digestivos', value=prefill_data.get('digestives', False))
            with col4:
                specify_digestives = st.text_input('Especificar Digestivos', value=prefill_data.get('specify_digestives', ''), label_visibility="collapsed", placeholder='Especificar')
            col1, col2, col3, col4 = st.columns([0.9,1.1,0.7,1.3])
            with col1:
                blood_pressure = st.checkbox('Presión', value=prefill_data.get('blood_pressure', False))
            with col2:
                specify_blood_pressure = st.text_input('Especificar Presión', value=prefill_data.get('specify_blood_pressure', ''), label_visibility="collapsed", placeholder='Especificar')

            with col3:
                pregnancy = st.checkbox('Embarazo', value=prefill_data.get('pregnancy', False))
            with col4:
                specify_pregnancy = st.text_input('Especificar Embarazo', value=prefill_data.get('specify_pregnancy', ''), label_visibility="collapsed", placeholder='Especificar')
            col1, col2, col3, col4 = st.columns([0.9,1.1,0.7,1.3])
            with col1:
                diabetes = st.checkbox('Diabetes', value=prefill_data.get('diabetes', False))
            with col2:
                specify_diabetes = st.text_input('Especificar Diabetes', value=prefill_data.get('specify_diabetes', ''), label_visibility="collapsed", placeholder='Especificar')

            with col3:
                migraine = st.checkbox('Migraña', value=prefill_data.get('migraine', False))
            with col4:
                specify_migraine = st.text_input('Especificar Migraña', value=prefill_data.get('specify_migraine', ''), label_visibility="collapsed", placeholder='Especificar')

            col1, col2, col3, col4 = st.columns([0.9,1.1,0.7,1.3])
            with col1:
                fainting = st.checkbox('Desmayos', value=prefill_data.get('fainting', False))
            with col2:
                specify_fainting = st.text_input('Especificar Desmayos', value=prefill_data.get('specify_fainting', ''), label_visibility="collapsed", placeholder='Especificar')

            with col3:
                injuries = st.checkbox('Heridas', value=prefill_data.get('injuries', False))
            with col4:
                specify_injuries = st.text_input('Especificar Heridas', value=prefill_data.get('specify_injuries', ''), label_visibility="collapsed", placeholder='Especificar')

            col1, col2, col3, col4 = st.columns([0.9,1.1,0.7,1.3])
            with col1:
                convulsion = st.checkbox('Convulsiones', value=prefill_data.get('convulsion', False))
            with col2:
                specify_convulsion = st.text_input('Especificar Convulsiones', value=prefill_data.get('specify_convulsion', ''), label_visibility="collapsed", placeholder='Especificar')

            with col3:
                others = st.checkbox('Otros', value=prefill_data.get('others', False))
            with col4:
                specify_others = st.text_input('Especificar Otros', value=prefill_data.get('specify_others', ''), label_visibility="collapsed", placeholder='Especificar')
            submit_historia_medica = st.form_submit_button(':orange[Guardar historia medica]')
            if submit_historia_medica:
                # Collecting data from the form fields
                medical_data = {
                    'folio': folio_from_db,
                    'health_condition': health_condition,
                    'current_physical_discomfort': current_physical_discomfort,
                    'chronic_disease': chronic_disease,
                    'last_meal_time': last_meal_time.isoformat() if last_meal_time else None,
                    'nervous_treatment': nervous_treatment,
                    'psychologist_treatment': psychologist_treatment,
                    'recent_hospitalizations': recent_hospitalizations,
                    'recent_surgeries': recent_surgeries,
                    'specify_health_condition': specify_health_condition,
                    'specify_current_physical_discomfort': specify_current_physical_discomfort,
                    'recent_medical_treatment': recent_medical_treatment,
                    'sleep_hours': sleep_hours,
                    'specify_nervous_treatment': specify_nervous_treatment,
                    'specify_psychologist_treatment': specify_psychologist_treatment,
                    'specify_recent_hospitalizations': specify_recent_hospitalizations,
                    'specify_recent_surgeries': specify_recent_surgeries,
                    'respiratory': respiratory,
                    'specify_respiratory': specify_respiratory,
                    'allergies': allergies,
                    'specify_allergies': specify_allergies,
                    'heart': heart,
                    'specify_heart': specify_heart,
                    'digestives': digestives,
                    'specify_digestives': specify_digestives,
                    'blood_pressure': blood_pressure,
                    'specify_blood_pressure': specify_blood_pressure,
                    'pregnancy': pregnancy,
                    'specify_pregnancy': specify_pregnancy,
                    'diabetes': diabetes,
                    'specify_diabetes': specify_diabetes,
                    'migraine': migraine,
                    'specify_migraine': specify_migraine,
                    'fainting': fainting,
                    'specify_fainting': specify_fainting,
                    'injuries': injuries,
                    'specify_injuries': specify_injuries,
                    'convulsion': convulsion,
                    'specify_convulsion': specify_convulsion,
                    'others': others,
                    'specify_others': specify_others
                }

                try:
                    # Update the data in MongoDB
                    collection.update_one({"folio": folio_from_db}, {"$set": medical_data}, upsert=True)
                    st.success("Historia Médica guardada exitosamente!")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

def aspectos_emocionales():
    # Try to retrieve existing data for the user
    if 'folio' in st.session_state:
        existing_data = collection.find_one({"folio": st.session_state['folio']})
        # If existing data is found, use it to pre-fill the form; otherwise, use default values
        prefill_data = existing_data if existing_data else {}
        with st.form(key='aspectos emocionales'):
            # st.title(':orange[Aspectos Emocionales]')
            folio_from_db = prefill_data.get('folio', '')
            name_from_db = prefill_data.get('name', '')
            st.write(f':red[folio:] {folio_from_db}')
            st.write(f':red[Nombre:] {name_from_db}')
            col1, col2 = st.columns(2)
            with col1:
                father_name = st.text_input('Nombre del padre', value=prefill_data.get('father_name', ''), placeholder='Ingresa el nombre de tu padre')
                mother_name = st.text_input('Nombre de la madre', value=prefill_data.get('mother_name', ''), placeholder='Ingresa el nombre de tu madre')
            with col2:
                father_ocupation = st.text_input('Ocupacion del padre', value=prefill_data.get('father_ocupation', ''), placeholder='Ingresa la ocupación de tu padre')
                mother_ocupation = st.text_input('Ocupación de la madre', value=prefill_data.get('mother_ocupation', ''), placeholder='Ingresa la ocupación de tu madre')
            col1, col2 = st.columns([.5,1.5])
            with col1:
                num_brothers = st.number_input('Numero de Hermanos',
                                            min_value=0, 
                                            max_value=30, 
                                            value=prefill_data.get('num_brothers', 0), 
                                            step=1)
            col1, col2 = st.columns(2)
            with col1:
                brothers_name = st.text_area('Nombre de hermanos', value=prefill_data.get('brothers_name', ''), placeholder='Ingresa el nombre de tus hermanos y/o hermanas')
            with col2:
                brothers_ocupation = st.text_area('Ocupacion de hermanos', value=prefill_data.get('brothers_ocupation', ''), placeholder='Ingresa la ocupación de tus hermanos y/o hermanas')
            who_do_you_live_with = st.text_input('¿Con quién vives?', value=prefill_data.get('who_do_you_live_with', ''), placeholder='')
            col1, col2 = st.columns(2)
            with col1:
                best_life_experience = st.text_area('Tu mejor experiencia', value=prefill_data.get('best_life_experience', ''), placeholder='Ingresa la mejor experiencia que hayas tenido en la vida')
            with col2:
                worst_life_experience = st.text_area('Tu experiencia más desagradable', value=prefill_data.get('worst_life_experience', ''), placeholder='Ingresa la experiencia más desagradable que hayas tenido en la vida')
            submit_aspectos_emocionales = st.form_submit_button(':orange[Guardar aspectos emocionales]')
            if submit_aspectos_emocionales:
                emotional_data = {
                    'father_name': father_name,
                    'mother_name': mother_name,
                    'father_ocupation': father_ocupation,
                    'mother_ocupation': mother_ocupation,
                    'num_brothers': num_brothers,
                    'brothers_name': brothers_name,
                    'brothers_ocupation': brothers_ocupation,
                    'who_do_you_live_with': who_do_you_live_with,
                    'best_life_experience': best_life_experience,
                    'worst_life_experience': worst_life_experience,
                }
                try:
                    # Update the data in MongoDB
                    collection.update_one({"folio": folio_from_db}, {"$set": emotional_data}, upsert=True)
                    st.success("Aspectos emocionales guardados exitosamente!")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

def aspectos_economicos():
    # Try to retrieve existing data for the user
    if 'folio' in st.session_state:
        existing_data = collection.find_one({"folio": st.session_state['folio']})
        # If existing data is found, use it to pre-fill the form; otherwise, use default values
        prefill_data = existing_data if existing_data else {}
        with st.form(key='aspectos_economicos'):
            # st.title(':orange[Aspectos Economicos]')
            folio_from_db = prefill_data.get('folio', '')
            name_from_db = prefill_data.get('name', '')
            st.write(f':red[folio:] {folio_from_db}')
            st.write(f':red[Nombre:] {name_from_db}')
            col1, col2 = st.columns(2)
            with col1:
                debts = st.selectbox(
                    '¿Tiene deudas económicas?',
                    ('Si', 'No'), 
                    index=None if prefill_data.get('debts') is None else ('Si', 'No').index(prefill_data.get('debts', 'No')),
                    placeholder='Elige una opción'
                )
                # debts_options = ('Si', 'No')
                # debts_default = debts_options.index(prefill_data.get('debts', 'No')) if prefill_data.get('debts') in debts_options else 0
                # debts = st.selectbox('¿Tiene deudas económicas?', debts_options, index=debts_default)
                banks = st.text_input('Bancos:', value=prefill_data.get('banks', ''),)
                tarjetas_departamentales = st.text_input('Tarjetas departamentales:', value=prefill_data.get('tarjetas_departamentales', ''),)
                empenos = st.text_input('Empeños:', value=prefill_data.get('empenos', ''),)
            with col2:
                specify_debts = st.text_input('Si eligiste "SI", especifica ', value=prefill_data.get('specify_debts', ''),)
                bank_debt = st.text_input('Valor de la deuda en bancos $', value=prefill_data.get('bank_debt', ''))
                tarjetas_departamentales_debt = st.text_input('Valor de la deuda en tarjetas departamentales $', value=prefill_data.get('tarjetas_departamentales_debt', ''))
                empenos_debt = st.text_input('Cuantía $', value=prefill_data.get('empenos_debt', ''))
            st.markdown('##### Bienes Patrimoniales')
            col1, col2, col3 = st.columns(3)
            with col1:
                cars = st.text_input('Autos', value=prefill_data.get('cars', ''))
                house = st.text_input('Casa', value=prefill_data.get('house', ''))
            with col2:
                properties = st.text_input('Inmueble', value=prefill_data.get('properties', ''))
                investments = st.text_input('Inversiones', value=prefill_data.get('investments', ''))
            with col3:
                business = st.text_input('Negocio', value=prefill_data.get('business', ''))
            submit_aspectos_economicos = st.form_submit_button(':orange[Guardar información económica]')
            if submit_aspectos_economicos:
                economic_data = {
                    'debts': debts,
                    'banks': banks,
                    'tarjetas_departamentales': tarjetas_departamentales,
                    'empenos': empenos,
                    'specify_debts': specify_debts,
                    'bank_debt': bank_debt,
                    'tarjetas_departamentales_debt': tarjetas_departamentales_debt,
                    'empenos_debt': empenos_debt,
                    'cars': cars,
                    'house': house,
                    'properties': properties,
                    'investments': investments,
                    'business': business,
                }
                try:
                    # Update the data in MongoDB
                    collection.update_one({"folio": folio_from_db}, {"$set": economic_data}, upsert=True)
                    st.success("Aspectos económicos guardados exitosamente!")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

def discusion_desarrollo():
    # Try to retrieve existing data for the user
    if 'folio' in st.session_state:
        existing_data = collection.find_one({"folio": st.session_state['folio']})
        # If existing data is found, use it to pre-fill the form; otherwise, use default values
        prefill_data = existing_data if existing_data else {}
        with st.form(key='discusion_desarrollo'):
            # st.title(':orange[Discusión y Desarrollo de Temas]')
            folio_from_db = prefill_data.get('folio', '')
            name_from_db = prefill_data.get('name', '')
            st.write(f':red[folio:] {folio_from_db}')
            st.write(f':red[Nombre:] {name_from_db}')
            st.markdown('##### :orange[Información Laboral]')
            info_laboral_1 = st.selectbox(
                '¿Se te ha pedido renuncia de cualquiera de tus empleos anteriores?',
                ('Si', 'No'), 
                index=None if prefill_data.get('info_laboral_1') is None else ('Si', 'No').index(prefill_data.get('info_laboral_1', 'No')),
                placeholder='Elige una opción'
            )
            info_laboral_2 = st.selectbox(
                '¿Se te ha acusado alguna vez de deshonestidad de cualquiera de tus empleos anteriores?', 
                ('Si', 'No'), 
                index=None if prefill_data.get('info_laboral_2') is None else ('Si', 'No').index(prefill_data.get('info_laboral_2', 'No')),
                placeholder='Elige una opción'
            )
            info_laboral_3 = st.selectbox(
                '¿Has violado los reglamentos establecidos de cualquier empleo?', 
                ('Si', 'No'), 
                index=None if prefill_data.get('info_laboral_3') is None else ('Si', 'No').index(prefill_data.get('info_laboral_3', 'No')),
                placeholder='Elige una opción'
            )
            info_laboral_4 = st.selectbox(
                '¿Has usado tu puesto o tus funciones para obtener beneficios en forma ilícita o no autorizada?', 
                ('Si', 'No'), 
                index=None if prefill_data.get('info_laboral_4') is None else ('Si', 'No').index(prefill_data.get('info_laboral_4', 'No')),
                placeholder='Elige una opción'
            )
            info_laboral_5 = st.selectbox(
                '¿Has hecho uso indebido de información confidencial de cualquiera de tus trabajos?', 
                ('Si', 'No'), 
                index=None if prefill_data.get('info_laboral_5') is None else ('Si', 'No').index(prefill_data.get('info_laboral_5', 'No')),
                placeholder='Elige una opción'
            )
            info_laboral_6 = st.text_input(
                '¿Cuál ha sido el problema laboral más serio que has tenido?',
                value=prefill_data.get('info_laboral_6', '')
            )
            info_laboral_7 = st.selectbox(
                '¿Has tenido discusiones serias con superiores?', 
                ('Si', 'No'), 
                index=None if prefill_data.get('info_laboral_7') is None else ('Si', 'No').index(prefill_data.get('info_laboral_7', 'No')),
                placeholder='Elige una opción'
            )
            info_laboral_8 = st.text_input(
                '¿Cuáles han sido las faltas administrativas más serias que has cometido de empleos anteriores?',
                value=prefill_data.get('info_laboral_8', '')
            )
            info_laboral_9 = st.selectbox(
                '¿Se ha levantado algún acta administrativa o algún proceso laboral?',
                ('Si', 'No'), 
                index=None if prefill_data.get('info_laboral_9') is None else ('Si', 'No').index(prefill_data.get('info_laboral_9', 'No')),
                placeholder='Elige una opción'
            )
            info_laboral_10 = st.selectbox(
                '¿Has aceptado sobornos de cualquier tipo de cualquiera de tus empleos anteriores?',
                ('Si', 'No'), 
                index=None if prefill_data.get('info_laboral_10') is None else ('Si', 'No').index(prefill_data.get('info_laboral_10', 'No')),
                placeholder='Elige una opción'
            )
            info_laboral_11 = st.selectbox(
                '¿Has saboteado tu trabajo o el de tus compañeros?',
                ('Si', 'No'), 
                index=None if prefill_data.get('info_laboral_11') is None else ('Si', 'No').index(prefill_data.get('info_laboral_11', 'No')),
                placeholder='Elige una opción'
            )
            info_laboral_12 = st.selectbox(
                '¿Se ha levantado alguna demanda laboral en tu contra?',
                ('Si', 'No'), 
                index=None if prefill_data.get('info_laboral_12') is None else ('Si', 'No').index(prefill_data.get('info_laboral_12', 'No')),
                placeholder='Elige una opción'
            )
            info_laboral_13 = st.selectbox(
                '¿Has demandado laboralmente a la empresa o alguno de tus jefes?',
                ('Si', 'No'), 
                index=None if prefill_data.get('info_laboral_13') is None else ('Si', 'No').index(prefill_data.get('info_laboral_13', 'No')),
                placeholder='Elige una opción'
            )
            info_laboral_14 = st.selectbox(
                '¿Supiste de personas de tus trabajos anteriores que hayan realizando actos ilegales?',
                ('Si', 'No'), 
                index=None if prefill_data.get('info_laboral_14') is None else ('Si', 'No').index(prefill_data.get('info_laboral_14', 'No')),
                placeholder='Elige una opción'
            )
            info_laboral_15 = st.selectbox(
                '¿Has participado de algún robo en alguna empresa?',
                ('Si', 'No'), 
                index=None if prefill_data.get('info_laboral_15') is None else ('Si', 'No').index(prefill_data.get('info_laboral_15', 'No')),
                placeholder='Elige una opción'
            )
            info_laboral_16 = st.selectbox(
                '¿Te has visto comprometido en realizar alguna conducta que afecte los intereses de la empresa?',
                ('Si', 'No'), 
                index=None if prefill_data.get('info_laboral_16') is None else ('Si', 'No').index(prefill_data.get('info_laboral_16', 'No')),
                placeholder='Elige una opción'
            )
            info_laboral_17 = st.selectbox(
                '¿Has falsificado o alterado de manera intencional documentos de tu empresa?',
                ('Si', 'No'), 
                index=None if prefill_data.get('info_laboral_17') is None else ('Si', 'No').index(prefill_data.get('info_laboral_17', 'No')),
                placeholder='Elige una opción'
            )
            info_laboral_18 = st.selectbox(
                '¿Has hecho uso indebido de los recursos de la empresa?',
                ('Si', 'No'), 
                index=None if prefill_data.get('info_laboral_18') is None else ('Si', 'No').index(prefill_data.get('info_laboral_18', 'No')),
                placeholder='Elige una opción'
            )
            st.markdown('##### Actividades Delictivas')
            actividades_delictivas_1 = st.selectbox(
                '¿Conoces a delincuentes o grupos delictivos de cualquier tipo?',
                ('Si', 'No'), 
                index=None if prefill_data.get('actividades_delictivas_1') is None else ('Si', 'No').index(prefill_data.get('actividades_delictivas_1', 'No')),
                placeholder='Elige una opción'
            )
            actividades_delictivas_2 = st.selectbox(
                '¿Has sido detenido o cuestionado por la policía por cualquier motivo?',
                ('Si', 'No'), 
                index=None if prefill_data.get('actividades_delictivas_2') is None else ('Si', 'No').index(prefill_data.get('actividades_delictivas_2', 'No')),
                placeholder='Elige una opción'
            )
            actividades_delictivas_3 = st.selectbox(
                '¿Has estado detenido en delegaciones, reclusorios, cárceles o penitenciarias?',
                ('Si', 'No'), 
                index=None if prefill_data.get('actividades_delictivas_3') is None else ('Si', 'No').index(prefill_data.get('actividades_delictivas_3', 'No')),
                placeholder='Elige una opción'
            )
            actividades_delictivas_4 = st.selectbox(
                '¿Has hecho algo por lo que pudiste haber sido detenido?',
                ('Si', 'No'), 
                index=None if prefill_data.get('actividades_delictivas_4') is None else ('Si', 'No').index(prefill_data.get('actividades_delictivas_4', 'No')),
                placeholder='Elige una opción'
            )
            actividades_delictivas_5 = st.selectbox(
                '¿Alguien de tu familia ha estado detenido en reclusorios, cárceles o penitenciarias?',
                ('Si', 'No'), 
                index=None if prefill_data.get('actividades_delictivas_5') is None else ('Si', 'No').index(prefill_data.get('actividades_delictivas_5', 'No')),
                placeholder='Elige una opción'
            )
            actividades_delictivas_6 = st.selectbox(
                '¿Has tenido cargos por cualquier falta cometida?',
                ('Si', 'No'), 
                index=None if prefill_data.get('actividades_delictivas_6') is None else ('Si', 'No').index(prefill_data.get('actividades_delictivas_6', 'No')),
                placeholder='Elige una opción'
            )
            actividades_delictivas_7 = st.selectbox(
                '¿Utilizas armas de fuego?',
                ('Si', 'No'), 
                index=None if prefill_data.get('actividades_delictivas_7') is None else ('Si', 'No').index(prefill_data.get('actividades_delictivas_7', 'No')),
                placeholder='Elige una opción'
            )
            actividades_delictivas_8 = st.selectbox(
                '¿Venta, comercialización de armas de fuego?',
                ('Si', 'No'), 
                index=None if prefill_data.get('actividades_delictivas_8') is None else ('Si', 'No').index(prefill_data.get('actividades_delictivas_8', 'No')),
                placeholder='Elige una opción'
            )
            actividades_delictivas_9 = st.selectbox(
                '¿Le has causado lesiones a personas con armas de fuego?',
                ('Si', 'No'), 
                index=None if prefill_data.get('actividades_delictivas_9') is None else ('Si', 'No').index(prefill_data.get('actividades_delictivas_9', 'No')),
                placeholder='Elige una opción'
            )
            actividades_delictivas_10 = st.selectbox(
                '¿Tienes antecedentes penales?',
                ('Si', 'No'), 
                index=None if prefill_data.get('actividades_delictivas_10') is None else ('Si', 'No').index(prefill_data.get('actividades_delictivas_10', 'No')),
                placeholder='Elige una opción'
            )
            actividades_delictivas_11 = st.selectbox(
                '¿Has ayudado a alguien a cometer alguna actividad ilícita, delito o acto vandálico?',
                ('Si', 'No'), 
                index=None if prefill_data.get('actividades_delictivas_11') is None else ('Si', 'No').index(prefill_data.get('actividades_delictivas_11', 'No')),
                placeholder='Elige una opción'
            )
            actividades_delictivas_12 = st.selectbox(
                '¿Se ha levantado alguna demanda civil, mercantil o judicial, en tu contra?',
                ('Si', 'No'), 
                index=None if prefill_data.get('actividades_delictivas_12') is None else ('Si', 'No').index(prefill_data.get('actividades_delictivas_12', 'No')),
                placeholder='Elige una opción'
            )
            actividades_delictivas_13 = st.selectbox(
                '¿Has cometido fraude, extorsión o chantaje?',
                ('Si', 'No'), 
                index=None if prefill_data.get('actividades_delictivas_13') is None else ('Si', 'No').index(prefill_data.get('actividades_delictivas_13', 'No')),
                placeholder='Elige una opción'
            )
            actividades_delictivas_14 = st.selectbox(
                '¿Has estado involucrado en algún secuestro?',
                ('Si', 'No'), 
                index=None if prefill_data.get('actividades_delictivas_14') is None else ('Si', 'No').index(prefill_data.get('actividades_delictivas_14', 'No')),
                placeholder='Elige una opción'
            )
            st.markdown('##### Hábitos Personales')
            habitos_personales_1 = st.text_input(
                '¿Cuándo fue la última vez que bebiste?',
                value=prefill_data.get('habitos_personales_1', '')
            )
            habitos_personales_2 = st.text_input(
                '¿Cuánto bebes al mes en promedio?',
                value=prefill_data.get('habitos_personales_2', '')
            )
            habitos_personales_3 = st.text_input(
                '¿Cuándo fue la última vez que olvidaste lo ocurrido mientras bebías?',
                value=prefill_data.get('habitos_personales_3', '')
            )
            habitos_personales_4 = st.text_input(
                '¿Cuándo fue la última vez que manejaste en estado de ebriedad?',
                value=prefill_data.get('habitos_personales_4', '')
            )
            habitos_personales_5 = st.selectbox(
                '¿Ha sido detenido por conducir en estado de embriaguez vehículos de la empresa?',
                ('Si', 'No'), 
                index=None if prefill_data.get('habitos_personales_5') is None else ('Si', 'No').index(prefill_data.get('habitos_personales_5', 'No')),
                placeholder='Elige una opción'
            )
            habitos_personales_6 = st.selectbox(
                '¿Te has presentado a laborar en estado de ebriedad, con aliento alcohólico o con resaca?',
                ('Si', 'No'), 
                index=None if prefill_data.get('habitos_personales_6') is None else ('Si', 'No').index(prefill_data.get('habitos_personales_6', 'No')),
                placeholder='Elige una opción'
            )
            habitos_personales_7 = st.selectbox(
                '¿Has faltado a tu trabajo por haber ingerido alcohol?',
                ('Si', 'No'), 
                index=None if prefill_data.get('habitos_personales_7') is None else ('Si', 'No').index(prefill_data.get('habitos_personales_7', 'No')),
                placeholder='Elige una opción'
            )
            habitos_personales_8 = st.selectbox(
                '¿Has ingerido bebidas alcohólicas en horas de trabajo?',
                ('Si', 'No'), 
                index=None if prefill_data.get('habitos_personales_8') is None else ('Si', 'No').index(prefill_data.get('habitos_personales_8', 'No')),
                placeholder='Elige una opción'
            )
            st.markdown('##### Drogas')
            drogas_1 = st.selectbox(
                '¿Consumes alguna droga ilegal?',
                ('Si', 'No'), 
                index=None if prefill_data.get('drogas_1') is None else ('Si', 'No').index(prefill_data.get('drogas_1', 'No')),
                placeholder='Elige una opción'
            )
            drogas_2 = st.selectbox(
                '¿Has probado o experimentado con cualquier droga ilegal?',
                ('Si', 'No'), 
                index=None if prefill_data.get('drogas_2') is None else ('Si', 'No').index(prefill_data.get('drogas_2', 'No')),
                placeholder='Elige una opción'
            )
            drogas_3 = st.selectbox(
                '¿Has tenido algún tipo de contacto con droga ilegal en su trabajo?',
                ('Si', 'No'), 
                index=None if prefill_data.get('drogas_3') is None else ('Si', 'No').index(prefill_data.get('drogas_3', 'No')),
                placeholder='Elige una opción'
            )
            drogas_4 = st.selectbox(
                '¿Has comprado o vendido cualquier droga ilegal?',
                ('Si', 'No'), 
                index=None if prefill_data.get('drogas_4') is None else ('Si', 'No').index(prefill_data.get('drogas_4', 'No')),
                placeholder='Elige una opción'
            )
            drogas_5 = st.selectbox(
                '¿Has transportado o distribuido alguna droga ilegal?',
                ('Si', 'No'), 
                index=None if prefill_data.get('drogas_5') is None else ('Si', 'No').index(prefill_data.get('drogas_5', 'No')),
                placeholder='Elige una opción'
            )
            drogas_6 = st.selectbox(
                '¿Tienes contactos con personas que vendan o distribuyan droga?',
                ('Si', 'No'), 
                index=None if prefill_data.get('drogas_6') is None else ('Si', 'No').index(prefill_data.get('drogas_6', 'No')),
                placeholder='Elige una opción'
            )
            drogas_7 = st.selectbox(
                '¿Sabe de alguna persona de la empresa que tenga relación con drogas ilegales?',
                ('Si', 'No'), 
                index=None if prefill_data.get('drogas_7') is None else ('Si', 'No').index(prefill_data.get('drogas_7', 'No')),
                placeholder='Elige una opción'
            )
            st.markdown('##### Antecedentes de Tránsito')
            transito_1 = st.selectbox(
                '¿Tienes antecedentes de tránsito?',
                ('Si', 'No'), 
                index=None if prefill_data.get('transito_1') is None else ('Si', 'No').index(prefill_data.get('transito_1', 'No')),
                placeholder='Elige una opción'
            )
            st.markdown('##### Conclusión o cierre')
            conclusion_1 = st.selectbox(
                '¿Has tenido alguna experiencia en tu trabajo por la que pudieras ser chantajeado posteriormente?',
                ('Si', 'No'), 
                index=None if prefill_data.get('conclusion_1') is None else ('Si', 'No').index(prefill_data.get('conclusion_1', 'No')),
                placeholder='Elige una opción'
            )

            conclusion_2 = st.selectbox(
                '¿Pensaste que el día de hoy iba a hacerte alguna otra pregunta de algo que no hayas comentado hasta el momento?',
                ('Si', 'No'), 
                index=None if prefill_data.get('conclusion_2') is None else ('Si', 'No').index(prefill_data.get('conclusion_2', 'No')),
                placeholder='Elige una opción'
            )

            conclusion_3 = st.selectbox(
                '¿Falseaste u omitiste deliberadamente alguna información que te haya solicitado el día de hoy?',
                ('Si', 'No'), 
                index=None if prefill_data.get('conclusion_3') is None else ('Si', 'No').index(prefill_data.get('conclusion_3', 'No')),
                placeholder='Elige una opción'
            )

            conclusion_4 = st.selectbox(
                '¿Hay algo en tu mente en este momento que te preocupe para no poder tener un buen examen?',
                ('Si', 'No'), 
                index=None if prefill_data.get('conclusion_4') is None else ('Si', 'No').index(prefill_data.get('conclusion_4', 'No')),
                placeholder='Elige una opción'
            )

            conclusion_5 = st.selectbox(
                '¿Hay algo que quieras decirme en este momento y estés dudando si hacerlo o no?',
                ('Si', 'No'), 
                index=None if prefill_data.get('conclusion_5') is None else ('Si', 'No').index(prefill_data.get('conclusion_5', 'No')),
                placeholder='Elige una opción'
            )

            conclusion_6 = st.text_area(
                'Observaciones',
                key='observaciones_user',
                placeholder='Si tienes algún comentario u observación puedes escribirlo aquí',
                value=prefill_data.get('conclusion_6', '')
            )
            submit_discusion_desarrollo = st.form_submit_button(':orange[Guardar]')
            if submit_discusion_desarrollo:
                discusion_desarrollo_data ={
                    'info_laboral_1': info_laboral_1,
                    'info_laboral_2': info_laboral_2,
                    'info_laboral_3': info_laboral_3,
                    'info_laboral_4': info_laboral_4,
                    'info_laboral_5': info_laboral_5,
                    'info_laboral_6': info_laboral_6,
                    'info_laboral_7': info_laboral_7,
                    'info_laboral_8': info_laboral_8,
                    'info_laboral_9': info_laboral_9,
                    'info_laboral_10': info_laboral_10,
                    'info_laboral_11': info_laboral_11,
                    'info_laboral_12': info_laboral_12,
                    'info_laboral_13': info_laboral_13,
                    'info_laboral_14': info_laboral_14,
                    'info_laboral_15': info_laboral_15,
                    'info_laboral_16': info_laboral_16,
                    'info_laboral_17': info_laboral_17,
                    'info_laboral_18': info_laboral_18,
                    'actividades_delictivas_1': actividades_delictivas_1,
                    'actividades_delictivas_2': actividades_delictivas_2,
                    'actividades_delictivas_3': actividades_delictivas_3,
                    'actividades_delictivas_4': actividades_delictivas_4,
                    'actividades_delictivas_5': actividades_delictivas_5,
                    'actividades_delictivas_6': actividades_delictivas_6,
                    'actividades_delictivas_7': actividades_delictivas_7,
                    'actividades_delictivas_8': actividades_delictivas_8,
                    'actividades_delictivas_9': actividades_delictivas_9,
                    'actividades_delictivas_10': actividades_delictivas_10,
                    'actividades_delictivas_11': actividades_delictivas_11,
                    'actividades_delictivas_12': actividades_delictivas_12,
                    'actividades_delictivas_13': actividades_delictivas_13,
                    'actividades_delictivas_14': actividades_delictivas_14,
                    'habitos_personales_1': habitos_personales_1,
                    'habitos_personales_2': habitos_personales_2,
                    'habitos_personales_3': habitos_personales_3,
                    'habitos_personales_4': habitos_personales_4,
                    'habitos_personales_5': habitos_personales_5,
                    'habitos_personales_6': habitos_personales_6,
                    'habitos_personales_7': habitos_personales_7,
                    'habitos_personales_8': habitos_personales_8,
                    'drogas_1': drogas_1,
                    'drogas_2': drogas_2,
                    'drogas_3': drogas_3,
                    'drogas_4': drogas_4,
                    'drogas_5': drogas_5,
                    'drogas_6': drogas_6,
                    'drogas_7': drogas_7,
                    'transito_1': transito_1,
                    'conclusion_1': conclusion_1,
                    'conclusion_2': conclusion_2,
                    'conclusion_3': conclusion_3,
                    'conclusion_4': conclusion_4,
                    'conclusion_5': conclusion_5,
                    'conclusion_6': conclusion_6,
                }
                try:
                    # Update the data in MongoDB
                    collection.update_one({"folio": folio_from_db}, {"$set": discusion_desarrollo_data}, upsert=True)
                    st.success("Aspectos económicos guardados exitosamente!")
                except Exception as e:
                    st.error(f"An error occurred: {e}")








