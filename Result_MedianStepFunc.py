# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 18:14:11 2021

@author: taikhum1
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.close('all')


ReadingFile1  = 'DT_stepfunc_FR.csv'
ReadingFile2  = 'DT_Path_FR.xlsx'
ReadingFile3  = 'IF_delays.csv'

DT_StepFunc_FR = pd.read_csv(ReadingFile1,header=None,skiprows=2)

StepFunc_PathA = pd.read_excel(ReadingFile2,0,header=None,skiprows=2)
StepFunc_PathB = pd.read_excel(ReadingFile2,1,header=None,skiprows=2)
StepFunc_PathC = pd.read_excel(ReadingFile2,2,header=None,skiprows=2)
StepFunc_PathD = pd.read_excel(ReadingFile2,3,header=None,skiprows=2)
UtilityTimes = pd.read_excel(ReadingFile2,4,header=None,skiprows=2)

for i in range(2,len(DT_StepFunc_FR)):
    if 'irreparable' in DT_StepFunc_FR.iloc[i,0]:
        DT_StepFunc_FR.iloc[i,3:] = DT_StepFunc_FR.iloc[i,-1]
        
for i in range(2,len(StepFunc_PathA)):
    if 'irreparable' in StepFunc_PathA.iloc[i,0]:
        StepFunc_PathA.iloc[i,3:] = StepFunc_PathA.iloc[i,-1]
for i in range(2,len(StepFunc_PathB)):
    if 'irreparable' in StepFunc_PathB.iloc[i,0]:
        StepFunc_PathB.iloc[i,3:] = StepFunc_PathB.iloc[i,-1]
for i in range(2,len(StepFunc_PathC)):
    if 'irreparable' in StepFunc_PathC.iloc[i,0]:
        StepFunc_PathC.iloc[i,3:] = StepFunc_PathC.iloc[i,-1]
for i in range(2,len(StepFunc_PathD)):
    if 'irreparable' in StepFunc_PathD.iloc[i,0]:
        StepFunc_PathD.iloc[i,3:] = StepFunc_PathD.iloc[i,-1]

        

IF_delays = pd.read_csv(ReadingFile3)
AllstepFunc_FR = pd.read_csv(ReadingFile1,header=None)
Usability = AllstepFunc_FR.iloc[0,1:]*100     

Median_FR = np.percentile(DT_StepFunc_FR.iloc[:,-1],50,interpolation='higher')

for i in range(len(DT_StepFunc_FR)):
    if (Median_FR == DT_StepFunc_FR.iloc[i,-1]):
        MedianFR_loc = i
        
Median_StepFunc_PathA = StepFunc_PathA.iloc[MedianFR_loc,1:]   
Median_StepFunc_PathB = StepFunc_PathB.iloc[MedianFR_loc,1:]     
Median_StepFunc_PathC = StepFunc_PathC.iloc[MedianFR_loc,1:]     
Median_StepFunc_PathD = StepFunc_PathD.iloc[MedianFR_loc,1:]   
Median_Gov_FR = DT_StepFunc_FR.loc[MedianFR_loc,1:]

Median_IFdelays = IF_delays.iloc[MedianFR_loc,1:] 
 
    

fig1,ax = plt.subplots(figsize=(5.25,4.5))
plt.step(Median_StepFunc_PathA,Usability,color=[0.13,0.369,0.659],linewidth=1.1)
plt.step(Median_StepFunc_PathB,Usability,color=[0.3,0.69,0.29],linewidth=1.1)
plt.step(Median_StepFunc_PathC,Usability,color=[0.1,0.71,0.66],linewidth=1.1)
plt.step(Median_StepFunc_PathD,Usability,color=[0.008,0,0.314],linewidth=1.1)
plt.step(Median_Gov_FR,Usability,'--',color=[0,0,0],linewidth=1.5)
plt.xlim([-15, 500])
#plt.ylim([-0.05, 1.05])
Yaxis = list(range(5,95,7))
Yaxis_IF = list(range(58,80,7))
Yaxis_IF_CM = list(range(48,5,-7))
Yaxis_Utility = 90

colorinspection = [0.51,0.314,0.55]
colorIF = [0.45,0.725,0.694]
colorIF2 = [0.862,0.96,0.862]

if 'irreparable' in DT_StepFunc_FR.iloc[MedianFR_loc,0]:
    plt.barh(20 , height = 3, width = Median_IFdelays.iloc[0],color=colorinspection)
    plt.barh(10 , height = 3, width = Median_IFdelays.iloc[-1] , color=colorIF)
else:
    #Inspection time
    plt.barh(Yaxis_IF , height = 3, width = Median_IFdelays.iloc[0],color=colorinspection)
    plt.barh(Yaxis_IF_CM , height = 3, width = Median_IFdelays.iloc[0],color=colorinspection)
    #Financing time
    plt.barh(Yaxis_IF[2] , height = 3, width = Median_IFdelays.iloc[3],left = Median_IFdelays.iloc[0],color=colorIF)
    #Engineering time
    plt.barh(Yaxis_IF[1] , height = 3, width = Median_IFdelays.iloc[1],left = Median_IFdelays.iloc[0],color=colorIF)
    #Permitting time
    plt.barh(Yaxis_IF[1] , height = 3, width = Median_IFdelays.iloc[2],left = Median_IFdelays.iloc[0]+Median_IFdelays.iloc[1],color=colorIF2)
    # Stabilization time
    plt.barh(Yaxis_IF[0] , height = 3, width = Median_IFdelays.iloc[11],left = Median_IFdelays.iloc[0],color=colorIF)
    #Contractor Mobilization time
    plt.barh(Yaxis_IF_CM , height = 3, width = Median_IFdelays.iloc[4:11],left = Median_IFdelays.iloc[0],color=colorIF)
    #Utlitiy time
    plt.barh(Yaxis_Utility,height=3,width=UtilityTimes.iloc[MedianFR_loc,-1],color=colorIF)
                                   
plt.savefig("MedianStepFunc_FR.png",dpi=600)

