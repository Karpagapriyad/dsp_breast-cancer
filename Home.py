import streamlit as st

st.set_page_config(
    layout="wide",
    page_title= "Breast Cancer Prediction",
    page_icon= "breast_cancer_logo.png"
)

st.sidebar.success("")

with st.container():
    logo_col, title_col = st.columns([1, 3])
    # with logo_col:
    #     st.image("breast_cancer_logo.png", width=100)
    with title_col:
        st.title("Breast Cancer Prediction")

