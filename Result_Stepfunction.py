# -*- coding: utf-8 -*-
"""
Created on Wed May 26 15:31:58 2021

@author: taiks
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.close('all')


ReadingFile1  = 'DT_stepfunc_FR.csv'
ReadingFile2  = 'DT_stepfunc_SiP.csv'

StepFunc_FR = pd.read_csv(ReadingFile1,header=None)
StepFunc_SiP = pd.read_csv(ReadingFile2,header=None)
                
for i in range(2,len(StepFunc_FR)):
    if 'irreparable' in StepFunc_FR.iloc[i,0]:
        StepFunc_FR.iloc[i,3:] = StepFunc_FR.iloc[i,-1]
        
for i in range(2,len(StepFunc_SiP)):
    if 'irreparable' in StepFunc_SiP.iloc[i,0]:
        StepFunc_SiP.iloc[i,3:] = StepFunc_SiP.iloc[i,-1]
               
#FUNCTIONAL RECOVERY
Usability = StepFunc_FR.loc[0,1:]
fig1,ax = plt.subplots(figsize=(3.25,2.5))
Median_FR = np.percentile(StepFunc_FR.iloc[:,-1],50,interpolation='higher')
Prct10_FR = np.percentile(StepFunc_FR.iloc[:,-1],10,interpolation='higher')
Prct90_FR = np.percentile(StepFunc_FR.iloc[:,-1],90,interpolation='higher')

for i in range(len(StepFunc_FR)):
    if (Median_FR == StepFunc_FR.iloc[i,-1]):
        MedianFR_loc = i
    if (Prct10_FR == StepFunc_FR.iloc[i,-1]):
        Prct10FR_loc = i
    if (Prct90_FR == StepFunc_FR.iloc[i,-1]):
        Prct90FR_loc = i


a_list = list(range(2,len(StepFunc_FR)))
for i in a_list:
    plt.step(StepFunc_FR.loc[i,1:],Usability,color=[0.67,0.67,0.67],alpha=0.2,linewidth=0.5)
plt.step(StepFunc_FR.loc[MedianFR_loc,1:],Usability,color=[0,0,0],linewidth=1.5)
plt.step(StepFunc_FR.loc[Prct10FR_loc,1:],Usability,color=[0,0,0],linewidth=1.5,linestyle='dashed')
plt.step(StepFunc_FR.loc[Prct90FR_loc,1:],Usability,color=[0,0,0],linewidth=1.5,linestyle='dashed')    
plt.xlim([-15, 500])
plt.ylim([-0.05, 1.05])
plt.savefig("StepFunction_FR.png",dpi=600)

# Plot histogram of downtime values
fig3,ax = plt.subplots(figsize=(3.25,1))
TotalDT = StepFunc_FR.iloc[2:,-1]

plt.hist(TotalDT,bins=40,color=[0.67,0.67,0.67])
plt.xlim([-15, 500])
plt.ylim([0, 600])
plt.xticks([0,100,200,300,400,500])
plt.yticks([0,600],['0','0.3']) # Adjust y-axis according to plot
plt.tight_layout()
plt.savefig("Histogram_FR.png",dpi=600)


#SHELTER-IN-PLACE
fig2,ax = plt.subplots(figsize=(3.25,2.5))
Median_SiP = np.percentile(StepFunc_SiP.iloc[:,-1],50,interpolation='higher')
Prct10_SiP = np.percentile(StepFunc_SiP.iloc[:,-1],10,interpolation='higher')
Prct90_SiP = np.percentile(StepFunc_SiP.iloc[:,-1],90,interpolation='higher')

for i in range(len(StepFunc_SiP)):
    if (Median_SiP == StepFunc_SiP.iloc[i,-1]):
        MedianSiP_loc = i
    if (Prct10_SiP == StepFunc_SiP.iloc[i,-1]):
        Prct10SiP_loc = i
    if (Prct90_SiP == StepFunc_SiP.iloc[i,-1]):
        Prct90SiP_loc = i

for i in a_list:
    plt.step(StepFunc_SiP.loc[i,1:],Usability,color=[0.67,0.67,0.67],alpha=0.2,linewidth=0.5)
plt.step(StepFunc_SiP.loc[MedianSiP_loc,1:],Usability,color=[0,0,0],linewidth=1.5)
plt.step(StepFunc_SiP.loc[Prct10SiP_loc,1:],Usability,color=[0,0,0],linewidth=1.5,linestyle='dashed')
plt.step(StepFunc_SiP.loc[Prct90SiP_loc,1:],Usability,color=[0,0,0],linewidth=1.5,linestyle='dashed')    
plt.xlim([-15, 500])
plt.ylim([-0.05, 1.05])
plt.savefig("StepFunction_SiP.png",dpi=600)

fig4,ax = plt.subplots(figsize=(3.25,1))
TotalDT = StepFunc_SiP.iloc[2:,-1]
plt.hist(TotalDT,bins=50,color=[0.67,0.67,0.67])
plt.xlim([-15, 500])
plt.ylim([0, 600])
plt.xticks([0,100,200,300,400,500])
plt.yticks([0,600],['0','0.3']) # Adjust y-axis according to plot
#plt.ylabel("Proportion of realizations")
plt.tight_layout()
plt.savefig("Histogram_SiP.png",dpi=600)
         
