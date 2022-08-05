# -*- coding: utf-8 -*-
"""
Created on Sun May  2 16:07:32 2021

@author: taiks
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')

RecoveryStates = ["FR","RO","SiP"]

N=len(RecoveryStates)
ProbDT = np.zeros([N,5])
r=0;

for w in RecoveryStates:
    ReadingFile1  = 'DT_stepfunc_'+w+'.csv'
    DT_StepFunc = pd.read_csv(ReadingFile1)
    Downtime = DT_StepFunc.iloc[:,-1]
    i=0;p1=0;p2=0;p3=0;p4=0;p5=0;
    while(i<len(DT_StepFunc)-1):
        if(Downtime[i]<=30*4):
            p1=p1+1
        elif(Downtime[i]>30*4 and Downtime[i]<=30*8):
            p2=p2+1
        elif(Downtime[i]>30*8 and Downtime[i]<=30*12):
            p3=p3+1
        elif(Downtime[i]>30*12 and Downtime[i]<=30*24):
            p4=p4+1
        elif(Downtime[i]>30*24):
            p5=p5+1
        i=i+1
    n_real_rapidity = [p1,p2,p3,p4,p5]
    ProbDT[r,:] = [i/((len(DT_StepFunc)-1)/100) for i in n_real_rapidity]
    r=r+1 
Prob_SiP = np.zeros([1])
Prob_RO = np.zeros([1])
Prob_FR = np.zeros([1])
r=0;

ReadingFile2  = 'RS_stats.csv'
RS_stats = pd.read_csv(ReadingFile2)
RS_stats_np = np.asarray(RS_stats)
Prob_SiP[0] = RS_stats_np[2,1]*100
Prob_RO[0] = RS_stats_np[1,1]*100
Prob_FR[0] = RS_stats_np[0,1]*100
r=r+1;
        

colors5 = [0.909,0.976,0.866]
colors4 = [0.75,0.906,0.796]
colors3 = [0.592,0.757,0.745]
colors2 = [0.619,0.537,0.675]
colors1 = [0.427,0.208,0.431]

# Rapidity plot
ind = [1, 2, 3]
list_of_labels1 = ["FR","RO","SiP"]

fig1,ax = plt.subplots(figsize =(3.5, 3.25))
p1 = plt.barh(ind , ProbDT[:,0],0.5,color=colors5)
p2 = plt.barh(ind , ProbDT[:,1],0.5,left=ProbDT[:,0],color=colors4)
p3 = plt.barh(ind , ProbDT[:,2],0.5,left=ProbDT[:,0]+ProbDT[:,1],color=colors3)
p4 = plt.barh(ind , ProbDT[:,3],0.5,left=ProbDT[:,0]+ProbDT[:,1]+ProbDT[:,2],color=colors2)
p5 = plt.barh(ind , ProbDT[:,4],0.5,left=ProbDT[:,0]+ProbDT[:,1]+ProbDT[:,2]+ProbDT[:,3],color=colors1)
plt.xlabel("Percentage of realizations")
plt.legend(["<=4 months","4 < DT <= 8","8 < DT <= 12","12 < DT <= 24","DT > 24"])
plt.yticks(ind, list_of_labels1)
plt.xticks([0,25,50,75,100])
plt.tight_layout()
plt.savefig("Rapidity_ref.png",dpi=1200)

# Robustness plot
ind2 = 1

# Shelter-in-Place
fig2,ax = plt.subplots(figsize=(2,2.5))
p7 = plt.barh(ind2,Prob_SiP,0.5,color=colors2)
plt.xlim([0, 100])
plt.xticks([0,25,50,75,100])
plt.tight_layout()
plt.axvline(10,c='maroon', linewidth=1, linestyle='--')
plt.savefig("Robustness_SiP.png",dpi=600)

#Reoccupancy
fig3,ax = plt.subplots(figsize=(2,2.5))
p7 = plt.barh(ind2,Prob_RO,0.5,color=colors3)
plt.xlim([0, 100])
plt.xticks([0,25,50,75,100])
ax.yaxis.set_tick_params(width=0)
plt.tight_layout()
plt.savefig("Robustness_RO.png",dpi=600)

#Functional Recovery
fig4,ax = plt.subplots(figsize=(2,2.5))
p7 = plt.barh(ind2,Prob_FR,0.5,color=colors4)
plt.xlim([0, 100])
plt.xticks([0,25,50,75,100])
ax.yaxis.set_tick_params(width=0)
plt.tight_layout()
plt.savefig("Robustness_FR.png",dpi=600)



                        