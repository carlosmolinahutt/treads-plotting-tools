# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 20:15:00 2021

@author: taiks
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')

# To be able to perform disaggregation, the user will have to assign a "Disaggregation group" tag to each fragility component in  the RCTable. 
#Fragility components that belong to the same disaggregation group, will be assigned the same tag. 
#The Tags are assigned based on the repair sequence of the element, i.e., Shear walls and SC connections are assigned 1a and 1b group tags since both belong to RS1. 
Groups = ['1a','1b','2a','2b','2c','2d','2e',3,4,5,6,7]
labels = ['Shear wall','Slab-column connections','Hot & cold water piping','Wall partitions & finishing','Suspended ceiling','HVAC','Fire sprinkler system','Mechanical equipment','Electrical equipment','Curtain walls','Elevator','Staircase']

Nreal_RS = np.zeros([len(Groups),6])     #Number of realizations where each recovery state is achieved
Prob_RS = np.zeros([len(Groups),6])

ReadingFile1  = 'RC_component.csv'
ReadingFile2  = 'Repair_Class_Table.csv'
ReadingFile3  = 'RT_stepfunc_FR.xlsx'
ReadingFile4  = 'IF_delays.csv'
                    
#ROBUSTNESS DISAGGREGATION
File1 = pd.read_csv(ReadingFile1,low_memory=False, header=None)
RC_component = File1.transpose()
RCTable = pd.read_csv(ReadingFile2)
for j in range(len(Groups)):
    if (j<=6):
        array = Groups[j].split() 
    else:
        array =  map(int, str(Groups[j]))
    DeagGroup = RCTable.loc[RCTable["Disaggregation group"].isin(array)]
    RC_DeagGroup = RC_component.loc[RC_component[0].isin(DeagGroup["Fragility"])]
    MaxRC_DeagGroup = RC_DeagGroup.loc[:,4:].max()
    for i in range(4,len(MaxRC_DeagGroup)+4):
        if(MaxRC_DeagGroup[i]==0):
            Nreal_RS[j,0] = Nreal_RS[j,0]+1
        if(MaxRC_DeagGroup[i]==1):
            Nreal_RS[j,1] = Nreal_RS[j,1]+1
        if(MaxRC_DeagGroup[i]==2):
            Nreal_RS[j,2] = Nreal_RS[j,2]+1
        if(MaxRC_DeagGroup[i]==3):
            Nreal_RS[j,3] = Nreal_RS[j,3]+1
        if(MaxRC_DeagGroup[i]==4):
            Nreal_RS[j,4] = Nreal_RS[j,4]+1
        if(MaxRC_DeagGroup[i]==5):
            Nreal_RS[j,5] = Nreal_RS[j,5]+1
    Prob_RS[j,:] = [i/len(MaxRC_DeagGroup)*100 for i in Nreal_RS[j,:]]
    j=j+1
    
    
# RAPIDITY DISAGGREGATION
IF_delays = pd.read_csv(ReadingFile4)
# We are plotting the disaggregation of repairable realizations. Hence calculate the number of repairable realizations
n_repairable = RC_component.shape[1]-4  #Since the framework only provides RC's of repairable realizations, the (size of RC_Component matrix - header rows) = equal to number of repairable realizations
Mean_inspection = sum(IF_delays['IF_inspection'])/n_repairable
Mean_eng = sum(IF_delays['IF_eng'])/n_repairable
Mean_permit = sum(IF_delays['IF_permit'])/n_repairable
Mean_finance = sum(IF_delays['IF_finance'])/n_repairable
Mean_cm_RS1 = sum(IF_delays['IF_cm_RS1'])/n_repairable
Mean_cm_RS2 = sum(IF_delays['IF_cm_RS2'])/n_repairable
Mean_cm_RS3 = sum(IF_delays['IF_cm_RS3'])/n_repairable
Mean_cm_RS4 = sum(IF_delays['IF_cm_RS4'])/n_repairable
Mean_cm_RS5 = sum(IF_delays['IF_cm_RS5'])/n_repairable
Mean_cm_RS6 = sum(IF_delays['IF_cm_RS6'])/n_repairable
Mean_cm_RS7 = sum(IF_delays['IF_cm_RS7'])/n_repairable
Mean_stab = sum(IF_delays['IF_stab'])/n_repairable

