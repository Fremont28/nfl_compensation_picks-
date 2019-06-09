#5/25/19 
#Which NFL teams are the best at making compensation picks? (2013-2018 drafts)*****

#import libraries 
import pandas as pd
import numpy as np 

#import data 
nflP=pd.read_csv("college_metrics_nfl.csv")
nflP=nflP[["Rnd","Pick","Year","First","Last","Pos","DrAge","Tm","CarAV"]]
new=nflP[nflP.Tm=="NEW"]
nflP = nflP[~nflP["Tm"].str.contains("NEW")] 

#patriots
def pat_assign(x):
    if x=="NEW":
        return "NWE"

new['Tm']=new['Tm'].apply(pat_assign)
nflP=pd.concat([nflP,new],axis=0)

nflP1=nflP  
otro=nflP1[(nflP1.Tm=="SDG")|(nflP1.Tm=="STL")]
nflP1 = nflP1[~nflP1["Tm"].str.contains("SDG|STL")] 

#assign teams different names (i.e. san diego, st. louis move to los angeles)
def san_diego(x):
    if x=="SDG":
        return "LAC"
    if x=="STL":
        return "LAR"

otro['Tm']=otro['Tm'].apply(san_diego)
nflP1=pd.concat([nflP1,otro],axis=0) 
nflP1['DrAge']=nflP1['DrAge'].fillna(nflP1.DrAge.mean())

#non-2019 draft years (13-18) 
p1=nflP1[~(nflP1.Year ==2019)]
p1=p1[~(p1.Year ==2012)]

#sum car av 
sum_av=p1.groupby('Tm')['CarAV'].sum() 
sum_av.sort_values(ascending=False)

#ii. average av 
avg_av=p1.groupby('Tm')['CarAV'].mean() 
avg_av.sort_values(ascending=False)

#iii. average av and average picks 
avg_av=p1.groupby(['Tm','Rnd'])['CarAV'].mean()
avg_av.sort_values(ascending=False)

#who is hitting on early round picks? (1-4)
rounds_early=p1[(p1.Rnd=="1")|(p1.Rnd=="2") | (p1.Rnd=="3")|(p1.Rnd=="4")]
rounds_early.CarAV.mean() 
avg_av_early=rounds_early.groupby('Tm')['CarAV'].mean()
avg_av_early.sort_values(ascending=False)
avg_av_early=pd.DataFrame(avg_av_early)
avg_av_early.reset_index(level=0,inplace=True)
avg_av_early.columns=['Tm','early_CarAV']

#who is hitting on late round/supplemental picks? (5-7)
rounds_late=p1[(p1.Rnd=="5")|(p1.Rnd=="6") | (p1.Rnd=="7")|(p1.Rnd=="S6")|(p1.Rnd=="S3")|(p1.Rnd=="S5")]
rounds_late.CarAV.mean() #3.75 
avg_av_late=rounds_late.groupby('Tm')['CarAV'].mean()
avg_av_late.sort_values(ascending=False)
avg_av_late=pd.DataFrame(avg_av_late)
avg_av_late.reset_index(level=0,inplace=True)
avg_av_late.columns=['Tm','late_CarAV']

#compare early vs. late picks 
comps_rnds=pd.merge(avg_av_early,avg_av_late,on="Tm")
comps_rnds['avg_early_CarAV']=12.19 
comps_rnds['avg_late_CarAV']=3.75
comps_rnds['early_CarAV_AA']=comps_rnds['early_CarAV']/comps_rnds['avg_early_CarAV'] #>1 better than average
comps_rnds['late_CarAV_AA']=comps_rnds['late_CarAV']/comps_rnds['avg_late_CarAV']  
comps_rnds.sort_values('late_CarAV_AA')

comps_rnds['ratio']=comps_rnds['early_CarAV']/comps_rnds['late_CarAV']
comps_rnds.sort_values('ratio') #lower means teams draft similary in early and late rounds---- 

#total carAV 
comps_rnds['avg_tot_CarAV']=comps_rnds.early_CarAV+comps_rnds.late_CarAV

#highest late round finds by team?
p1.CarAV.mean() 
late_gems=rounds_late[rounds_late.CarAV>8.35]
late_gems.sort_values('CarAV')

