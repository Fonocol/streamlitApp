import streamlit as st
from forms.contact import contact_form

@st.dialog("Contact Me")
def show_contact_form():
    contact_form()
    

col1, col2 = st.columns(2,gap="small",vertical_alignment="center")
with col1:
    st.image("assets/me.png", width=230)
with col2:
    st.title("Colince FONO", anchor = False)
    st.write(
        "Etudiant en Master Big Data Et Machine Learning a EFREI-Paris en Alternance"
    )
    if st.button("Contact Me"):
        show_contact_form()


# experiances
st.write("\n")
st.subheader("Experience & Qualifications", anchor=False)
st.write(
    """
    - PowerBI Data Visualization 
    - Data Scientist
    - Machine Learning Engineer
    - Python Developer
    - Data Analyst
    - Web Developer
    """
)

#skill
st.write("\n")
st.subheader("Hard Skills", anchor=False)
st.write(
    """
    - PowerBI Data Visualization 
    - Python R SQL
    - Machine Learning Deep Learning
    - Excellent communication skills
    - Strong analytical and problem-solving skills
    - Strong coding skills in Python and R
    - Proficiency in data manipulation and analysis
    - Proficiency in web development
    - Proficiency in machine learning and deep learning
    """
)