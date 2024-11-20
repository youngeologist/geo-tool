'''
Asep Hermawan
November 2024
LOT/FIT chart interactive visualization
-----------------------------------------
'''
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots
import datetime

st.set_page_config(
    page_title="LOT/FIT Chart",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data(welldata):
    df = pd.read_excel(welldata, engine='xlrd')
    df = df.fillna(method='ffill')
    return df

#end_function_load_data
def garislurus(pressure, koef, x0):
    x= koef*pressure + x0
    return x

def main():
    # st.header("LOT Chart")
    ChartTitle ="ASEP-01 8-1/2\" LOT Chart"
    image = Image.open('geostrat100.png')
    st.sidebar.image(image)

    welldata = st.sidebar.file_uploader("Upload LOT/FIT data (XLS file only)")
    if welldata is None:
        welldata = './data/asep01-lotdata.xls'
    df = load_data(welldata)
    ChartTitle = st.sidebar.text_input("Chart Title", ChartTitle)

    # Tampilkan select box untuk memilih data
    Time_column = st.sidebar.selectbox("TIME Data", list(df.columns))
    Pressure = st.sidebar.selectbox("PRESSURE", list(df.columns))
    Volume = st.sidebar.selectbox("VOLUME", list(df.columns))
    try:
        MaxPress = int(df[Pressure].max())
    except:
        MaxPress = 1000

        
    Time0= pd.to_datetime(df[Time_column].min())
    TimeMax = pd.to_datetime(df[Time_column].max())
    Time1 = Time0.timestamp()-28800 # (UTC+8)
    TimeMax = TimeMax.timestamp()-28800
    Langkah = (TimeMax - Time1)/3600
    Time1Slider = datetime.datetime.fromtimestamp(Time1)
    TimeMaxSlider = datetime.datetime.fromtimestamp(TimeMax)

    cols = st.columns(3)
    #TimeSlider = cols2[0].slider('Select Model Time[0]', min_value=Time1, max_value=TimeMax, value=Time1)
    TimeSlider = cols[0].slider('Model Start Time (s)', min_value=0, max_value=3600, value=1800)
    Gradient = cols[1].slider('Model Gradient', min_value=0.0, max_value=1.0, value=0.5)
    MaxPress = cols[2].slider('Model Max Pressure (Psi)', min_value=0, max_value=MaxPress, value=1000)
    #MaxPress = cols[2].text_input("Model Max Pressure", MaxPress)
    MaxPress = int(MaxPress)

    PressureModel = np.arange(0,MaxPress,100)

    Time1 = Time1+TimeSlider*Langkah
    Garis = garislurus(PressureModel, Gradient, Time1)
    
    datetime_model = []
    for garis in Garis:
        garis1 = datetime.datetime.fromtimestamp(garis)
        datetime_model.append(garis1)

    #st.write(datetime_model)

    fig = make_subplots(specs=[[{"secondary_y": True}]])   

    fig.update_layout(
        title_text = ChartTitle,
        legend=dict(orientation="h", x=1, y=1, xanchor='right', yanchor='top'),
        yaxis1=dict(
            title=dict(text="Presure"),
            side="left",
            range=[0,MaxPress+1000],
        ),
        yaxis2=dict(
            tickmode='array',
            tickvals=[2,4,6,8,10],
            title=dict(text="Volume"),
            range=[0,10],
            side="right",
            showgrid=False,
        ),
    )

    # Set x-axis title
    fig.update_xaxes(title_text="<b>TIME</b>")

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Pressure</b> (psi)", secondary_y=False)
    fig.update_yaxes(title_text="<b>Volume pumping</b> (bbls)", secondary_y=True)

    # Show chart
    first_chart = go.Scatter(x=df[Time_column], y=df[Pressure], name=Pressure, line=dict(color='blue', width=2))
    second_chart = go.Scatter(x=df[Time_column], y=df[Volume], name=Volume, line=dict(color='green'))
    garis = go.Scatter(x=datetime_model, y=PressureModel, name='Linear', line=dict(color='red', width=0.75))

    fig.add_trace(first_chart, row=1, col=1, secondary_y=False)
    fig.add_trace(second_chart, row=1, col=1, secondary_y=True)
    fig.add_trace(garis, row=1, col=1, secondary_y=False)

    st.plotly_chart(fig)

if __name__ == "__main__":
     main()


