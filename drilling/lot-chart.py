import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots

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

def main():
    # st.header("LOT Chart")
    ChartTitle ="ASEP-01 8-1/2\" LOT Chart"
    image = Image.open('./data/geostrat100.png')
    st.sidebar.image(image)

    welldata = st.sidebar.file_uploader("Upload LOT/FIT data (XLS file only)")
    if welldata is None:
        welldata = './data/asep01-lotdata.xls'
    df = load_data(welldata)
    ChartTitle = st.sidebar.text_input("Chart Title", ChartTitle)

    # Tampilkan select box untuk memilih data
    cols = st.columns(3)
    Time_column = cols[0].selectbox("TIME Data", list(df.columns))
    Pressure = cols[1].selectbox("PRESSURE", list(df.columns))
    Volume = cols[2].selectbox("VOLUME", list(df.columns))

    fig = make_subplots(specs=[[{"secondary_y": True}]])   

    fig.update_layout(
        title_text = ChartTitle,
        legend=dict(orientation="h"),
        yaxis1=dict(
            title=dict(text="Presure"),
            side="left",
        ),
        yaxis2=dict(
            title=dict(text="Volume"),
            range=[0,10],
            side="right",
        ),
    )

    # Set x-axis title
    fig.update_xaxes(title_text="<b>TIME</b>")

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Pressure</b> (psi)", secondary_y=False)
    fig.update_yaxes(title_text="<b>Volume pumping</b> (bbls)", secondary_y=True)

    # Show chart
    first_chart = go.Scatter(x=df[Time_column], y=df[Pressure], name=Pressure, line=dict(color='blue'))
    second_chart = go.Scatter(x=df[Time_column], y=df[Volume], name=Volume, line=dict(color='red'))
    fig.add_trace(first_chart, row=1, col=1, secondary_y=False)
    fig.add_trace(second_chart, row=1, col=1, secondary_y=True)

    st.plotly_chart(fig)

if __name__ == "__main__":
     main()


