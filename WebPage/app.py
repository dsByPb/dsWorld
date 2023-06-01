import requests
import streamlit as st
from PIL import Image
from io import StringIO
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pages import Data_Wrangling as dw

df = None

# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="My Webpage", page_icon=":tada:", layout="wide")

st.markdown("# Main page 🎈")
st.sidebar.markdown("# Main page 🎈")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# Use local CSS
def local_css(file_name):
    # path = os.path.join(os.path.dirname(__file__), '..', 'style', file_name)
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    

local_css("style/style.css")

# ---- LOAD ASSETS ----
lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
# path = os.path.join(os.path.dirname(__file__), '..', 'images', "yt_contact_form.png")
img_contact_form = Image.open("images/yt_contact_form.png")

# path = os.path.join(os.path.dirname(__file__), '..', 'images', "yt_lottie_animation.png")
img_lottie_animation = Image.open("images/yt_lottie_animation.png")

# ---- HEADER SECTION ----
with st.container():
    st.subheader("Hi, I am Priyab :wave:")
    # st.title("A Data Scientist From India")
    st.write(
        "I am passionate about finding ways to use Python to be more efficient and effective at work."
    )
    st.write("[Learn More >](https://dSbyPb.com)")

# -------------functionality-----------------------
# # Add a selectbox to the sidebar:
# add_selectbox = st.sidebar.selectbox(
#     'How would you like to be contacted?',
#     ('Email', 'Home phone', 'Mobile phone')
# )

# # Add a slider to the sidebar:
# add_slider = st.sidebar.slider(
#     'Select a range of values',
#     0.0, 100.0, (25.0, 75.0)
# )

# left_column, right_column = st.columns(2)
# # You can use a column just like st.sidebar:
# left_column.button('Press me!')

# # Or even better, call Streamlit functions inside a "with" block:
# with right_column:
#     chosen = st.radio(
#         'Sorting hat',
#         ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
#     st.write(f"You are in {chosen} house!")

# multiselect
# select_column = st.multiselect("Select columns to drop:",df.columns)

# Add a slider to the sidebar:
# add_slider = st.sidebar.slider(
#     'Select a range of values',
#     0.0, 100.0, (25.0, 75.0)
# )
# ---------------------------------------------

def read_file(file_path):
    global df
    try:
        # Check the file extension
        file_name = file_path.name
        file_extension = file_name.split(".")[-1]
        if file_extension not in ["xlsx", "csv"]:
            raise ValueError("Invalid file format! Please provide a file with .xlsx or .csv extension.")

        # Read the file
        if file_extension == "xlsx":
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path)

    except Exception as e:
        error_message = f"Error while reading file: {str(e)}"
        print(error_message)
        df = None
    
# ---- Create Model ---
with st.container():
    st.write("---")
    st.header("Let's build the smart model!")
    st.write("##")
    #adding a file uploader
    column_selection = st.radio("Select dataset", ("File", "URL"))

    # Display different content based on the selected column
    if column_selection == "File":
        # download_folder = os.path.expanduser("~/Downloads/Customer Call List.csv")
        file = st.file_uploader("Please choose a data file", type=["xlsx", "csv"], 
                                accept_multiple_files=False)
    else:
        file = st.text_input("URL of data file")
    
    if file is not None:
        data_load_state = st.text('Loading data...')
        # Get the file name and extension
        read_file(file)
        if df is not None:
            data_load_state.text('Loading data...done!')
            with st.container():
                dw.data_wrangling(df)
        else:
            st.error("Error while reading the file. Please check the file format and try again.")
