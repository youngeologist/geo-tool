# Korelasi marker antar sumur
# Asep Hermawan
# November 2024
#--------------------------------

from correlation import Korelasi
import pandas as pd
import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Well Correlation",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
# baca file data
def load_header(welldata):
    header = pd.read_excel(welldata, sheet_name='HEADER')
    header = header.fillna(method='ffill')
    return header
#end_function_load_header

def load_logdata(welldata):
    dflog = pd.read_excel(welldata, sheet_name='LOGDATA')
    df = dflog.fillna(method='ffill')            
    return df 
#end_function_load_lwddata

def load_marker(welldata):
    marker = pd.read_excel(welldata, sheet_name='MARKER')
    marker = marker.fillna(method='ffill')
    return marker
#end_function_load_marker

def create_correlation(df_marker1, df_marker2, delta1, delta2):
    merged_df = pd.merge(df_marker1, df_marker2, on='MARKER')
    df_marker_merge = merged_df[['MARKER', 'TVDSS_x', 'TVDSS_y']] 
    df_marker_merge.columns = ['MARKER', 'TVDSS1', 'TVDSS2']
    connectlines = []
    for i, depth in df_marker_merge.iterrows():
        connectlines.append([(0, depth['TVDSS1']-delta1), (10, depth['TVDSS2']-delta2)])
    return connectlines
#end_function_create_correlation

def flat_depth(marker, marker1, marker2, marker3, marker4):
    
    flatdepth = marker1.loc[(marker1['MARKER'] == marker), 'TVDSS']
    welldepth2 = marker2.loc[(marker2['MARKER'] == marker), 'TVDSS']
    welldepth3 = marker3.loc[(marker3['MARKER'] == marker), 'TVDSS']
    welldepth4 = marker4.loc[(marker4['MARKER'] == marker), 'TVDSS']
    
    delta1 = float(welldepth2) - float(flatdepth)
    delta2 = float(welldepth3) - float(flatdepth)
    delta3 = float(welldepth4) - float(flatdepth)                             
    return delta1, delta2, delta3
    
#end_function_flat_depth

def main():
    image = Image.open('../data/geostrat100.png')
    st.sidebar.image(image)
    # read log data
    welldata01 = st.sidebar.file_uploader("Upload Well-1 file")
    if welldata01 is None:
       welldata01 = '../data/dummy01_correlation.xls'
    WellName1 = load_header(welldata01)
    wellname1 = WellName1.iloc[0]

    welldata02 = st.sidebar.file_uploader("Upload Well-2 file")
    if welldata02 is None:
       welldata02 = '../data/dummy02_correlation.xls'
    WellName2 = load_header(welldata02)
    wellname2 = WellName2.iloc[0]

    welldata03 = st.sidebar.file_uploader("Upload Well-3 file")
    if welldata03 is None:
       welldata03 = '../data/dummy03_correlation.xls'
    WellName3 = load_header(welldata03)
    wellname3 = WellName3.iloc[0]

    welldata04 = st.sidebar.file_uploader("Upload Well-4 file")
    if welldata04 is None:
       welldata04 = '../data/dummy04_correlation.xls'
    WellName4 = load_header(welldata04)
    wellname4 = WellName4.iloc[0]
        
    welldata1 = load_logdata(welldata01)
    welldata2 = load_logdata(welldata02)
    welldata3 = load_logdata(welldata03)
    welldata4 = load_logdata(welldata04)

    #baca file marker
    marker1 = load_marker(welldata01)
    marker2 = load_marker(welldata02)
    marker3 = load_marker(welldata03)
    marker4 = load_marker(welldata04)
    
    # Merged all marker in well to select only same marker to be connected by marker line
    merged_marker0 = pd.merge(marker1, marker2, on='MARKER')
    merged_marker1 = pd.merge(marker3, marker4, on='MARKER')
    merged_marker2 = pd.merge(merged_marker0, merged_marker1, on='MARKER')

    # Add WELLDEPTH to merged_marker to be displayed on selectbox
    add_marker = pd.DataFrame({'MARKER': ['WELL DEPTH'], 'TVDSS': [0]})
    merged_marker = pd.concat([add_marker, merged_marker2], ignore_index=True)
    #------------------------
    skala = 1000
    min = 100
    max = 600
    FillGR = 'NO'
    ShBaseLine = 75
    #------------------------
    skala = st.sidebar.selectbox("Set Scale", list([1000,500]))
    mindepth = st.sidebar.text_input("Top", min)
    maxdepth = st.sidebar.text_input("Bottom", max)
    mindepth = int(mindepth)  
    maxdepth = int(maxdepth)
    skala = int(skala) 

    if maxdepth <= mindepth :  
       maxdepth = mindepth + 500
       st.write('Bottom must be greater than Top')

    flatmarker = st.sidebar.selectbox("Flat log on marker", list(merged_marker['MARKER']))
    FillGR = st.sidebar.selectbox("Fill GR below Shale Baseline?", list(['NO','YES']))
    # ShaleBaseLine = st.sidebar.text_input("Shale Base Line", ShBaseLine)
    cols = st.columns(4)
    #ShaleBaseLine = st.sidebar.slider('Shale Base Line', min_value=0, max_value=150, value=75)
    ShaleBaseLine1 = cols[0].slider('Shale Baseline-1', min_value=0, max_value=150, value=75)
    ShaleBaseLine2 = cols[1].slider('Shale Baseline-2', min_value=0, max_value=150, value=75)
    ShaleBaseLine3 = cols[2].slider('Shale Baseline-3', min_value=0, max_value=150, value=75)
    ShaleBaseLine4 = cols[3].slider('Shale Baseline-4', min_value=0, max_value=150, value=75)
    ShaleBaseLine1 = int(ShaleBaseLine1)
    ShaleBaseLine2 = int(ShaleBaseLine2)
    ShaleBaseLine3 = int(ShaleBaseLine3)
    ShaleBaseLine4 = int(ShaleBaseLine4)

    Depth_cm = (maxdepth - mindepth)*100
    Log_length_cm = Depth_cm/skala
    Log_length_in = Log_length_cm/2.4

    panjang = Log_length_in
    lebar = 10
    majortick = 50
    minortick = 5

    if flatmarker =='WELL DEPTH' :
       delta1 = 0
       delta2 = 0
       delta3 = 0
    else:
       delta1, delta2, delta3 = flat_depth(flatmarker, marker1, marker2, marker3, marker4)

    korelasi = Korelasi(panjang,lebar,'Marker Correlation', mindepth, maxdepth, majortick, minortick)
    korelasi.mainwell(wellname1['WELLNAME'], float(wellname1['RTE']), mindepth, maxdepth, welldata1, marker1, FillGR, ShaleBaseLine1)
    korelasi.secondwell(wellname2['WELLNAME'], float(wellname2['RTE']), mindepth, maxdepth, delta1, welldata2, marker2, FillGR, ShaleBaseLine2)
    korelasi.thirdwell(wellname3['WELLNAME'], float(wellname3['RTE']), mindepth, maxdepth, delta2, welldata3, marker3, FillGR, ShaleBaseLine3)
    korelasi.fourthwell(wellname4['WELLNAME'], float(wellname4['RTE']), mindepth, maxdepth, delta3, welldata4, marker4, FillGR, ShaleBaseLine4)
    lines1 = create_correlation(marker1, marker2, 0, delta1)
    lines2 = create_correlation(marker2, marker3, delta1, delta2)
    lines3 = create_correlation(marker3, marker4, delta2, delta3)
    korelasi.show_correlation(lines1, lines2, lines3)
    
if __name__ == "__main__":
     main()
