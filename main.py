import streamlit as st
import read_data
from PIL import Image
import person
import ekgdata_new_class


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
    st.markdown("<br>"*3, unsafe_allow_html=True)
    image = Image.open(Picturepath)
    st.image(image)

    Auswahl = ["Ruhe","Belastung"]
    st.session_state.modus = st.segmented_control("",
                                            Auswahl,
                                            selection_mode="single",
                                            key= "modus_selector",
                                            default="Ruhe"
                                            )

    if st.session_state.modus == "Ruhe":        #prüft Modus der Auswahlbox, und wählt demendsprechend den richtigen Pfad für das EKG aus
        a=0
    else:
        a=1


    try:
        Figure = ekgdata_new_class.EKGdata(ekgdata_new_class.EKGdata.ekg_dict_choose(id-1,a))
        avg_hr = Figure.calc_avg_hr()
        avg_hr_rounded = round(avg_hr)

        st.write("###### Alter: ",person.Person.load_by_id(id).calc_age())
        st.write("###### Durchschnittspuls: ",avg_hr_rounded)

    except Exception:
        st.write("######  ")

with spalte2:
    col1, col2, col3 = st.columns(3)
    
    
    if st.session_state.modus == "Ruhe":        #prüft Modus der Auswahlbox, und wählt demendsprechend den richtigen Pfad für das EKG aus
        a=0
    else:
        a=1


    try:
        Figure = ekgdata_new_class.EKGdata(ekgdata_new_class.EKGdata.ekg_dict_choose(id-1,a))
        fig = Figure.plot_time_series()

        st.plotly_chart(fig)

    except Exception:
        st.markdown("<br>"*4, unsafe_allow_html=True)
        st.info("#####     Für diese Person / Auswahl gibt es keine Daten")





    
  

    

    
