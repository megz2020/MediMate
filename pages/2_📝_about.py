import streamlit as st
import pandas as pd
st.set_page_config(page_title="About", page_icon="📝", layout="wide")

st.markdown("## MediMate")
st.markdown("## Team Members")
ahmed_link_text = "Ahmed Magdy"
ahmed_link_url = "https://www.linkedin.com/in/megzz/"
aya_link_text = "Aya Elshorbagy"
aya_link_url = "https://www.linkedin.com/in/aya-elshorbagy-7b64ab103/"
mark_link_text = "Mark Karme"
mark_link_url = "https://www.linkedin.com/in/mark-karme-b4a8a6196/"
ahmed_image_url = "https://media.licdn.com/dms/image/C4D03AQEVFhx_VOgiog/profile-displayphoto-shrink_800_800/0/1579654629383?e=1707955200&v=beta&t=zU_ywWZ8HZRMDXOqtNI-oKoFmLYY2fji0i6rr02o910"
aya_image_url = "https://media.licdn.com/dms/image/C5603AQHll4kgyNT3Vg/profile-displayphoto-shrink_800_800/0/1520073077775?e=1707955200&v=beta&t=cXHSrW1sJ6uoYzSW-hS6TF8tEYaI1-rVZWFbtS-A3C4"
mark_image_url = "https://media.licdn.com/dms/image/C5603AQGw0ip2g8wN1w/profile-displayphoto-shrink_800_800/0/1578678191341?e=1707955200&v=beta&t=z8R3na06M1kts_lLkesEgUE5wItcYj-a3LplejUlLJE"

# Display image and hyperlink
st.image(ahmed_image_url, width=100)
st.markdown(f"[{ahmed_link_text}]({ahmed_link_url})", unsafe_allow_html=True)

st.image(aya_image_url, width=100)
st.markdown(f"[{aya_link_text}]({aya_link_url})", unsafe_allow_html=True)

st.image(mark_image_url, width=100)
st.markdown(f"[{mark_link_text}]({mark_link_url})", unsafe_allow_html=True)
st.markdown("## Project Description and Motivation")
st.markdown("""MediMateAI is a cutting-edge tool designed to assist you in extracting\
                     essential information from your prescriptions. Utilizing artificial intelligence,\
                     it not only provides you with comprehensive details on the potential side effects\
                     of your medication but also alerts you to any possible conflicts between your current\
                     prescription and previous medications. Moreover, MediMateAI serves as a reminder to ensure\
                     you take your medication as prescribed, helping you maintain a consistent schedule.\
                    Please note that this is a beta version, and while it offers valuable insights,\
                     it is not intended as a substitute for professional medical advice from your doctor.\
                     Additionally, it is not yet ready for widespread use and should not be relied upon for predictive purposes.""")
st.markdown("## Github Repository")
st.markdown("[MediMateAI](https://github.com/megz2020/MediMate)")