RT_RS1 = pd.read_excel(ReadingFile3,0); MeanRT_RS1 = RT_RS1.iloc[:,-1].mean()
RT_RS2 = pd.read_excel(ReadingFile3,1); MeanRT_RS2 = RT_RS2.iloc[:,-1].mean()
RT_RS3 = pd.read_excel(ReadingFile3,2); MeanRT_RS3 = RT_RS3.iloc[:,-1].mean()
RT_RS4 = pd.read_excel(ReadingFile3,3); MeanRT_RS4 = RT_RS4.iloc[:,-1].mean()
RT_RS5 = pd.read_excel(ReadingFile3,4); MeanRT_RS5 = RT_RS5.iloc[:,-1].mean()
RT_RS6 = pd.read_excel(ReadingFile3,5); MeanRT_RS6 = RT_RS6.iloc[:,-1].mean()
RT_RS7 = pd.read_excel(ReadingFile3,6); MeanRT_RS7 = RT_RS7.iloc[:,-1].mean()
                
                            
# ROBUSTNESS DISAGGREGATION PLOT                    
fig1,ax = plt.subplots(figsize=(2.9,2.5))
ind1 = list(range(1,len(Groups)+1))

#
colors5 = [0.909,0.976,0.866]
colors4 = [0.75,0.906,0.796]
colors3 = [0.592,0.757,0.745]
colors2 = [0.619,0.537,0.675]
colors1 = [0.427,0.208,0.431]

p1 = plt.barh(ind1 , Prob_RS[:,5],0.5,color=colors1)
p2 = plt.barh(ind1 , Prob_RS[:,4],0.5,left=Prob_RS[:,5],color=colors2)
p3 = plt.barh(ind1 , Prob_RS[:,3],0.5,left=Prob_RS[:,5]+Prob_RS[:,4],color=colors3)
p4 = plt.barh(ind1 , Prob_RS[:,2],0.5,left=Prob_RS[:,5]+Prob_RS[:,4]+Prob_RS[:,3],color=colors4)
p5 = plt.barh(ind1 , Prob_RS[:,1],0.5,left=Prob_RS[:,5]+Prob_RS[:,4]+Prob_RS[:,3]+Prob_RS[:,2],color=colors5)

plt.xlabel("Percentage of realizations")
plt.yticks(ind1, labels,fontname='arial')
plt.xlim([0, 100])
plt.xticks([0,50,100])
ax.yaxis.set_tick_params(width=0)
plt.tight_layout()
plt.rc('font', size=10)          # controls default text sizes
plt.savefig("Disaggregation_Robustness.png",dpi=600)


# RAPIDITY DISAGGREGATION PLOT  
# POST PROCESSING (TO ADD Y-AXIS, LEGEND, ETC) FOR THIS PLOT CAN BE DONE IN THE ATTACHED .PPT FILE 
fig2,ax =    plt.subplots(figsize=(2.5,2.75))
ind2 = [1,2,3,4,6,7,8,9,11,12,13,14,16,17,18,19]  
DT_disaggr = np.zeros([16,5])

DT_disaggr[:,0] = Mean_inspection
for i in [0,4,8,12]:
    DT_disaggr[i,1] = Mean_finance
for i in [1,5,9,13]:
    DT_disaggr[i,1] = Mean_eng
    DT_disaggr[i,2] = Mean_permit
for i in [2,6,10,14]:
    DT_disaggr[i,1] = Mean_stab
    
DT_disaggr[3,1] = Mean_cm_RS1; DT_disaggr[7,1] = Mean_cm_RS3; DT_disaggr[11,1] = Mean_cm_RS6; DT_disaggr[15,1] = Mean_cm_RS7;
                
DT_disaggr[0:4,3] = MeanRT_RS1; DT_disaggr[0:4,4] = max(MeanRT_RS2,MeanRT_RS4,MeanRT_RS5)
DT_disaggr[4:8,3] = MeanRT_RS3;
DT_disaggr[8:12,3] = MeanRT_RS6;
DT_disaggr[12:16,3] = MeanRT_RS7;

p1 = plt.barh(ind2 , DT_disaggr[:,0],0.8,color=colors1,alpha=0.6)
p2 = plt.barh(ind2 , DT_disaggr[:,1],0.8,left=DT_disaggr[:,0],color=colors2,alpha=0.6)
p3 = plt.barh(ind2 , DT_disaggr[:,2],0.8,left=DT_disaggr[:,0]+DT_disaggr[:,1],color=colors3,alpha=0.6)
p4 = plt.barh(ind2 , DT_disaggr[:,3],0.8,left=DT_disaggr[:,0]+DT_disaggr[:,1]+DT_disaggr[:,2],color=colors4,alpha=0.6)
p5 = plt.barh(ind2 , DT_disaggr[:,4],0.8,left=DT_disaggr[:,0]+DT_disaggr[:,1]+DT_disaggr[:,2]+DT_disaggr[:,3],color=colors5,alpha=0.6)

plt.xlim([0, 300])
plt.xticks([0,100,200,300])
ax.yaxis.set_tick_params(width=0)
plt.tight_layout()
plt.savefig("Disaggregation_Rapidity.png",dpi=600)