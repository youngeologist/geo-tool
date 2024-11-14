import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
import composite_logtemplates as logs

st.set_page_config(
    page_title="Composite Log",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)
welldata = './data/asep03-data.xls'
@st.cache_data
def load_header(welldata):
    header = pd.read_excel(welldata, sheet_name='HEADER', engine='xlrd')
    return header
#end_function_load_header

def load_lwddata(welldata):
    lwd = pd.read_excel(welldata, sheet_name='LOGDATA', engine='xlrd')
    df = lwd.fillna(method='ffill')            
    return df 
#end_function_load_lwddata

def load_mudlog(welldata):
    mudlog = pd.read_excel(welldata, sheet_name='MUDLOG', engine='xlrd')
    return mudlog
#end_function_load_mudlog

def load_marker(welldata):
    marker = pd.read_excel(welldata, sheet_name='MARKER', engine='xlrd')
    return marker
#end_function_load_marker

def load_survey(welldata):
    survey = pd.read_excel(welldata, sheet_name='SURVEY', engine='xlrd')
    return survey
#end_function_load_survey

def load_fluid(welldata):
    fluid = pd.read_excel(welldata, sheet_name='FLUID', engine='xlrd')
    return fluid
#end_function_load_fluid

def load_gaspeak(welldata):
    gaspeak = pd.read_excel(welldata, sheet_name='GASPEAK', engine='xlrd')
    return gaspeak
#end_function_load_gaspeak

def show_top_sidebar(df):
     #RTE = st.sidebar.text_input("RTE","28.4")
     DepthMode =  st.sidebar.selectbox("Depth MODE", list(['MD','TVD', 'TVDSS']))
     st.sidebar.write("Adjust Scale, Top or Bottom log, if viewer ERROR due to unable handling large image")
     Skala = st.sidebar.selectbox("Scale", list([1000,500,200]))
     min = int(df['DEPTH'].min())
     max = int(df['DEPTH'].max())
     Depth_min = st.sidebar.text_input("Top", min)
     Depth_max = st.sidebar.text_input("Bottom", max)
     return DepthMode, Skala, Depth_min, Depth_max
# #end_function_show_top_sidebar

def main():
    st.sidebar.markdown("<h4 style='text-align: center;'>COMPOSITE LOG VIEWER by Asep Hermawan</h4>", unsafe_allow_html=True)
    st.sidebar.subheader("E-Log/LWD File", divider=True)
    welldata = st.sidebar.file_uploader("Upload E-Log/LWD file")
    header = load_header(welldata)
    df = load_lwddata(welldata)
    headerdata = header.iloc[0]
    RTE = headerdata['RTE']
    DepthMode, Skala, Depth_min, Depth_max = show_top_sidebar(df)
    mudlog = load_mudlog(welldata)
    judul = (headerdata['WELLNAME']+" -- Interval ("+str(Depth_min)+" - "+str(Depth_max)+")"+DepthMode+
            " -- Scale 1:"+str(Skala)+" -- RTE: "+str(RTE)+"m")
    Depth_min = int(Depth_min)
    Depth_max = int(Depth_max)
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
    
    st.markdown("<h1 style='text-align: center;'>WELL COMPOSITE LOG</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>{headerdata['WELLNAME']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>Field: {headerdata['FIELD']}</h3>", unsafe_allow_html=True)
    st.markdown("""<hr style="height:2px;border-width:0;color:blue;background-color:gray">""", unsafe_allow_html=True)
    st.write(judul)
    L = logs.LogTemplate(judul, panjang, lebar, majortick, minortick)
    L.show_triplecombo_composite(Depth_min, Depth_max, RTE, DepthMode, df, mudlog, marker, survey, fluid, gaspeak)    
        
if __name__ == "__main__":
     main()
















