#correlation between ratio and total CarAV
comps_rnds['avg_tot_CarAV'].corr(comps_rnds['ratio']) #0.10
comps_rnds['avg_tot_CarAV'].corr(comps_rnds['early_CarAV']) #0.82
comps_rnds['avg_tot_CarAV'].corr(comps_rnds['late_CarAV']) #0.52  

#compensation picks(which teams are getting the most out of compensation picks?) 
av_years=p1.groupby('Year')['CarAV'].mean() #2013=12.4, 2014=11.5, 2013=9,2016=7.9,2017=5.1,2018=2.3
p2=p1 

#(2013)
yr13=p2[p2.Year==2013]
comps13=yr13[(yr13.Pick==95)|(yr13.Pick==96)|(yr13.Pick==97) |(yr13.Pick==130)|(yr13.Pick==131)|(yr13.Pick==132) | 
(yr13.Pick==133)|(yr13.Pick==166)|(yr13.Pick==167) | (yr13.Pick==168)|(yr13.Pick==201)|(yr13.Pick==202) | 
(yr13.Pick==203)|(yr13.Pick==204)|(yr13.Pick==205) | (yr13.Pick==206)|(yr13.Pick==239)|(yr13.Pick==240) |
(yr13.Pick==241)|(yr13.Pick==242)|(yr13.Pick==243) | (yr13.Pick==244)|(yr13.Pick==245)|(yr13.Pick==246)|
(yr13.Pick==247)|(yr13.Pick==248)|(yr13.Pick==249) | (yr13.Pick==250)|(yr13.Pick==251)|(yr13.Pick==252) | (yr13.Pick==253)|(yr13.Pick==254)]

comps13.shape 
comps13.Tm.unique()

#(2014)
yr14=p2[p2.Year==2014]
comps14=yr14[(yr14.Pick==97)|(yr14.Pick==98)|(yr14.Pick==99) |(yr14.Pick==100)|(yr14.Pick==133)|(yr14.Pick==134) | 
(yr14.Pick==135)|(yr14.Pick==136)|(yr14.Pick==137) | (yr14.Pick==138)|(yr14.Pick==139)|(yr14.Pick==140) | 
(yr14.Pick==173)|(yr14.Pick==174)|(yr14.Pick==175) | (yr14.Pick==176)|(yr14.Pick==209)|(yr14.Pick==210) |
(yr14.Pick==211)|(yr14.Pick==212)|(yr14.Pick==213) | (yr14.Pick==214)|(yr14.Pick==215)|(yr14.Pick==245)|
(yr14.Pick==246)|(yr14.Pick==247)|(yr14.Pick==248) | (yr14.Pick==249)|(yr14.Pick==250)|(yr14.Pick==251) |
(yr14.Pick==252)|(yr14.Pick==253)|(yr14.Pick==254) | (yr14.Pick==255)|(yr14.Pick==256)]


#(2015)
yr15=p2[p2.Year==2015]
comps15=yr15[(yr15.Pick==97)|(yr15.Pick==98)|(yr15.Pick==99) |(yr15.Pick==100)|(yr15.Pick==132)|(yr15.Pick==133) | 
(yr15.Pick==134)|(yr15.Pick==135)|(yr15.Pick==136) | (yr15.Pick==169)|(yr15.Pick==170)|(yr15.Pick==171) | 
(yr15.Pick==172)|(yr15.Pick==173)|(yr15.Pick==174) | (yr15.Pick==175)|(yr15.Pick==176)|(yr15.Pick==209) |
(yr15.Pick==210)|(yr15.Pick==211)|(yr15.Pick==212) | (yr15.Pick==213)|(yr15.Pick==214)|(yr15.Pick==215)|
(yr15.Pick==216)|(yr15.Pick==217)|(yr15.Pick==250) | (yr15.Pick==251)|(yr15.Pick==252)|(yr15.Pick==253) |
(yr15.Pick==254)|(yr15.Pick==255)|(yr15.Pick==256)] 

