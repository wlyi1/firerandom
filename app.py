import streamlit as st
from google.cloud import firestore
import pandas as pd
import json
from google.oauth2 import service_account
from google.cloud.firestore import Client
import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import datetime
from datetime import datetime as dt
import pandas as pd
from io import BytesIO
import requests
import urllib.request
import textwrap
st.write('Test')
def _font_as_bytes():
    with open('https://raw.githubusercontent.com/wlyi1/random/main/Random/Quicksand-Regular.ttf', 'rb') as f:
        font_bytes = BytesIO(f.read())
    return font_bytes

key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="testrandom1-6cf06")



resp = requests.get('https://raw.githubusercontent.com/wlyi1/random/main/Random/rdt1.png')
image3 = Image.open(BytesIO(resp.content))

#Data Sources
data = pd.read_csv('rand_aktivitas.csv')
image1 = 'https://raw.githubusercontent.com/wlyi1/random/main/Random/a3a.png'
st.image(image1)

list_rand = data.name
tgl_random = datetime.datetime.now()
tgl = tgl_random.strftime("%m/%d/%Y, %H:%M:%S")
today_rand = random.choice(list_rand)

wrapper = textwrap.TextWrapper(width=30)
word = wrapper.wrap(text=today_rand)
hari = dt.today().strftime('%Y-%m-%d')
path_font = "Quicksand-Regular.ttf"
path_font_2 = 'Quicksand-Bold.ttf'
font = ImageFont.truetype(path_font, 55)
font1 = ImageFont.truetype(path_font_2, 32)

img= ImageDraw.Draw(image3)
img.text((450,390), hari, font=font1, fill=(0,0,0))
xc = 470
for i in word:
    img.text((80,xc), i, font=font, fill=(0,0,0))
    xc += 55

st.caption('Jangan lupa tag @randomku dan pake #random #randomku biar tau cerita menarikmu apa hari ini 🤣')

col = db.collection('waliy')
if st.button('Randomin'):
    st.image(image3)
    col.add({'Tanggal' : tgl_random, 'Random' : today_rand})
    st.balloons()


st.markdown("----", unsafe_allow_html=True)

db1 = firestore.Client(credentials=creds, project="testrandom1-6cf06")
col = db.collection('listrandom').document('wal')

with st.form("my_form"):
    st.write("Ceritain ke RandomKu dong tentang aktivitas randommu hari ini 😃")
    nama = st.text_input("Namanya? 🧑 👩")
    cerita = st.text_area("Cerita singkatnya gimana nih? ✍🏻")
    submitted = st.form_submit_button("Submit")

# If the user clicked the submit button. write the data from the form to the database.
# You can store any data you want here. Just modify that dictionary below (the entries between the {}).

if submitted:
    db1.put({"Nama": nama, "Cerita": cerita})
    st.write('Terimakasih 👍')



db_content = db.fetch().items
#st.write(db_content)
df = pd.DataFrame(db_content)
data_lis = df['Random'].value_counts()[:3].index.tolist()

st.header('3 Top Trending Randomku')
st.info(data_lis[0])
st.success(data_lis[1])
st.warning(data_lis[2])

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)