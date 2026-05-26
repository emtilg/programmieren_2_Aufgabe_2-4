import streamlit as st
import read_data
from PIL import Image


# Eine Überschrift der ersten Ebene
st.write("# EKG APP")

# Eine Überschrift der zweiten Ebene
st.write("## Versuchsperson auswählen")

h = read_data.load_person_data()
namensliste = read_data.get_person_list(h)

# Eine Auswahlbox
st.session_state.current_user = st.selectbox(
    'Versuchsperson',
    options = namensliste, key="sbVersuchsperson")    #der Key ist für streamlit eine einzigartie bezeichnung für ein Element in Streamlit.

eintrag = read_data.find_person_data_by_name(st.session_state.current_user)
Picturepath = eintrag["picture_path"]

image = Image.open(Picturepath)
st.image(image, caption = st.session_state.current_user)