#(2016)
yr16=p2[p2.Year==2016]
comps16=yr16[(yr16.Pick==95)|(yr16.Pick==96)|(yr16.Pick==97) |(yr16.Pick==98)|(yr16.Pick==131)|(yr16.Pick==132) | 
(yr16.Pick==133)|(yr16.Pick==134)|(yr16.Pick==135) | (yr16.Pick==136)|(yr16.Pick==137)|(yr16.Pick==138) | 
(yr16.Pick==139)|(yr16.Pick==170)|(yr16.Pick==171) | (yr16.Pick==172)|(yr16.Pick==173)|(yr16.Pick==174) |
(yr16.Pick==175)|(yr16.Pick==208)|(yr16.Pick==209) | (yr16.Pick==210)|(yr16.Pick==211)|(yr16.Pick==212)|
(yr16.Pick==213)|(yr16.Pick==214)|(yr16.Pick==215) | (yr16.Pick==216)|(yr16.Pick==217)|(yr16.Pick==218) |
(yr16.Pick==219)|(yr16.Pick==220)|(yr16.Pick==221)] 

#(2017)
yr17=p2[p2.Year==2017]
comps17=yr17[(yr17.Pick==97)|(yr17.Pick==98)|(yr17.Pick==98) |(yr17.Pick==99)|(yr17.Pick==100)|(yr17.Pick==101) | 
(yr17.Pick==102)|(yr17.Pick==103)|(yr17.Pick==104) | (yr17.Pick==105)|(yr17.Pick==106)|(yr17.Pick==107) | 
(yr17.Pick==138)|(yr17.Pick==139)|(yr17.Pick==141) | (yr17.Pick==142)|(yr17.Pick==143)|(yr17.Pick==144) |
(yr17.Pick==176)|(yr17.Pick==177)|(yr17.Pick==178) | (yr17.Pick==179)|(yr17.Pick==180)|(yr17.Pick==181)|
(yr17.Pick==182)|(yr17.Pick==183)|(yr17.Pick==184) | (yr17.Pick==216)|(yr17.Pick==217)|(yr17.Pick==218) |
(yr17.Pick==251)|(yr17.Pick==252)|(yr17.Pick==253)] 

#(2018)
yr18=p2[p2.Year==2018]
comps18=yr18[(yr18.Pick==97)|(yr18.Pick==98)|(yr17.Pick==98) |(yr18.Pick==99)|(yr18.Pick==100)|(yr18.Pick==101) | 
(yr18.Pick==102)|(yr18.Pick==103)|(yr18.Pick==104) | (yr18.Pick==105)|(yr18.Pick==106)|(yr18.Pick==107) | 
(yr18.Pick==138)|(yr18.Pick==139)|(yr18.Pick==141) | (yr18.Pick==142)|(yr18.Pick==143)|(yr18.Pick==144) |
(yr18.Pick==176)|(yr18.Pick==177)|(yr18.Pick==178) | (yr18.Pick==179)|(yr18.Pick==180)|(yr18.Pick==181)|
(yr18.Pick==182)|(yr18.Pick==183)|(yr18.Pick==184) | (yr18.Pick==216)|(yr18.Pick==217)|(yr18.Pick==218) |
(yr18.Pick==251)|(yr18.Pick==252)|(yr18.Pick==253)] 

comp_picks=pd.concat([comps13,comps14,comps15,comps16,comps17,comps18],axis=0)
comp_picks.shape #197 comp picks 2013-2018 

#count picks 
count_tms=comp_picks.groupby('Tm')['Pos'].count()
count_tms.sort_values(ascending=False)

#average value from comp picks 
avg_value=comp_picks.groupby('Tm')['CarAV'].mean()
avg_value.sort_values(ascending=False)

def get_stats(group):
    return {'min': group.min(), 'max': group.max(), 'count': group.count(), 'mean': group.mean()}

summ=comp_picks['CarAV'].groupby(comp_picks['Tm']).apply(get_stats).unstack()
summ.sort_values(by="max",ascending=False)


#Positions and teams
avg_comp=comp_picks.groupby(['Pos','Tm']).mean() 
avg_count=comp_picks.groupby(['Pos','Tm']).count()
avg_count=avg_count['Rnd']
finaa=pd.concat([avg_comp,avg_count],axis=1)
finaa.columns=['Pick','Year','DrAge','CarAV','count']


