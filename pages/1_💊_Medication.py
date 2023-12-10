import streamlit as st
import pandas as pd
st.set_page_config(page_title="Medication", page_icon="💊", layout="wide")

st.markdown("# The Medication has been prescribed")
if "prescription_detailes" not in st.session_state:
    st.markdown("## Please go to home page and upload the prescription")
    st.stop()
else:
    prescription_detailes = st.session_state.prescription_detailes
    st.markdown(f"## Patient Name: {prescription_detailes['patient']}")
    st.markdown(f"## Doctor Name: {prescription_detailes['doctor']}")
    st.markdown(f"## Date: {prescription_detailes['date']}")
    prescription_medication = st.session_state.prescription_medication
    df = pd.DataFrame(prescription_medication)
    st.markdown("## Medication:")
    st.dataframe(df)
