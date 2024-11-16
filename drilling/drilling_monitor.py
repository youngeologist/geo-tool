import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image

st.set_page_config(
    page_title="Drilling TIME vs DATA",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)
@st.cache_data

def load_drillingdata(welldata):
    drl = pd.read_excel(welldata, engine='xlrd')
    df = drl.fillna(method='ffill')            
    return df 
#end_function_load_drillingdata

def show_top_sidebar(df):
    # Load the image
    st.sidebar.subheader("SELECT DRILLING PARAMETER", divider=True)
    # Using st.selectbox
    grafik1 = st.sidebar.selectbox("Parameter #1", list(df.columns))
    grafik2 = st.sidebar.selectbox("Parameter #2", list(df.columns))
    grafik3 = st.sidebar.selectbox("Parameter #3", list(df.columns))
    grafik4 = st.sidebar.selectbox("Parameter #4", list(df.columns))
    grafik5 = st.sidebar.selectbox("Parameter #5", list(df.columns))
    grafik6 = st.sidebar.selectbox("Parameter #6", list(df.columns))

    return grafik1, grafik2, grafik3, grafik4, grafik5, grafik6
# #end_function_show_top_sidebar

def main():
    image = Image.open('geostrat100.png')
    st.sidebar.image(image)

    st.sidebar.subheader("DRILLING TIME DATA", divider=True)
    welldata = st.sidebar.file_uploader("Upload XLS file with TIME data at the first column. Data header at the first row only")
    if welldata is None:
       welldata = 'drilling_data.xls'
    
    df = load_drillingdata(welldata)
    timecolumn = df.columns[0]
    grafik1, grafik2, grafik3, grafik4, grafik5, grafik6 = show_top_sidebar(df)
    # convert to date time format
    df[timecolumn] = pd.to_datetime(df[timecolumn])

    first_chart = go.Scatter(x=df[timecolumn], y=df[grafik1], name=grafik1)
    second_chart = go.Scatter(x=df[timecolumn], y=df[grafik2], name=grafik2)
    third_chart = go.Scatter(x=df[timecolumn], y=df[grafik3], name=grafik3)
    fourth_chart = go.Scatter(x=df[timecolumn], y=df[grafik4], name=grafik4)
    fifth_chart = go.Scatter(x=df[timecolumn], y=df[grafik5], name=grafik5)
    sixth_chart = go.Scatter(x=df[timecolumn], y=df[grafik6], name=grafik6)
    
    fig = make_subplots(rows=6, cols=1, 
                        shared_xaxes=True,
                        )
    
    fig.add_trace(first_chart, row=1, col=1)
    fig.add_trace(second_chart, row=2, col=1)
    fig.add_trace(third_chart, row=3, col=1)     
    fig.add_trace(fourth_chart, row=4, col=1)
    fig.add_trace(fifth_chart, row=5, col=1)
    fig.add_trace(sixth_chart, row=6, col=1)
    
    fig.update_layout(showlegend=False,
                      height=650, 
                      width=800, 
                      title_text="Drilling TIME vs DATA",            
                      yaxis1_title = grafik1,
                      yaxis2_title = grafik2,
                      yaxis3_title = grafik3,
                      yaxis4_title = grafik4,
                      yaxis5_title = grafik5,
                      yaxis6_title = grafik6,
                      xaxis6_title = 'TIME',
                     )
    
    fig.layout.hovermode = 'closest'
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
