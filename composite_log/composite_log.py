'''
Main Program
Composite Log Viewer
Asep Hermawan, Nov 2024
'''

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image
import composite_logtemplates as logs

st.set_page_config(
    page_title="Composite Log",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_header(welldata):
    header = pd.read_excel(welldata, sheet_name='HEADER', engine='xlrd')
    return header
#end_function_load_header

def load_logdata(welldata):
    lwd = pd.read_excel(welldata, sheet_name='LOGDATA', engine='xlrd')
    df = lwd.ffill()           
    return df 
#end_function_load_logdata

def load_mudlog(welldata):
    mudlog = pd.read_excel(welldata, sheet_name='GASDATA', engine='xlrd')
    mudlog = mudlog.ffill() 
    return mudlog
#end_function_load_mudlog

def load_marker(welldata):
    marker = pd.read_excel(welldata, sheet_name='MARKER', engine='xlrd')
    marker = marker.ffill() 
    return marker
#end_function_load_marker

def load_survey(welldata):
    survey = pd.read_excel(welldata, sheet_name='SURVEY', engine='xlrd')
    survey = survey.ffill() 
    return survey
#end_function_load_survey

def load_fluid(welldata):
    fluid = pd.read_excel(welldata, sheet_name='FLUID', engine='xlrd')
    fluid = fluid.ffill() 
    return fluid
#end_function_load_fluid

def load_gaspeak(welldata):
    gaspeak = pd.read_excel(welldata, sheet_name='GASPEAK', engine='xlrd')
    gaspeak = gaspeak.ffill() 
    return gaspeak
#end_function_load_gaspeak

def show_top_sidebar(df):
     # Load the image
     st.sidebar.subheader("WELL DATA", divider=True)
     DepthMode =  st.sidebar.selectbox("Depth MODE", list(['MD','TVD', 'TVDSS']))
     st.sidebar.write("Adjust Scale, Top or Bottom log, if viewer ERROR due to unable creating long image")
     Skala = st.sidebar.selectbox("Scale", list([1000,500,200]))
     min = int(df['DEPTH'].min())
     max = int(df['DEPTH'].max())
     Depth_min = st.sidebar.slider('Top Log', min_value=min, max_value=max-100, value=min)
     Depth_max = st.sidebar.slider('Bottom Log', min_value=min+100, max_value=max, value=min+1000)
     return DepthMode, Skala, Depth_min, Depth_max
# #end_function_show_top_sidebar

def main():
    image = Image.open('./data/geostrat100.png')
    st.sidebar.image(image)

    st.sidebar.subheader("WELL DATA", divider=True)
    welldata = st.sidebar.file_uploader("Upload Pre-formated XLS well data file")
    if welldata is None:
       welldata = './data/asep03-welldata.xls'
    
    header = load_header(welldata)
    df = load_logdata(welldata)
    headerdata = header.iloc[0]
    WellName = headerdata['WELLNAME']
    Field = headerdata['FIELD']
    RTE = headerdata['RTE']
    East = headerdata['SURFACEX']
    North = headerdata['SURFACEY']
    Unit = headerdata['UNIT']
    
    # Show sidebar
    DepthMode, Skala, Depth_min, Depth_max = show_top_sidebar(df)
    mudlog = load_mudlog(welldata)
    judul = (WellName+" - Interval ("+str(Depth_min)+" - "+str(Depth_max)+")"+Unit+DepthMode+
            " - Scale 1:"+str(Skala))
    Depth_min = int(Depth_min)
    Depth_max = int(Depth_max)
    if Depth_max <= Depth_min:
        st.write('Bottom log must be greater than Top log....app reset bottom log')
        Depth_max = Depth_min+500
    skala = float(Skala)
    RTE = float(RTE)
   
    marker = load_marker(welldata)
    survey = load_survey(welldata)
    fluid = load_fluid(welldata)
    gaspeak = load_gaspeak(welldata)

    Depth_cm = (Depth_max - Depth_min)*100
    Log_length_cm = Depth_cm/skala
    Log_length_in = Log_length_cm/2.4

    panjang = Log_length_in
    lebar = 8
    majortick = 50
    minortick = 10
    
    st.markdown(f"<h2 style='text-align: center;'>WELL COMPOSITE LOG ({DepthMode})</h2>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>{WellName}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>Scale 1:{Skala}</h3>", unsafe_allow_html=True)
    st.markdown("""<hr style="height:2px;border-width:0;color:blue;background-color:gray">""", unsafe_allow_html=True)
    with st.container():
        cols1 = st.columns(4)    
        cols1[0].markdown(f"<h4 style='text-align: right;'>Easting: </h4>", unsafe_allow_html=True)
        cols1[1].markdown(f"<h4 style='text-align: left;'>{East}m</h4>", unsafe_allow_html=True)
        cols1[0].markdown(f"<h4 style='text-align: right;'>Northing: </h4>", unsafe_allow_html=True)
        cols1[1].markdown(f"<h4 style='text-align: left;'>{North}m</h4>", unsafe_allow_html=True)
        cols1[2].markdown(f"<h4 style='text-align: right;'>Field: </h4>", unsafe_allow_html=True)
        cols1[3].markdown(f"<h4 style='text-align: left;'>{Field}</h4>", unsafe_allow_html=True)
        cols1[2].markdown(f"<h4 style='text-align: right;'>RTE: </h4>", unsafe_allow_html=True)
        cols1[3].markdown(f"<h4 style='text-align: left;'>{RTE}{Unit}</h4>", unsafe_allow_html=True)
    st.markdown("""<hr style="height:2px;border-width:0;color:blue;background-color:gray">""", unsafe_allow_html=True)
    
    #st.write(judul)
    L = logs.LogTemplate(judul, panjang, lebar, majortick, minortick)
    L.show_triplecombo_composite(Depth_min, Depth_max, RTE, DepthMode, df, mudlog, marker, survey, fluid, gaspeak)    
        
if __name__ == "__main__":
     main()
















