#second highest pick per group 
min_max= comp_picks.assign(Data_Value=comp_picks.CarAV.abs())\
       .groupby(['Tm']).CarAV.agg([('Min' , 'min'), ('Max', 'max')])\
       .add_prefix('Tm')

#total comp picks by team 
comp_picks_tms=comp_picks.groupby('Tm')['Pick'].count()
com_high=comp_picks_tms.sort_values(ascending=False)
com_high.to_csv("com_high.csv")

#off and def car av (compensation picks)
off=comp_picks[(comp_picks.Pos=="T") | (comp_picks.Pos=="RB") | (comp_picks.Pos=="TE")|
(comp_picks.Pos=="K") | (comp_picks.Pos=="C") | (comp_picks.Pos=="QB")| 
(comp_picks.Pos=="OL") | (comp_picks.Pos=="FB") | (comp_picks.Pos=="WR")|
(comp_picks.Pos=="G")]

off_av=off['CarAV'].groupby(off['Tm']).apply(get_stats).unstack()
off_av.sort_values(by="mean",ascending=False)
off_av['pos']="Offense"
off_av.columns = [''] * len(off_av.columns)

defe=comp_picks[(comp_picks.Pos=="LB") | (comp_picks.Pos=="DT") | (comp_picks.Pos=="DB")|
(comp_picks.Pos=="DE") | (comp_picks.Pos=="TE") | (comp_picks.Pos=="FB")| 
(comp_picks.Pos=="WR") | (comp_picks.Pos=="CB") | (comp_picks.Pos=="OLB")|
(comp_picks.Pos=="ILB") | (comp_picks.Pos=="S") | (comp_picks.Pos=="LS")|
(comp_picks.Pos=="DL")]

defe_av=defe['CarAV'].groupby(defe['Tm']).apply(get_stats).unstack()
defe_av.sort_values(by="mean",ascending=False)

defe_av['pos']="Defense"
defe_av.columns = [''] * len(defe_av.columns)

#offensive comp picks redraft/what-if dak prescott scenarios 
offH=off[off.CarAV>=5][["CarAV","Last","Tm","Year"]] #prescott dal 2016 (42 av) 
offH['yrs']=2018-offH['Year']
offH['yrs']=offH['yrs']+1
offH.sort_values(by="CarAV")
offH['CarAv_yr']=offH.CarAV/offH.yrs #talkin' bout?
offH.sort_values(by="CarAv_yr")

#defensive comp picks 
defH=defe[defe.CarAV>=5][["CarAV","Last","Tm","Year"]] 
defH['yrs']=2018-defH['Year']
defH['yrs']=defH['yrs']+1
defH.sort_values(by="CarAV")
defH['CarAv_yr']=defH.CarAV/defH.yrs #talkin' bout?
defH.sort_values(by="CarAv_yr")

#dak prescott metriccs 
dak=comp_picks[comp_picks['Last'].str.contains('Good')]
dak

#correlation between Pick and CarAV 
comp_picks['CarAV'].corr(comp_picks.Pick)

#comp picks by team 
comp_picks_tms=comp_picks['avg'].groupby(comp_picks['Tm']).apply(get_stats).unstack()
comp_picks_tms.sort_values(by="mean",ascending=False)

#by round 
comp_picks['yrs']=2019-comp_picks['Year']
comp_picks['avg']=comp_picks.CarAV/comp_picks.yrs

comp_picks_tms['count'].corr(comp_picks_tms['max'])

round_av=comp_picks['avg'].groupby(comp_picks['Rnd']).apply(get_stats).unstack()
round_av.sort_values(by="mean",ascending=False)

#late round steals 
rnds=comp_picks[(comp_picks.Rnd=="5") | (comp_picks.Rnd=="6") | (comp_picks.Rnd=="7")]
rnds=rnds[["Last","Tm","avg"]]
rnds.sort_values(by="avg")

rnds_tres=comp_picks[(comp_picks.Rnd=="3") | (comp_picks.Rnd=="4")]
rnds_tres=rnds_tres[["Last","Tm","avg"]]
rnds_tres.sort_values(by="avg")

#summed picks 
sum_comp=comp_picks.groupby('Tm')['CarAV'].sum()
sum_comp.sort_values() 

#teams 
ttm=comp_picks[comp_picks['Tm'].str.contains('DEN')]
ttm










