import requests
import streamlit as st
# from streamlit_lottie import st_lottie
from PIL import Image
from io import StringIO
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import app as ap

# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
# st.set_page_config(page_title="My Webpage", page_icon=":tada:", layout="wide")

st.markdown("# Modelling 🎉")
st.sidebar.markdown("# Modelling 🎉")


lr=LinearRegression()
X=np.array(ap.df['SepalLengthCm']).reshape(-1,1)
y=np.array(ap.df['Species']).reshape(-1,1)
# lr.fit(X,y)
value = st.number_input("SepalLengthCm",4.50,7.50, step=0.20)
value = np.array(value).reshape(-1,1)
# prediction = lr.predict(value)[0]
if st.button("Species prediction"):
    st.write("predict")
    # st.write(f"{prediction}")