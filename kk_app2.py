import pandas as pd
import streamlit as st
from elasticsearch import Elasticsearch
import re
from IPython.display import Audio
import base64
# Connect to Elasticsearch
es = Elasticsearch(hosts=[{"host": "35.226.245.142", "port": 9200, "scheme": "http"}])

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def search(query=None, tel_query=None, agent_query=None, time_durationclip_query=None, time_durationclip_query2=None , datetime_query= None,end_date=None):
    must = []
    if query:
        must.append({"match": {"text_field": query}})
    if tel_query:
        must.append({"match": {"tel": tel_query}})
    if agent_query:
        must.append({"match": {"agent": agent_query}})
    if time_durationclip_query:
        must.append({"range": {"time_durationclip": {"gte": time_durationclip_query}}})
    if time_durationclip_query2:
        must.append({"range": {"time_durationclip": {"lte": time_durationclip_query2}}})
    if datetime_query:
        must.append({"range": {"datetime": {"gte": datetime_query, "lte": end_date}}})
        
    body = {
        "size":20,
        "query": {
            "bool": {
                "must": must
            }
        }
    }
    results = es.search(index="botnoi4", body=body)
    return results["hits"]["hits"]



def search_app():

    st.subheader('Search')
    col1, col2, col3 , col4 ,col5,col6= st.columns(6)
    
    query = None
    agent_query = None
    tel_query = None
    time=None
    datetime = None
    end_datetime = None

    with col1:
        query = st.text_input("Enter search query:")
    with col2:
        agent_query = st.text_input("Enter agent name:")

    with col3:
        tel_query = st.text_input("Enter Customer id")

    with col4:
        time, time2 = st.slider(
            'Enter Duration',
            0.0, 100.0, (25.0, 75.0))
    with col5:
        datetime = st.date_input("Enter start date")

        # Convert date to datetime object
    with col6:
        end_datetime = st.date_input("Enter end date")
        
    if st.button('Search'):
        # perform the search and retrieve the results
        results = search(query=query,tel_query=tel_query, agent_query=agent_query, time_durationclip_query=time,time_durationclip_query2=time2, datetime_query=datetime,end_date=end_datetime)

        if results:
            st.write(len(results))
            for result in results:
                show = []
                text = result["_source"]["text_field"]
                agent = result["_source"]["agent"]
                tel = result["_source"]["tel"]
                time = result["_source"]["time_durationclip"]
                audio_url = result["_source"]["audio_url"]
                datetime = result["_source"]["datetime"]
#                 data = {'time':list(time),'tel':list(tel),'agent':agent,'audio_url':audio_url,'text':text}
#                 df = pd.DataFrame(data)
#                 st.dataframe(df)
                # Display the text and audio player
                
#                 st.write("- " + str(time))
#                 st.write("- " + tel)
#                 st.write("- " + agent)
#                 st.write(Audio(audio_url))
#                 st.write("- " + text)
                
                col1, col2, col3, col4, col5,col6 = st.columns((6, 2, 4, 2, 2,4), gap='medium')
                with col4:
                    st.write(str(time))
                with col3:
                    st.write(tel)
                with col2:
                    st.write(agent)
                with col1:
                    text = text.replace(query, f"<span style='color: red;'>{query}</span>")
                    st.markdown(text, unsafe_allow_html=True)
                with col5 :
                    st.write(datetime)
                with col6:
                    st.write(Audio(audio_url))
                    
            text = [result['_source']['text_field'] for result in results]
            agent = [result['_source']['agent'] for result in results]
            tel = [result['_source']['tel'] for result in results]
            time = [result['_source']['time_durationclip'] for result in results]
            audio_url = [result['_source']['audio_url'] for result in results]
            datetime =  [result['_source']['datetime'] for result in results]
            data = {'time_durationclip':time,'tel':tel,'agent':agent,'audio_url':audio_url,'text':text,'datetime':datetime}            
            df = pd.DataFrame(data)
            st.dataframe(df)
        else:
            st.write("No results found")
            
        csv = convert_df(df)
        
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='data.csv',
            mime='text/csv',
        )


st.set_page_config(layout="wide")

st.title('Contact Center APP')
# tab1, tab2,  = st.tabs(["Upload", "Search"])

# with tab1:
#     st.subheader('Update Data')
#     with st.form("my_form", clear_on_submit=True):
#         txt_1 = st.text_input('Text')
#         agent_1 = st.text_input('Agent Name')
#         tel_1 = st.text_input('Telephone Number')
#         # aud_1 = st.file_uploader('Upload audio')
#         aud_1 = st.text_input('Upload audio')
#         submitted = st.form_submit_button("Submit")

#         if submitted:

#             doc1 = {'text_field':txt_1,'agent':agent_1,'tel':tel_1,'audio_url': aud_1}
#             es.index(index='botnoi1', body=doc1)
#             es.indices.refresh(index='botnoi1')
#             st.success('Your form has been submitted!')


# with tab2:
#     search_app()
# run the search app
search_app()
