# Deviation Survey Program
# Asep Hermawan
# November 2024
#--------------------------

import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots
import svydev

st.set_page_config(
    page_title="Well Deviation Survey",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_header(welldata):
    header = pd.read_excel(welldata, sheet_name='HEADER', engine='xlrd')
    header = header.ffill()
    return header
#end_function_load_header
def load_data(welldata):
    df = pd.read_excel(welldata, sheet_name='SURVEY', engine='xlrd')
    df = df.ffill()
    return df
#end_function_load_data
def load_plan(welldata):
    plan = pd.read_excel(welldata, sheet_name='PLAN', engine='xlrd')
    plan = plan.ffill()
    return plan
#end_function_load_plan

def Show_VSPlot(fig, ChartTitle, df, dfplan):
    
    fig.update_layout(
        title_text = ChartTitle,
        height=600, 
        width=700, 
        legend=dict(orientation="h"),
        yaxis=dict(
            title=dict(text="TVD"),
            side="left",
        )
    )

    # Set x-axis title
    fig.update_xaxes(title_text="<b>Vertical Section</b> (m)")
    # Set y-axis titles
    fig.update_yaxes(title_text="<b>TVD</b> (m)")
    fig.update_yaxes(autorange='reversed')
    # Show chart
    ActualSurvey = go.Scatter(x=df['VS'], y=df['TVD'], name='Actual Survey', line=dict(color='blue'))
    PlanSurvey = go.Scatter(x=dfplan['VS'], y=dfplan['TVD'], name='Plan Survey', line=dict(color='red'))
    fig.add_trace(PlanSurvey, row=1, col=1)
    fig.add_trace(ActualSurvey, row=1, col=1)
    st.plotly_chart(fig)
#end_function_Show_VSPlot

def Show_PlanView(fig, ChartTitle, df, dfplan):
    fig.update_layout(
        title_text = ChartTitle,
        height=600, 
        width=700, 
        legend=dict(orientation="h"),
        yaxis=dict(
            title=dict(text="NS"),
            side="left",
        )
    )

    # Set x-axis title
    fig.update_xaxes(title_text="<b>EW</b> (m)")
    # Set y-axis titles
    fig.update_yaxes(title_text="<b>NS</b> (m)")
   
    # Show chart
    ActualSurvey = go.Scatter(x=df['EW'], y=df['NS'], name='Actual Survey', line=dict(color='blue'))
    PlanSurvey = go.Scatter(x=dfplan['EW'], y=dfplan['NS'], name='Plan Survey', line=dict(color='red'))
    fig.add_trace(PlanSurvey, row=1, col=1)
    fig.add_trace(ActualSurvey, row=1, col=1)
    st.plotly_chart(fig)
#end_function_Show_PlanView

def show_3DView(fig, ChartTitle, df, dfplan):
    fig.add_trace(go.Scatter3d(
    x=dfplan['EW'],
    y=dfplan['NS'],
    z=dfplan['TVD'],
    mode='lines',
    marker=dict(
        size=1,
        color='red',
        opacity=0.8
    ),
    name='Plan Survey'
    ))

    fig.add_trace(go.Scatter3d(
        x=df['EW'],
        y=df['NS'],
        z=df['TVD'],
        mode='lines',
        marker=dict(
            size=1,
            color='blue',
            opacity=0.8
        ),
        name='Actual Survey'
    ))

    # Customize the layout
    fig.update_layout(
        scene = dict(
                zaxis=dict(
                      autorange="reversed"
                ),
                xaxis_title='EW (m)',
                yaxis_title='NS (m)',
                zaxis_title='TVD (m)'
        ),
        width=800,
        height=600
    )
    # Display the plot in Streamlit
    st.plotly_chart(fig)

def CalculateSurvey(df, RTE, AZVS):
    depth = df['DEPTH'].values   
    inc = df['INC'].values
    azi = df['AZI'].values
    TVD, TVDSS, DX, DY, VS = [],[],[],[],[]
    
    for i in range (len(df)): 
        if i == 0:
            TVD.append (0.0)
            TVDSS.append(float(-RTE))
            DX.append(0.0)
            DY.append(0.0)
            VS.append(0.0) 
        else:  
            FTVD = svydev.FDepthTVD(depth[i-1],inc[i-1],azi[i-1],TVD[i-1],depth[i],inc[i],azi[i])
            TVD.append(float(FTVD))
            TVDSS.append(float(FTVD)-RTE)
            FuncDX = svydev.FEasting(depth[i-1],inc[i-1],azi[i-1],DX[i-1],depth[i],inc[i],azi[i])
            DX.append(float(FuncDX))
            FuncDY = svydev.FNorthing(depth[i-1],inc[i-1],azi[i-1],DY[i-1],depth[i],inc[i],azi[i])
            DY.append(float(FuncDY))
            FVS = svydev.FVertSection(AZVS, DX[i], DY[i])
            VS.append(float(FVS)) 
    
    data = {'DEPTH': depth, 'INC': inc, 'AZI': azi, 'TVD': TVD, 'TVDSS': TVDSS, 'EW': DX, 'NS': DY, 'VS': VS}
    survey = pd.DataFrame(data)
    return survey

def main():
    # st.header("LOT Chart")
    ChartTitle ="ASEP-01 Well Profile"
    image = Image.open('../data/geostrat100.png')
    st.sidebar.image(image)

    welldata = st.sidebar.file_uploader("Upload Survey data (XLS file only)")
    if welldata is None:
        welldata = '../data/asep01-surveydata.xls'

    df = load_data(welldata)
    dfplan = load_plan(welldata)
    headerdata = load_header(welldata)

    headerdata = headerdata.iloc[0]
    WellName = headerdata['WELLNAME']
    RTE = headerdata['RTE']
    VSAZ = headerdata['VSAZ']
    SURFACEX = headerdata['SURFACEX']
    SURFACEY = headerdata['SURFACEY']

    ChartTitle = st.sidebar.text_input("Chart Title", ChartTitle)
    
    fig1 = make_subplots()
    fig2 = make_subplots()
    fig3 = go.Figure()

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["[ Plan Survey ]", "[ Actual Survey ]", 
                                      "[ Vertical Section View ]","[ Plan View ]", "[ 3D View ]"])
    with tab1:
         st.subheader("Plan Survey Data", divider=True)
         st.table(dfplan.style.format('{:.2f}'))
    with tab2:
         st.subheader("Survey Data", divider=True)
         df = CalculateSurvey(df,RTE,VSAZ)
         st.table(df.style.format('{:.2f}'))
    with tab3:
         Show_VSPlot(fig1, ChartTitle, df, dfplan)
    with tab4:
         Show_PlanView(fig2, ChartTitle, df, dfplan)
    with tab5:
        show_3DView(fig3, ChartTitle, df, dfplan)
    
    #
if __name__ == "__main__":
     main()


