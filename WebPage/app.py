import requests
import streamlit as st
# from streamlit_lottie import st_lottie
from PIL import Image
from io import StringIO
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
    st.title("A Data Scientist From India")
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
# ---------------------------------------------

# # ---- WHAT I DO ----
# with st.container():
#     st.write("---")
#     left_column, right_column = st.columns(2)
#     with left_column:
#         st.header("What I do")
#         st.write("##")
#         st.write(
#             """
#             On my YouTube channel I am creating tutorials for people who:
#             - are looking for a way to leverage the power of Python in their day-to-day work.
#             - are struggling with repetitive tasks in Excel and are looking for a way to use Python and VBA.
#             - want to learn Data Analysis & Data Science to perform meaningful and impactful analyses.
#             - are working with Excel and found themselves thinking - "there has to be a better way."

#             If this sounds interesting to you, consider subscribing and turning on the notifications, so you don’t miss any content.
#             """
#         )
#         st.write("[YouTube Channel >](https://youtube.com/c/CodingIsFun)")
#     # with right_column:
#     #     st_lottie(lottie_coding, height=300, key="coding")

# # ---- PROJECTS ----
# with st.container():
#     st.write("---")
#     st.header("My Projects")
#     st.write("##")
#     image_column, text_column = st.columns((1, 2))
#     with image_column:
#         st.image(img_lottie_animation)
#     with text_column:
#         st.subheader("Integrate Lottie Animations Inside Your Streamlit App")
#         st.write(
#             """
#             Learn how to use Lottie Files in Streamlit!
#             Animations make our web app more engaging and fun, and Lottie Files are the easiest way to do it!
#             In this tutorial, I'll show you exactly how to do it
#             """
#         )
#         st.markdown("[Watch Video...](https://youtu.be/TXSOitGoINE)")
# with st.container():
#     image_column, text_column = st.columns((1, 2))
#     with image_column:
#         st.image(img_contact_form)
#     with text_column:
#         st.subheader("How To Add A Contact Form To Your Streamlit App")
#         st.write(
#             """
#             Want to add a contact form to your Streamlit website?
#             In this video, I'm going to show you how to implement a contact form in your Streamlit app using the free service ‘Form Submit’.
#             """
#         )
#         st.markdown("[Watch Video...](https://youtu.be/FOULV9Xij_8)")

# # ---- CONTACT ----
# with st.container():
#     st.write("---")
#     st.header("Get In Touch With Me!")
#     st.write("##")

#     # Documention: https://formsubmit.co/ !!! CHANGE EMAIL ADDRESS !!!
#     contact_form = """
#     <form action="https://formsubmit.co/YOUR@MAIL.COM" method="POST">
#         <input type="hidden" name="_captcha" value="false">
#         <input type="text" name="name" placeholder="Your name" required>
#         <input type="email" name="email" placeholder="Your email" required>
#         <textarea name="message" placeholder="Your message here" required></textarea>
#         <button type="submit">Send</button>
#     </form>
#     """
#     left_column, right_column = st.columns(2)
#     with left_column:
#         st.markdown(contact_form, unsafe_allow_html=True)
#     with right_column:
#         st.empty()

