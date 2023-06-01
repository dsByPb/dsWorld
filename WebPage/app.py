import requests
import streamlit as st
from PIL import Image
from io import StringIO
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

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
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style/style.css")

# ---- LOAD ASSETS ----
lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
img_contact_form = Image.open("images/yt_contact_form.png")
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
    
def col_missing_info():
    # missing data in columns
    rows = st.columns(3)
    rows[0].markdown("### Is there?")
    rows[0].dataframe(df.isna().any())
    rows[1].markdown("### Count")
    rows[1].dataframe(df.isna().sum())
    rows[2].markdown("### Percentages")
    rows[2].dataframe(df.isna().sum()/len(df) * 100)

def row_missing_info():
    # missing data in row
    # st.write("Missing values count in each row: ", df.isna().sum(axis=1).values)
    st.write("Is there any row with at least one missing value: ", df.isnull().any(axis = 1).sum())
    st.write("how many rows are there with only missing values: ",df.isnull().all(axis = 1).sum())
    if df.isnull().all(axis = 1).sum() > 0:
        row_selection = st.radio("Would you like to drop the rows?", ("Yes", "No"), index = 1)
        if row_selection == "Yes":
            df.dropna(how='all', inplace=True)

def row_drop():
    # Check for duplicate rows
    duplicate_count = df.duplicated().sum()

    # Check if there are any duplicate rows
    if duplicate_count > 0:
        # Drop duplicate rows
        df.drop_duplicates(inplace=True)
        if duplicate_count == 1:
            st.write(duplicate_count, " duplicate row has been deleted.")
        else:
            st.write(duplicate_count, " duplicate rows have been deleted.")
    # st.write("Dropping rows where the non null values are less than a threshold value")
    # df_new.isnull().sum(axis=1).values
    # df_new.notnull().sum(axis=1).values
    # df3=df_new.dropna(thresh=3) #Remove rows where the number of non null values is less than 3
    # df3.head()
    # df3.notnull().sum(axis=1).values
    # print(len(df_new),len(df3))

    # # drop rows by index, if a column values is "Y" or drop if cell values is empty
    # for x in df.index:
    #     if df.loc[x,"colName"] == "Y":
    #         df.drop(x, inpalce=True)

def col_drop():
    # st.write("Columns with large percentages of missing values")
    missing_counts = df.isna().sum()
    max_missing_count = missing_counts.max()
    columns_with_max_missing = missing_counts[missing_counts == max_missing_count].index.tolist()
    columns_text = ', '.join(columns_with_max_missing)
    st.write("Columns with the maximum number of missing values:", columns_text)
    # st.write(columns_with_max_missing, " has ", max_missing_count, "% missing data.")
    col_selection = st.radio("Would you like to drop the columns?", ("Yes", "No"), index = 1)
    if col_selection == "Yes":
        df.drop(columns_with_max_missing, axis=1, inplace=True)
    st.write(df.isna().sum()/len(df) * 100)
    
    select_column = st.multiselect("Select columns to drop:",df.columns)
    df.drop(columns = select_column, inplace=True)

# Function to perform strip operations
def perform_strip_operations(df, selected_column, strip_operation, 
                             selected_transformation_types, specific_character):
    if specific_character:
        characters_list = specific_character.strip().split('and')
        characters_list = [character.strip() for character in characters_list]
        specific_string_to_transform = ''.join(characters_list)

    for transformation_type in selected_transformation_types:
        string_to_transform = None
        
        if transformation_type == "Strip Alphabets":
            string_to_transform = '[a-zA-Z]'
        elif transformation_type == "Strip Numericals":
            string_to_transform = '[0-9]'
        elif transformation_type == "Strip Special Characters":
            string_to_transform = '[^\W\s_]'
        elif transformation_type == "Strip Specific Character":
            # specific_character = st.text_input("Enter a specific character(separated by and) to strip")
            # if specific_character:
            #     characters_list = specific_character.strip().split('and')
            #     characters_list = [character.strip() for character in characters_list]
            #     string_to_transform = ''.join(characters_list)
            string_to_transform = specific_string_to_transform

        if string_to_transform is not None:
            if strip_operation == "left":
                df[selected_column] = df[selected_column].str.lstrip(string_to_transform)
            elif strip_operation == "right":
                df[selected_column] = df[selected_column].str.rstrip(string_to_transform)
            elif strip_operation == "full":
                df[selected_column] = df[selected_column].str.strip(string_to_transform)

    return df

