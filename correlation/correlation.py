"""
Modul: 3 Wells Marker Correlation
Asep Hermawan
Nov, 2023
"""

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)

class Korelasi:
    def __init__(self, panjang, lebar, judul, top, bottom, majortick, minortick):
        self.fontWellName = 20
        self.fontMarkerName = 12
        self.panjang = panjang
        self.lebar = lebar
        self.judul = judul
        self.top = top
        self.bottom = bottom
        self.majortick = majortick
        self.minortick = minortick

        self.fig = plt.figure(figsize=(self.lebar, self.panjang))
        # Siapkan layout log GR/RES/DEN/NEU well-1 
        self.ax10 = self.fig.add_axes([0.05, 0.10, 0.05, 0.70])
        self.ax11 = self.fig.add_axes([0.10, 0.10, 0.10, 0.70])
        self.ax12 = self.fig.add_axes([0.20, 0.10, 0.10, 0.70])
        self.ax13 = self.fig.add_axes([0.30, 0.10, 0.10, 0.70])
        self.ax14 = self.ax13.twiny()

        # Siapkan layout log GR/RES/DEN/NEU well-2 
        self.ax20 = self.fig.add_axes([0.50, 0.10, 0.05, 0.70])
        self.ax21 = self.fig.add_axes([0.55, 0.10, 0.10, 0.70])
        self.ax22 = self.fig.add_axes([0.65, 0.10, 0.10, 0.70])
        self.ax23 = self.fig.add_axes([0.75, 0.10, 0.10, 0.70])
        self.ax24 = self.ax23.twiny()

        # Siapkan layout log GR/RES/DEN/NEU well-3
        self.ax30 = self.fig.add_axes([0.95, 0.10, 0.05, 0.70]) 
        self.ax31 = self.fig.add_axes([1.00, 0.10, 0.10, 0.70])
        self.ax32 = self.fig.add_axes([1.10, 0.10, 0.10, 0.70])
        self.ax33 = self.fig.add_axes([1.20, 0.10, 0.10, 0.70])
        self.ax34 = self.ax33.twiny()

        # Siapkan layout log GR/RES/DEN/NEU well-4
        self.ax40 = self.fig.add_axes([1.40, 0.10, 0.05, 0.70]) 
        self.ax41 = self.fig.add_axes([1.45, 0.10, 0.10, 0.70])
        self.ax42 = self.fig.add_axes([1.55, 0.10, 0.10, 0.70])
        self.ax43 = self.fig.add_axes([1.65, 0.10, 0.10, 0.70])
        self.ax44 = self.ax43.twiny()

        self.format_axis()

    def format_axis(self):
             
        CurveNm = ['TVDSS','GR','Res','Den','             /Neu']
        CurveScl = [[0,10],[0,150], [0.2, 200], [1.7,2.7], [0.6,0]]
        CurveClr = ['black','green','black','red','blue']    
        
        j=0
        for i, self.ax in enumerate(self.fig.axes):
            self.ax.set_xlim(CurveScl[j])
            self.ax.set_xticks([])
            self.ax.xaxis.tick_top()
            self.ax.set_xlabel(CurveNm[j], color = CurveClr[j])
            self.ax.xaxis.set_label_position('top')
            self.ax.set_ylim(self.top, self.bottom)
            self.ax.yaxis.set_major_locator(MultipleLocator(self.majortick))
            self.ax.minorticks_on()
            self.ax.grid(which='minor', color='#999999', linestyle='-', alpha=0.2)
            self.ax.grid(which='major', color='#666666', linestyle='-')
            self.ax.invert_yaxis()
            j+= 1
            if j == 5:
               j = 0
            
        
    def mainwell(self, WellName, top, bottom, df_log, df_marker):
        self.top = top
        self.bottom = bottom  
        self.WellName = WellName
        self.depth = df_log['TVDSS']
        self.GR = df_log['GR']
        self.Res = df_log['RT']
        self.Den = df_log['DEN']
        self.Neu = df_log['NEU']
        self.Den_syn = (0.6-self.Neu)/0.6+1.7
        self.MarkerName = df_marker['MARKER']
        self.MarkerDepth = df_marker['TVDSS']
                
        #self.format_axis()
        self.ax11.text(100, self.top-20, self.WellName, fontsize=self.fontWellName)
        self.ax10.set_yticklabels([])
        self.ax12.set_yticklabels([])
        self.ax12.set_xscale('log')
        self.ax13.set_yticklabels([])
        
        # generate log plot
        self.ax11.plot(self.GR, self.depth, color='green', linewidth=0.7) 
        # self.ax11.fill_betweenx(self.depth, self.GR, 75, where=self.GR < 75, facecolor='yellow')
        self.ax12.plot(self.Res, self.depth, color='black', linewidth=0.7)
        self.ax13.plot(self.Den, self.depth, color='red', linewidth=0.7)
        self.ax13.plot(self.Den_syn, self.depth, color='blue', linewidth=0.1, alpha=0)
        self.ax14.plot(self.Neu, self.depth, color='blue', linewidth=0.7)
        self.ax13.fill_betweenx(
                               self.depth, self.Den_syn, self.Den, 
                               where=((self.Den < self.Den_syn) & (self.Den > 1.7)), 
                               facecolor='yellow', interpolate=True
                               )

        self.ax10.hlines(self.MarkerDepth, xmin=0, xmax=10, color='red', linewidth=0.8) 
        self.ax11.hlines(self.MarkerDepth, xmin=0, xmax=150, color='red', linewidth=0.8) 
        self.ax12.hlines(self.MarkerDepth, xmin=0.2, xmax=200, color='red', linewidth=0.8)
        self.ax13.hlines(self.MarkerDepth, xmin=1.7, xmax=2.7, color='red', linewidth=0.8)
        
        for i, row in df_marker.iterrows():
            if row['TVDSS'] > self.top and row['TVDSS'] < self.bottom:
                  self.ax12.text(0.3, row['TVDSS']-1, row['MARKER'], color='red', fontsize=self.fontMarkerName)

    def secondwell(self, WellName, top, bottom, delta, df_log, df_marker):
        self.top = top
        self.bottom = bottom
        self.WellName = WellName
        self.depth = df_log['TVDSS'] 
        self.GR = df_log['GR']
        self.Res = df_log['RT']
        self.Den = df_log['DEN']
        self.Neu = df_log['NEU']
        self.Den_syn = (0.6-self.Neu)/0.6+1.7

        self.MarkerName = df_marker['MARKER']
        self.MarkerDepth = df_marker['TVDSS'] 
       
        #self.format_axis()
        self.ax20.set_ylim(self.top+delta, self.bottom+delta)
        self.ax21.set_ylim(self.top+delta, self.bottom+delta)
        self.ax22.set_ylim(self.top+delta, self.bottom+delta)
        self.ax23.set_ylim(self.top+delta, self.bottom+delta)
              
        self.ax20.invert_yaxis()
        self.ax21.invert_yaxis()
        self.ax22.invert_yaxis()
        self.ax23.invert_yaxis()
        
        self.ax21.text(100, self.top+delta-20, self.WellName, fontsize=self.fontWellName)
        self.ax20.set_yticklabels([])
        self.ax22.set_yticklabels([])
        self.ax22.set_xscale('log')
        self.ax23.set_yticklabels([])
                
        # generate log plot
        self.ax21.plot(self.GR, self.depth, color='green', linewidth=0.7) 
        # self.ax21.fill_betweenx(self.depth, self.GR, 75, where=self.GR < 75, facecolor='yellow')
        self.ax22.plot(self.Res, self.depth, color='black', linewidth=0.7)
        self.ax23.plot(self.Den, self.depth, color='red', linewidth=0.7)
        self.ax23.plot(self.Den_syn, self.depth, color='blue', linewidth=0.1, alpha=0)
        self.ax24.plot(self.Neu, self.depth, color='blue', linewidth=0.7)
        self.ax23.fill_betweenx(
                               self.depth, self.Den_syn, self.Den, 
                               where=((self.Den < self.Den_syn) & (self.Den > 1.7)), 
                               facecolor='yellow', interpolate=True
                               )

        self.ax20.hlines(self.MarkerDepth, xmin=0, xmax=10, color='red', linewidth=0.8) 
        self.ax21.hlines(self.MarkerDepth, xmin=0, xmax=150, color='red', linewidth=0.8) 
        self.ax22.hlines(self.MarkerDepth, xmin=0.2, xmax=200, color='red', linewidth=0.8)
        self.ax23.hlines(self.MarkerDepth, xmin=1.7, xmax=2.7, color='red', linewidth=0.8)
        
        for i, row in df_marker.iterrows():
            if row['TVDSS'] > self.top+delta and row['TVDSS'] < self.bottom+delta:
                  self.ax22.text(0.3, row['TVDSS']-1, row['MARKER'], color='red', fontsize=self.fontMarkerName)

    def thirdwell(self, WellName, top, bottom, delta, df_log, df_marker):
        self.top = top
        self.bottom = bottom
        self.WellName = WellName
        self.depth = df_log['TVDSS']
        self.GR = df_log['GR']
        self.Res = df_log['RT']
        self.Den = df_log['DEN']
        self.Neu = df_log['NEU']
        self.Den_syn = (0.6-self.Neu)/0.6+1.7

        self.MarkerName = df_marker['MARKER']
        self.MarkerDepth = df_marker['TVDSS']
       
        #self.format_axis()
        self.ax30.set_ylim(self.top+delta, self.bottom+delta)
        self.ax31.set_ylim(self.top+delta, self.bottom+delta)
        self.ax32.set_ylim(self.top+delta, self.bottom+delta)
        self.ax33.set_ylim(self.top+delta, self.bottom+delta)
        
        self.ax30.invert_yaxis()
        self.ax31.invert_yaxis()
        self.ax32.invert_yaxis()
        self.ax33.invert_yaxis()
        
        self.ax31.text(100, self.top+delta-20, self.WellName, fontsize=self.fontWellName)
        self.ax30.set_yticklabels([])
        self.ax32.set_yticklabels([])
        self.ax32.set_xscale('log')
        self.ax33.set_yticklabels([])
               
        # generate log plot
        self.ax31.plot(self.GR, self.depth, color='green', linewidth=0.7) 
        # self.ax31.fill_betweenx(self.depth, self.GR, 75, where=self.GR < 75, facecolor='yellow')
        self.ax32.plot(self.Res, self.depth, color='black', linewidth=0.7)
        self.ax33.plot(self.Den, self.depth, color='red', linewidth=0.7)
        self.ax33.plot(self.Den_syn, self.depth, color='blue', linewidth=0.1, alpha=0)
        self.ax34.plot(self.Neu, self.depth, color='blue', linewidth=0.7)
        self.ax33.fill_betweenx(
                               self.depth, self.Den_syn, self.Den, 
                               where=((self.Den < self.Den_syn) & (self.Den > 1.7)), 
                               facecolor='yellow', interpolate=True
                               )

        self.ax30.hlines(self.MarkerDepth, xmin=0, xmax=10, color='red', linewidth=0.8) 
        self.ax31.hlines(self.MarkerDepth, xmin=0, xmax=150, color='red', linewidth=0.8) 
        self.ax32.hlines(self.MarkerDepth, xmin=0.2, xmax=200, color='red', linewidth=0.8)
        self.ax33.hlines(self.MarkerDepth, xmin=1.7, xmax=2.7, color='red', linewidth=0.8)
        
        for i, row in df_marker.iterrows():
            if row['TVDSS'] > self.top+delta and row['TVDSS'] < self.bottom+delta:
                  self.ax32.text(0.3, row['TVDSS']-1, row['MARKER'], color='red', fontsize=self.fontMarkerName)
    #end_function_thirdwell

    def fourthwell(self, WellName, top, bottom, delta, df_log, df_marker):
        self.top = top
        self.bottom = bottom
        self.WellName = WellName
        self.depth = df_log['TVDSS']
        self.GR = df_log['GR']
        self.Res = df_log['RT']
        self.Den = df_log['DEN']
        self.Neu = df_log['NEU']
        self.Den_syn = (0.6-self.Neu)/0.6+1.7

        self.MarkerName = df_marker['MARKER']
        self.MarkerDepth = df_marker['TVDSS']
       
        #self.format_axis()
        self.ax40.set_ylim(self.top+delta, self.bottom+delta)
        self.ax41.set_ylim(self.top+delta, self.bottom+delta)
        self.ax42.set_ylim(self.top+delta, self.bottom+delta)
        self.ax43.set_ylim(self.top+delta, self.bottom+delta)
        
        self.ax40.invert_yaxis()
        self.ax41.invert_yaxis()
        self.ax42.invert_yaxis()
        self.ax43.invert_yaxis()
        
        self.ax41.text(100, self.top+delta-20, self.WellName, fontsize=self.fontWellName)
        self.ax40.set_yticklabels([])
        self.ax42.set_yticklabels([])
        self.ax42.set_xscale('log')
        self.ax43.set_yticklabels([])
        
        # generate log plot
        self.ax41.plot(self.GR, self.depth, color='green', linewidth=0.7) 
        # self.ax31.fill_betweenx(self.depth, self.GR, 75, where=self.GR < 75, facecolor='yellow')
        self.ax42.plot(self.Res, self.depth, color='black', linewidth=0.7)
        self.ax43.plot(self.Den, self.depth, color='red', linewidth=0.7)
        self.ax43.plot(self.Den_syn, self.depth, color='blue', linewidth=0.1, alpha=0)
        self.ax44.plot(self.Neu, self.depth, color='blue', linewidth=0.7)
        self.ax43.fill_betweenx(
                               self.depth, self.Den_syn, self.Den, 
                               where=((self.Den < self.Den_syn) & (self.Den > 1.7)), 
                               facecolor='yellow', interpolate=True
                               )

        self.ax40.hlines(self.MarkerDepth, xmin=0, xmax=10, color='red', linewidth=0.8) 
        self.ax41.hlines(self.MarkerDepth, xmin=0, xmax=150, color='red', linewidth=0.8) 
        self.ax42.hlines(self.MarkerDepth, xmin=0.2, xmax=200, color='red', linewidth=0.8)
        self.ax43.hlines(self.MarkerDepth, xmin=1.7, xmax=2.7, color='red', linewidth=0.8)
        
        for i, row in df_marker.iterrows():
            if row['TVDSS'] > self.top+delta and row['TVDSS'] < self.bottom+delta:
                  self.ax42.text(0.3, row['TVDSS']-1, row['MARKER'], color='red', fontsize=self.fontMarkerName)
    #end_function_fourthwell
    
    def show_correlation(self, lines1, lines2, lines3):  
        self.ax15 = self.fig.add_axes([0.40, 0.10, 0.10, 0.70])
        self.ax15.set_axis_off()
        self.ax15.set_ylim(self.top, self.bottom)
        self.ax15.invert_yaxis()

        for point_pair in lines1:
            x_coords = [point_pair[0][0], point_pair[1][0]]
            y_coords = [point_pair[0][1], point_pair[1][1]]
            self.ax15.plot(x_coords, y_coords, color='red', linewidth=0.8)
        
        self.ax25 = self.fig.add_axes([0.85, 0.10, 0.10, 0.70])
        self.ax25.set_axis_off()
        self.ax25.set_ylim(self.top, self.bottom)
        self.ax25.invert_yaxis()

        for point_pair in lines2:
            x_coords = [point_pair[0][0], point_pair[1][0]]
            y_coords = [point_pair[0][1], point_pair[1][1]]
            self.ax25.plot(x_coords, y_coords, color='red', linewidth=0.8)
        
        self.ax35 = self.fig.add_axes([1.30, 0.10, 0.10, 0.70])
        self.ax35.set_axis_off()
        self.ax35.set_ylim(self.top, self.bottom)
        self.ax35.invert_yaxis()

        for point_pair in lines3:
            x_coords = [point_pair[0][0], point_pair[1][0]]
            y_coords = [point_pair[0][1], point_pair[1][1]]
            self.ax35.plot(x_coords, y_coords, color='red', linewidth=0.8)

        st.pyplot(self.fig)