# ---- Create Model ---
with st.container():
    st.write("---")
    st.header("Let's build the smart model!")
    st.write("##")
    #adding a file uploader
    file = st.file_uploader("Please choose a file")
    if file is not None:
        data_load_state = st.text('Loading data...')
        #To read file as bytes:
        bytes_data = file.getvalue()
        # st.write(bytes_data)
        #To convert to a string based IO:
        stringio = StringIO(file.getvalue().decode("utf-8"))
        # st.write(stringio)
        #To read file as string:
        string_data = stringio.read()
        # st.write(string_data)
        #Can be used wherever a "file-like" object is accepted:
        df= pd.read_csv(file)
        data_load_state.text('Loading data...done!')
        # st.write("Tabular Data represenatation:")
        if st.checkbox("Tabular Data"):
            st.table(df.head(100))
        if st.checkbox("Statistical Summary"):
            st.table(df.describe())
        if st.checkbox("Correlation graph"):
            fig,ax = plt.subplots(figsize=(5,2.5))
            sns.heatmap(df.corr(),annot=True,cmap="coolwarm")
            st.pyplot(fig)
        graph = st.selectbox("Different types of graph",["Scatter plot", "Bar graph", "Histogram"])
        if graph == "Scatter plot":
            value = st.slider("Filter data using Sepal Length",4,8)
            data = df.loc[df["SepalLengthCm"]>= value]
            fig,ax=plt.subplots(figsize=(10,5))
            sns.scatterplot(data = data, x= "SepalLengthCm", y="Species", hue="PetalLengthCm")
            st.pyplot(fig)
        if graph == "Bar graph":
            fig,ax=plt.subplots(figsize=(3.5,2))
            sns.barplot(data = df, x= "SepalLengthCm", y=df.PetalLengthCm.index)
            st.pyplot(fig)
        if graph == "Histogram":
            fig,ax=plt.subplots(figsize=(5,3))
            sns.distplot(df.SepalLengthCm,kde=True)
            st.pyplot(fig)

        if st.checkbox("Handle missing values"):
            st.subheader("Checking missing values")

            rows = st.columns(3)
            rows[0].markdown("### Is there?")
            rows[0].dataframe(df.isna().any())
            rows[1].markdown("### Count")
            rows[1].dataframe(df.isna().sum())
            rows[2].markdown("### Percentages")
            rows[2].dataframe(df.isna().sum()/len(df))

            # st.write("Is there any column with at least one missing value: ", df.isna().any())
            # st.write("Missing values count in each column: ", df.isna().sum())
            # st.write("Percentages of missing values in each column: ", df.isna().sum()/len(df))
            st.write("Missing values count in each row: ", df.isna().sum(axis=1).values)
            st.write("Is there any row with at least one missing value: ", df.isnull().any(axis = 1).sum())
            st.write("how many rows are there with only missing values: ",df.isnull().all(axis = 1).sum())
            
            labels = "SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm", "Species"
            sizes = [2, 3, 0, 0, 1]
            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=False, startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            st.pyplot(fig1)

            user_choice = st.selectbox(
                'How do you like to deal with missing record?',
                ('Pleae select','Drop','Fill'))
            # st.write('You selected:', user_choice)
            df_new = df.copy()
            if user_choice == "Drop":
                st.write("Dropping columns with large percentages of missing values")
                st.write(df.isna().sum().idxmax())
                df_new=df_new.drop(df.isna().sum().idxmax(),axis=1)
                df_new.head() # use df_new ahead

                # st.write("Dropping rows with at least one missing value")
                # df1=df_new.dropna(how="any")
                # df1.head()

                # df1.isna().any() #No missing values

                st.write("Dropping rows if all values in that row are missing values (Rows with only missing values)")
                df2=df_new.dropna(how="all")
                df2.head()
                # print(len(df_new),len(df2)) #The row with only missing values has been removed

                # st.write("Dropping rows where the non null values are less than a threshold value")
                # df_new.isnull().sum(axis=1).values
                # df_new.notnull().sum(axis=1).values
                # df3=df_new.dropna(thresh=3) #Remove rows where the number of non null values is less than 3
                # df3.head()
                # df3.notnull().sum(axis=1).values
                # print(len(df_new),len(df3))

                # -----------Fill
                user_choice1 = st.selectbox(
                'How do you like to deal further?',
                ('Pleae select','Fill'))
                if user_choice1 == "Fill":
                    st.write(df_new.isnull().sum())
                    user_choice2 = st.selectbox(
                    'How do you like to deal further?',
                    ('Pleae select',
                    'Filling missing values with a particular value',
                    'Missing values of a particular column can be treated separately',
                    'Forward filling',
                    'Backward filling',
                    'Interpolate Numerical missing values'))
                    
                    if user_choice2 == "Filling missing values with a particular value":
                        df4=df_new.fillna(0)
                        df4.head()
                    elif user_choice2 == "Missing values of a particular column can be treated separately":
                        df5=df_new.copy()
                        df5.head()
                        df5["Species"].fillna("Unknown",inplace=True) #Filling missing values in Species column with Unknown
                        df5.head()
                        df5["Sepal.Length"].fillna(df5["Sepal.Length"].mean(),inplace=True) #Filling missing values in Sepal Length column with average
                        df5.head()
                    elif user_choice2 == "Forward filling":
                        df6=df_new.fillna(method="ffill")
                        df6.head()
                        df6=df_new.fillna(method="pad")
                        df6.head()
                    elif user_choice2 == "Backward filling":
                        df7=df_new.fillna(method="bfill")
                        df7.head()
                    elif user_choice2 == "Interpolate Numerical missing values":
                        df8=df_new[['Sepal.Length', 'Sepal.Width', 'Petal.Length']]
                        df8.head()
                        df9=df8.interpolate(method ='linear', limit_direction ='forward')
                        df9.head()
            elif user_choice == "Fill":
                st.write(df_new.isnull().sum()) 
            
            st.subheader("Checking Duplicated rows")
            df.duplicated() #This returns True for duplicated rows
            df.duplicated().sum() #This returns the number of duplicated rows
            len(df)
            # Dropping duplicated rows
            df.drop_duplicates(inplace=True)
            df.head()
            df.duplicated().sum()
            len(df)

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











