import streamlit as st
from google.cloud import firestore
import pandas as pd
import json
from google.oauth2 import service_account
from google.cloud.firestore import Client

key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="testrandom1-6cf06")

col = db.collection('users')
st.write(col.get())

for doc in col.stream():
    st.write(f'{doc.id} => {doc.to_dict()}')

doc_ref = db.collection('users').document('waliy')
doc = doc_ref.get()
docs = doc.to_dict()

st.write(doc.id)
df = pd.DataFrame(doc.to_dict(), index=[0])
st.write(df)