def col_strip_operation(st, operation_key, operation_details):
    global df
    left_col, middle_col, right_col = st.columns(3)
    with left_col:
        column_names = ["None"] + df.columns.tolist()
        selected_column_key = operation_key + "_selected_column"
        # Select a column from the DataFrame
        selected_column = st.selectbox("Select a column for strip operation", 
                                    #    options=[None] + column_names, 
                                        options = column_names, 
                                        index = column_names.index(operation_details['selected_column']), 
                                        key=selected_column_key)

    with middle_col:
        strip_operation_key = operation_key + "_strip_operation"
        # Select the strip operation
        strip_operation = st.selectbox("Select a strip operation", 
                                        ["None", "left", "right", "full"], 
                                        index = ['None', 'left', 'right', 'full'].index(operation_details['strip_operation']), 
                                        key=strip_operation_key)

    with right_col:
        # Create a multiselect field with transformation types
        transformation_types = ["Strip Alphabets", "Strip Numericals", "Strip Special Characters", "Strip Specific Character"]
        selected_transformation_types_key = operation_key + "_selected_transformation_types"
        selected_transformation_types = st.multiselect("Select transformation types", 
                                                        transformation_types, 
                                                        default=operation_details['selected_transformation_types'], 
                                                        key=selected_transformation_types_key)
        specific_character_key = operation_key + "_specific_character"
        specific_character = st.text_input("Enter a specific character(separated by and) to strip", key=specific_character_key)
        
    # Update the operation details in the session state
    st.session_state.operations[operation_key]['selected_column'] = selected_column
    st.session_state.operations[operation_key]['strip_operation'] = strip_operation
    st.session_state.operations[operation_key]['selected_transformation_types'] = selected_transformation_types
    st.session_state.operations[operation_key]['specific_character'] = specific_character

    # Perform strip operations on button click
    if st.button("Apply Strip" + operation_key):
        # Get the operation details
        selected_column = operation_details['selected_column']
        strip_operation = operation_details['strip_operation']
        selected_transformation_types = operation_details['selected_transformation_types']
        specific_character = operation_details['specific_character']

        
        # Process the strip operations
        df = perform_strip_operations(df, selected_column, strip_operation,
                                    selected_transformation_types, specific_character)
        # Display the updated DataFrame
        st.dataframe(df)
      


def replace_operation():
    # df['Phone_Number'] = df['Phone_Number'].str.replace('[â-ZA-Z0-9]','') # except alphabets and numeric, everything else
    # Yes with Y and No with N
    pass

def split_operation():
    # Split operation logic goes here
    # split by comma and create new columns (address)
    pass

def perform_operations():
    global df
    # Create a session state to store the operations
    if 'operations' not in st.session_state:
        st.session_state.operations = {}

    # Create a button to add more operations
    if st.button("Add Operation"):
        # Create a unique key for the caching mechanism
        operation_key = str(len(st.session_state.operations)+1)

        # Store the operation details in the session state
        st.session_state.operations[operation_key] = {
            'selected_column': "None",
            'strip_operation': "None",
            'selected_transformation_types': [],
            'specific_character': ""
        }
    
    # Display the expander sections for each operation
    for operation_key, operation_details in st.session_state.operations.items():
        with st.expander("Operation " + operation_key):
            # Based on radio button selection, call the respective method
            selected_operation = st.radio(
                "Select an operation",
                options=["None", "Strip", "Replace", "Split"],
                index=0
            )

            if selected_operation == "Strip":
                col_strip_operation(st, operation_key, operation_details)
            elif selected_operation == "Replace":
                replace_operation()
            elif selected_operation == "Split":
                split_operation()

