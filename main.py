import streamlit as st
import read_data
from PIL import Image
import ekgdata


# Eine Überschrift der ersten Ebene
st.write("# EKG APP")

# Eine Überschrift der zweiten Ebene
st.write("## Versuchsperson auswählen")

h = read_data.load_person_data()
namensliste = read_data.get_person_list(h)

# Eine Auswahlbox
st.session_state.current_user = st.selectbox(
    '',
    options = namensliste, key="sbVersuchsperson")    #der Key ist für streamlit eine einzigartie bezeichnung für ein Element in Streamlit.

eintrag = read_data.find_person_data_by_name(st.session_state.current_user)
Picturepath = eintrag["picture_path"]
id = eintrag["id"]

spalte1, spalte2 = st.columns([1,3])

with spalte1:
    st.markdown("<br>"*4, unsafe_allow_html=True)
    image = Image.open(Picturepath)
    st.image(image)

with spalte2:

    Leistungstest_df = ekgdata.EKGdata.read_my_csv(ekgdata.EKGdata.load_EKG_by_id(id))
    plot = ekgdata.EKGdata.make_plot_df(Leistungstest_df)
    st.plotly_chart(plot)