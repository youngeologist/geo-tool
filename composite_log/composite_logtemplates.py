"""
Modul : Composite Log template
Asep Hermawan, November 2024
"""
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
from matplotlib.patches import Rectangle
from matplotlib.ticker import (MultipleLocator, LogLocator, FormatStrFormatter, AutoMinorLocator)
import streamlit as st
import numpy as np

# Main Class of LogTemplate
class LogTemplate:
    def __init__(self, judul, panjang, lebar, majortick, minortick):
        self.judul = judul
        self.panjang = panjang
        self.lebar = lebar
        self.majortick = majortick
        self.minortick = minortick
                
        self.fig = plt.figure(figsize=(lebar, panjang))
        self.fig.set_dpi(75)
        self.fig.suptitle(self.judul, size=10, y=0.045, ha='right')
        
        # Layout log
        self.ax4 = self.fig.add_axes([0.25, 0.05, 0.1, 0.95])
        self.ax1 = self.fig.add_axes([0.05, 0.05, 0.2, 0.95])
        self.ax12 = self.ax1.twiny()
        self.ax13 = self.ax1.twiny()
        self.ax2 = self.fig.add_axes([0.35, 0.05, 0.2, 0.95])
        self.ax22 = self.ax2.twiny()
        self.ax23 = self.ax2.twiny()
        self.ax3 = self.fig.add_axes([0.55, 0.05, 0.2, 0.95])
        # Density/Neutron in same column
        self.ax32 = self.ax3.twiny()

    def show_triplecombo_composite(self, min, max, RTE, DepthMode, df_lwd, df_mudlog, df_marker, df_survey, df_fluid, df_gaspeak):
        self.top = min
        self.bottom = max
        self.mode = DepthMode
        self.rte = RTE
        self.depth = df_lwd['DEPTH']
        self.tvd = df_lwd['TVD']
        self.rop = df_lwd['ROP']
        self.cal = df_lwd['CAL']
        self.gr = df_lwd['GR']
        self.resSh = df_lwd['RESSH']
        self.resDp = df_lwd['RESDP']
        self.neu = df_lwd['NEU']
        self.den = df_lwd['DEN']
        # create synthetic density curve for density-neutron x-ove
        self.den_syn = (0.6-df_lwd['NEU'])/0.6+1.7
        # self.den_syn = (0.6-self.neu)/0.6+1.7
        
        # Load mudlog data
        self.mudlog_depth = df_mudlog['DEPTH']
        self.mudlog_tvd = df_mudlog['TVD']
        self.tgas = df_mudlog['TGAS']
        
        # Load marker data
        self.marker = df_marker['MARKER']
        self.depth_marker = df_marker['MD']
        self.tvd_marker = df_marker['TVD']
        self.tvdss_marker = df_marker['TVDSS']
        self.teks = df_marker['TEXT']
        self.depthplot = df_marker['MDPLOT']
        self.tvdplot = df_marker['TVDPLOT']
        self.tvdssplot = df_marker['TVDSSPLOT']
        self.xplot = df_marker['XPLOT']

        if self.mode == 'TVD': 
           self.depth = self.tvd
           self.mudlog_depth = self.mudlog_tvd
           self.depth_marker = self.tvd_marker
        elif self.mode == 'TVDSS':
           self.depth = self.tvd - self.rte
           self.mudlog_depth = self.mudlog_tvd - self.rte
           self.depth_marker = self.tvd_marker - self.rte

        # generate log plot
        self.ax1.plot(self.gr, self.depth, color='green', linewidth=0.75)
        #self.ax1.fill_between(self.depth, self.gr, 75, where=(self.gr < 75), color='yellow', interpolate=True, alpha=0.5)
        self.ax12.plot(self.rop, self.depth, color='black', linewidth=0.5)
        self.ax13.plot(self.cal, self.depth, color='blue', linewidth=0.5, linestyle="--")
        self.ax2.plot(self.resSh, self.depth, color='blue', linewidth=0.75)
        self.ax22.plot(self.resDp, self.depth, color='red', linewidth=0.75)
        self.ax3.plot(self.neu, self.depth, color='blue', linewidth=0.75, linestyle='--')
        self.ax32.plot(self.den, self.depth, color='red', linewidth=0.75)
        
        # make this chart invisible
        self.ax32.plot(self.den_syn, self.depth, color='blue', linewidth=0.75, alpha=0) 
        
        # create density-neutron x-over
        self.ax32.fill_between(
                               self.depth, self.den_syn, self.den, 
                               where=(self.den_syn > self.den), 
                               color='yellow', interpolate=True
                               )
        
        # generate Total Gas data
        self.ax23.plot(self.tgas, self.mudlog_depth, color='black', linewidth=0.75)
        
        # generate marker
        self.ax2.hlines(self.depth_marker, xmin=0.2, xmax=2000, color='red', linewidth=1) 
        for i, row in df_marker.iterrows():
            if self.mode == 'MD':
               if row['MDPLOT'] > self.top and row['MDPLOT'] < self.bottom:
                  self.ax2.text(row['XPLOT'], row['MDPLOT'], row['TEXT'], color='red', fontsize=6) 
            elif self.mode == 'TVD':
               if row['TVDPLOT'] > self.top and row['TVDPLOT'] < self.bottom:
                  self.ax2.text(row['XPLOT'], row['TVDPLOT'], row['TEXT'], color='red', fontsize=6)
            else:
               if row['TVDSSPLOT'] > self.top and row['TVDSSPLOT'] < self.bottom:
                  self.ax2.text(row['XPLOT'], row['TVDSSPLOT'], row['TEXT'], color='red', fontsize=6)

        # generate survey
        for i, row in df_survey.iterrows():
            if self.mode == 'MD':
               if row['MD'] > self.top and row['MD'] < self.bottom:
                  self.ax32.text(row['XPLOT'], row['MD'], row['TEXT1']+'\n'+row['TEXT2']+'\n'+row['TEXT3'], color='black', fontsize=5) 
            elif self.mode == 'TVD':
               if row['TVD'] > self.top and row['TVD'] < self.bottom:
                  self.ax32.text(row['XPLOT'], row['TVD'], row['TEXT1']+'\n'+row['TEXT2']+'\n'+row['TEXT3'], color='black', fontsize=5)
            else:
               if row['TVDSS'] > self.top and row['TVDSS'] < self.bottom:
                  self.ax32.text(row['XPLOT'], row['TVDSS'], row['TEXT1']+'\n'+row['TEXT2']+'\n'+row['TEXT3'], color='black', fontsize=5)
        
        # generate gas peak
        for i, row in df_gaspeak.iterrows():
            if self.mode == 'MD':
               if row['DEPTH'] > self.top and row['DEPTH'] < self.bottom:
                  self.ax23.text(row['TG']-0.9*row['TG'], row['DEPTH']+1, row['TEXT1']+'\n'+row['TEXT2'], color='blue', fontsize=5) 
            elif self.mode == 'TVD':
               if row['TVD'] > self.top and row['TVD'] < self.bottom:
                  self.ax23.text(row['TG']-0.9*row['TG'], row['TVD']+1, row['TEXT1']+'\n'+row['TEXT2'], color='blue', fontsize=5)
            else:
               if row['TVDSS'] > self.top and row['TVDSS'] < self.bottom:
                  self.ax23.text(row['TG']-0.9*row['TG'], row['TVDSS']+1, row['TEXT1']+'\n'+row['TEXT2'], color='blue',  fontsize=5)
        
        # show fluid ID
        for i, row in df_fluid.iterrows():
            if self.mode == 'MD':
               if row['MDTOP'] > self.top and row['MDTOP'] < self.bottom:
                  self.ax4.add_patch(Rectangle((0, row['MDTOP']), 10, row['THICKMD'], 
                                      color = row['COLOR'], fill=True, alpha=0.8))
            elif self.mode == 'TVD':
               if row['TVDTOP'] > self.top and row['TVDTOP'] < self.bottom:
                  self.ax4.add_patch(Rectangle((0, row['TVDTOP']), 10, row['THICKTVD'], 
                                      color = row['COLOR'], fill=True, alpha=0.8))
            else :
               if row['TVDSSTOP'] > self.top and row['TVDSSTOP'] < self.bottom:
                  self.ax4.add_patch(Rectangle((0, row['TVDSSTOP']), 10, row['THICKTVD'], 
                                      color = row['COLOR'], fill=True, alpha=0.8))      
        
        # Format log output & display log
        self.format_axis()
        st.pyplot(self.fig)
        # plt.savefig('./asep-03xxx.pdf', bbox_inches='tight')
       
    def format_axis(self): 
        # Initiate log format
        CurveNm = ('DEPTH','GR','ROP','CAL','ResSh','ResDp','TGas','NEU', 'DEN','DT')
        CurveScl = ([0,10],[0,150],[100,0],[5,20],[0.2,200],[0.2,200],[0.2,200],[0.6,0],[1.7,2.7],[140,40])
        CurveClr = ('white','green','black','blue','blue', 'red', 'black','blue', 'red', 'blue')
        
        # Generate format for all chart
        for i, self.ax in enumerate(self.fig.axes):
            self.ax.set_xlim(CurveScl[i])
            self.ax.set_xticks(CurveScl[i])
            self.ax.xaxis.tick_top()
            self.ax.set_xlabel(CurveNm[i], color=CurveClr[i], fontsize=7)
            self.ax.xaxis.set_label_position('top')
            self.ax.tick_params(axis='x',colors=CurveClr[i], labelsize=5)
            self.ax.set_ylim(self.top, self.bottom)
            self.ax.invert_yaxis()
            self.ax.set_yticklabels([])
            self.ax.yaxis.set_major_locator(MultipleLocator(self.majortick))
            self.ax.yaxis.set_minor_locator(MultipleLocator(self.minortick))
            self.ax.minorticks_on()
            if i!= 0:
               self.ax.grid(which='minor', color='#999999', linestyle='-', alpha=0.5)
               self.ax.grid(which='major', color='#666666', linestyle='-')

        #Resistivity log template
        self.ax2.set_xscale('log')
        self.ax2.tick_params(axis='y',labelsize=15)
        self.ax2.yaxis.set_major_formatter(tck.FormatStrFormatter('%0.0f'))
        #self.ax2.xaxis.set_major_locator(LogLocator(base=10, subs=np.arange(0.2, 200)))
        #self.ax2.xaxis.set_minor_locator(LogLocator(base=10, subs=np.arange(0.2, 200)))
        self.ax22.set_xscale('log')
        self.ax23.set_xscale('log')
        # ROP label
        self.ax12.spines['top'].set_position(('outward',25))
        self.ax13.spines['top'].set_position(('outward',50))
        # Deep RES label
        self.ax22.spines['top'].set_position(('outward',25))
        self.ax23.spines['top'].set_position(('outward',50))
        # Density label
        self.ax32.spines['top'].set_position(('outward',25))
        