def fillNA():
    st.write(df.isnull().sum())
    user_choice = st.selectbox(
    'How do you like to deal with missing values?',
    ('Pleae select',
    'Filling missing values with a particular value',
    'Missing values of a particular column can be treated separately',
    'Forward filling',
    'Backward filling',
    'Interpolate Numerical missing values'))
    
    if user_choice == "Filling missing values with a particular value":
        df4=df.fillna(0)
        st.dataframe(df4.head())
    elif user_choice == "Missing values of a particular column can be treated separately":
        df5=df.copy()
        df5.head()
        df5["Species"].fillna("Unknown",inplace=True) #Filling missing values in Species column with Unknown
        df5.head()
        df5["Sepal.Length"].fillna(df5["Sepal.Length"].mean(),inplace=True) #Filling missing values in Sepal Length column with average
        df5.head()
    elif user_choice == "Forward filling":
        df6=df.fillna(method="ffill")
        df6.head()
        df6=df_new.fillna(method="pad")
        df6.head()
    elif user_choice == "Backward filling":
        df7=df.fillna(method="bfill")
        df7.head()
    elif user_choice == "Interpolate Numerical missing values":
        df8=df[['Sepal.Length', 'Sepal.Width', 'Petal.Length']]
        df8.head()
        df9=df8.interpolate(method ='linear', limit_direction ='forward')
        df9.head()

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
        else:
            st.error("Error while reading the file. Please check the file format and try again.")
        
        if st.checkbox("Tabular Data"):
            st.table(df.head(10))

        if st.checkbox("Statistical Summary"):
            st.table(df.describe())

        if st.checkbox("Correlation graph"):
            fig,ax = plt.subplots(figsize=(5,2.5))
            sns.heatmap(df.corr(),annot=True,cmap="coolwarm")
            st.pyplot(fig)

        if st.checkbox("Other graphs"):
            graph = st.selectbox("Different types of graph",["Scatter plot", "Bar graph", "Histogram"])
            if graph == "Scatter plot":
                pass
                # value = st.slider("Filter data using Sepal Length",4,8)
                # data = df.loc[df["SepalLengthCm"]>= value]
                # fig,ax=plt.subplots(figsize=(10,5))
                # sns.scatterplot(data = data, x= "SepalLengthCm", y="Species", hue="PetalLengthCm")
                # st.pyplot(fig)
            if graph == "Bar graph":
                pass
                # fig,ax=plt.subplots(figsize=(3.5,2))
                # sns.barplot(data = df, x= "SepalLengthCm", y=df.PetalLengthCm.index)
                # st.pyplot(fig)
            if graph == "Histogram":
                pass
                # fig,ax=plt.subplots(figsize=(5,3))
                # sns.distplot(df.SepalLengthCm,kde=True)
                # st.pyplot(fig)

        if st.checkbox("Handle missing values"):
            st.subheader("Checking missing values")
            col_missing_info()  
            row_missing_info()        
            user_choice = st.selectbox(
                'How do you like to deal with missing record?',
                ('Pleae select','Drop','Fill'))
            df_new = df.copy() # unwanted -------------
            if user_choice == "Drop":
                row_drop()
                col_drop()
                # df = col_strip_operation()  # Call col_strip_operation initially
                perform_operations()  # Call perform_operations to handle radio button selection and add operation functionality

                selected_operation = st.radio(
                    "Would you like to fill the missing values?",
                    options=["Yes", "No"],
                    index=1
                )
                if selected_operation == "Yes":
                    fillNA()

            elif user_choice == "Fill":
                fillNA()

            df = df.reset_index(drop=True)

            # st.subheader("Dealing with outliers")
            # # Detecting outliers using a boxplot
            # boxplot=df.boxplot(column=["Sepal.Length","Sepal.Width","Petal.Length","Petal.Width"]) #Sepal Width has really large values
            # # Detecting outliers using 1.5*IQR rule
            # Q1 = df.quantile(0.25)
            # Q3 = df.quantile(0.75)
            # IQR = Q3 - Q1
            # print(IQR)
            # (df < (Q1 - 1.5 * IQR)) |(df > (Q3 + 1.5 * IQR))
            # # Removing outliers
            # # This will return True for all the rows which have at least one outof bound row
            # out_rows=((df < (Q1 - 1.5 * IQR)) |(df > (Q3 + 1.5 * IQR))).any(axis=1) 
            # out_rows
            # df_out=df[~out_rows]
            # df_out.head()
            # print(len(df),len(df_out))

            # st.subheader("Dealing with data types in columns")
            # df=pd.read_csv("D:\\Workshops\\Data Manipulation & Cleaning with Python & R\\Data Cleaning with Python\\Datasets\\iris - ColumnTypes.CSV")
            # df
            # arr=df["Sepal.Length"].values #Creating an array
            # valstr=",".join(list(arr)) #Create a single string
            # valstr
            # valstr2=valstr.replace('"',"") #Replace double quotations with empty strings
            # valstr2
            # vlist=valstr2.split(",") #Create a string list
            # vlist
            # varr=np.array(vlist) #Create an array
            # varr
            # df["Sepal.Length"]=varr.astype(float) #Convert the strings into floats
            # df

            # st.subheader("Spliiting columns")
            # df=pd.read_csv("D:\\Workshops\\Data Manipulation & Cleaning with Python & R\\Data Cleaning with Python\\Datasets\\iris - SplittingColumns.CSV")
            # df
            # L=list(df["Sepal Width & Length"].values)
            # L
            # L1=[st.split(",")[0] for st in L]
            # L2=[st.split(",")[1] for st in L]
            # arr1=np.array(L1)
            # arr2=np.array(L2)
            # df.drop("Sepal Width & Length",axis=1,inplace=True)
            # df["Sepal.Width"]=arr1.astype(float)
            # df["Sepal.Length"]=arr2.astype(float)
            # df

            # st.subheader("Special Data Preprocessing")
            # import pandas as pd
            # import numpy as np
            # from sklearn.preprocessing import LabelEncoder, OneHotEncoder #For encoding categorical variables
            # from sklearn.preprocessing import StandardScaler

            # # Sliding Window
            # data=pd.DataFrame({"Date":["2021-01-01","2021-01-02","2021-01-03","2021-01-04","2021-01-05","2021-01-06","2021-01-07"],
            #                 "Price":[100,200,150,250,300,200,170]})
            # data
            # # next_price consist of value of next row data
            # data["Next_Price"]=np.roll(data["Price"].values,-1)
            # data
            # # drop last row, as the record already exist in previous row
            # data.drop(6,inplace=True)
            # data

            # # Standardizing
            # data=pd.DataFrame({"Height":[1.24,1.34,1.45,0.67,1.66],
            #                 "Width":[56,45,67,78,45]})
            # data
            # df1=data.apply(lambda x:(np.array(x)-np.array(x).mean())/np.array(x).std())
            # df1
            # ssc=StandardScaler()
            # mat_ssc=ssc.fit_transform(data)
            # mat_ssc
            # df2=pd.DataFrame(mat_ssc,columns=["Height","Width"])
            # df2











