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
import streamlit.components.v1 as components
from streamlit.components.v1 import html
from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard, create_share_link, get_geolocation
import time

import random

showErrorDetails = False

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

tab1, tab2, tab3 = st.tabs(['Kegiatan Random ⏳', 'Makan Terserah 🍵', 'Pilih Orang 😮‍💨'])
with tab1:

    st.image(image1)
    st.caption('Jangan lupa tag @randomku dan pake #random #randomku biar tau cerita randommu hari ini 🤣')

    col = db.collection('waliy')
    if st.button('Randomin'):
        st.image(image3)
        col.add({'Tanggal' : tgl_random, 'Random' : today_rand})
        st.balloons()


    st.markdown("----", unsafe_allow_html=True)

    db1 = firestore.Client(credentials=creds, project="testrandom1-6cf06")
    col1 = db.collection('Story_waliy')

    with st.form("my_form"):
        st.write("Ceritain ke RandomKu dong tentang aktivitas randommu hari ini 😃")
        nama = st.text_input("Namanya? 🧑 👩")
        cerita = st.text_area("Cerita singkatnya gimana nih? ✍🏻")
        submitted = st.form_submit_button("Submit")
        if submitted:
            col1.add({"Tanggal": tgl_random, "Cerita": cerita})
            st.write('Terimakasih 👍')
    # If the user clicked the submit button. write the data from the form to the database.
    # You can store any data you want here. Just modify that dictionary below (the entries between the {}).



    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

with tab2:
    
    try:
        st.header('Yang mau makan masih bilang terserah, sini random kan aja pilihan makannya!')
        st.write('nyalain dulu GPS nya dan izinkan')
        if st.checkbox("Cek Lokasiku"):
            loc = get_geolocation()
            with st.spinner('waiting'):
                time.sleep(5)

            #st.write(f"Your coordinates are {loc}")
            #st.write(loc['coords']['latitude'])
            #st.write(loc['coords']['longitude'])
            try:
                lat_user = loc['coords']['latitude']
                long_user = loc['coords']['longitude']
            except TypeError:
                st.write(" ")
        gmaps = st.secrets['gmaps']
        foods = ['rumah+makan', 'pecel', 'nasi+goreng', '']
        
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat_user}%2C{long_user}&radius=1500&types=restaurant&language=id&key={gmaps}"

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers = headers, data = payload)
        res = response.json()
        #st.write(res)
        total = len(res['results'])
        num = [x for x in range(total)]
        #st.write(num)
        ran_num = random.choice(num)

        lat = res['results'][ran_num]['geometry']['location']['lat']
        long = res['results'][ran_num]['geometry']['location']['lng']

        lis = []
        for i in range(total):
            j = res['results'][i]['name']
            lis.append(j)

        #st.write(lat)
        #st.write(lis)
        st.subheader(lis[ran_num])
        data = {'lat': [lat], 'lon': [long]}
        dfmap = pd.DataFrame(data)
        #st.write(dfmap)
        #st.map(dfmap)
        components.iframe(width=600,  height=450, src=f"https://www.google.com/maps/embed/v1/place?key={gmaps}&q={lat}, {long}")
    
    except NameError:
        st.success('Welcome To Randomku')

with tab3:
    @st.cache(allow_output_mutation=True)
    def get_data_input():
        return[]
    
    st.subheader('Pilih Nama Secara Random')
    
    nama = st.text_input('Tulisin namanya siapa aja (pisakan dengan tanda koma) ')
    lis_nama = nama.split(",")
    no = random.choice([i for i in range(lis_nama)])
    if st.button('Pilih Nama'):
        st.write(lis_nama[no])