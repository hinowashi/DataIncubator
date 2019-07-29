
# coding: utf-8

# In[1]:


from astropy.io import ascii
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib as mpl
import pandas as pd


# Definitions
# 
# Liquidity: Cash and Cash Equivalents relative to total deposits
# 
# Solvency (Capitalization): Equity relative to assets

# RCON1754:       Held to maturity securities
# 
# UBPR/RCON 2170: Total Assets
# 
# UBPR3210:       Total Bank Equity Capital
# 
# UBPR0081:       Noninterest-Bearing Cash and Due From Banks
# 
# RCON2200:       Deposits in domestic offices #Includes the sum of "Total Transaction Accounts (2215)"; plus "Nontransaction Savings Deposits (2389)"; plus "Total Time Deposits (2514))".
# 
# RCON1608:       COMMERCIAL AND INDUSTRIAL LOANS - NONACCRUAL
# 
# RCON1607:       COMMERCIAL AND INDUSTRIAL LOANS - PAST DUE 90 DAYS OR MORE AND STILL ACCRUING
# 
# RCON2948:       Total Liabilites

# # Creating the datafile 
# 
# In order to create a data set with the information needed. I read and merge the relevant dataframes to careate dfComplete.
# 
# dfComplete will then include new columns with the definitions stablished. 

# In[18]:


nameList = ['ID RSSD','Reporting Period','UBPR0081','UBPR2170','UBPR2200','UBPR1754','UBPR7316','UBPRE120']
df1 = pd.read_csv('/Users/casanova/Desktop/DataSience/FFIECCDRBulkAllUBPRRatios2017/FFIECCDRUBPRRatiosBalanceSheetdollar2017.csv', skiprows=1, usecols=nameList)

nameList = ['ID RSSD','Reporting Period','UBPR7316','UBPR3210']
df2 = pd.read_csv('/Users/casanova/Desktop/DataSience/FFIECCDRBulkAllUBPRRatios2017/FFIECCDRUBPRRatiosSummaryRatios2017.csv', skiprows=1, usecols=nameList)

nameList = ['Reporting Period End Date','IDRSSD','FDIC Certificate Number','OCC Charter Number','OTS Docket Number',
            'Primary ABA Routing Number','Financial Institution Name','Financial Institution Address',
            'Financial Institution City','Financial Institution State','Financial Institution Zip Code',
            'RCON2170','RCON2200','RCON2948','RCON1754','RCON1607','RCON1608']

df3 = pd.read_csv('/Users/casanova/Desktop/DataSience/FFIECCDRCallReports2017/FFIECCDRpart1.csv', skiprows=1, usecols=nameList)
df3 = df3.rename(columns={'IDRSSD': 'ID RSSD','RCON2170': 'UBPR2170','RCON1754': 'UBPR1754'})

dfComplete = pd.merge(left=df1,right=df2, how='outer')
dfComplete = pd.merge(left=dfComplete,right=df3, how='outer')

dfComplete = dfComplete[np.isfinite(dfComplete['FDIC Certificate Number'])]


# In[19]:


dfComplete['solvency'] = (dfComplete['UBPR3210'])/dfComplete['UBPR2170']
dfComplete['liquidity'] = dfComplete['UBPR0081']/dfComplete['UBPR2200']
dfComplete['liquidityBonds'] = dfComplete['UBPRE120']/dfComplete['UBPR2200']
dfComplete['HTM'] = dfComplete['UBPR1754']/dfComplete['UBPR2200']
dfComplete['NPLofCI'] = (dfComplete['RCON1607']+dfComplete['RCON1608'])/dfComplete['UBPR2200']
dfComplete = dfComplete[np.isfinite(dfComplete['liquidity'])]

dfComplete = dfComplete[(dfComplete['solvency']>=0)&(dfComplete['solvency']<=1)]
dfComplete = dfComplete[dfComplete['liquidity']<=1]
dfComplete = dfComplete[dfComplete['liquidityBonds']<=1]


# In[20]:


dfIndex = dfComplete.set_index(['Reporting Period','ID RSSD'])
dfIndex= dfIndex.sort_index(ascending=True)
df = dfIndex.loc['9/30/2017 11:59:59 PM']


# In[25]:


df.describe()


# In[26]:


fig, ax = plt.subplots(figsize=(10,10))
tag = np.log10(df['UBPR2170'].values)
cmap = plt.cm.CMRmap
cmaplist = [cmap(i) for i in range(cmap.N)]
cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)

bounds = np.linspace(2,10,20)
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)




ax.scatter(df['solvency'].values,df['liquidity'].values, marker = '.',
           c=tag,cmap=cmap, norm=norm, edgecolors='None')
ax.set_xlabel('Solvency')
ax.set_ylabel('Liquidity')
ax.semilogy()
ax.semilogx()
ax.set_xlim((1e-2,1))
ax.set_ylim((1e-5,1))

ax2 = fig.add_axes([0.95, 0.1, 0.03, 0.8])
cb = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, spacing='proportional',
                               ticks=bounds, boundaries=bounds, format='%6.2f')
plt.savefig('./all.pdf',dpi=800,bbox_inches='tight',pad_inches=0.02, format='pdf')
plt.show()


# In[8]:


fig, ax = plt.subplots(nrows=2, ncols=2,figsize=(10,10))
tag = np.log10(df['UBPR2170'].values)
cmap = plt.cm.CMRmap
cmaplist = [cmap(i) for i in range(cmap.N)]
cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)

bounds = np.linspace(2,10,20)
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)




ax[0,0].scatter(df['solvency'].values,df['liquidity'].values, marker = '.',
           c=tag,cmap=cmap, norm=norm, edgecolors='None')
ax[0,0].set_xlabel('Solvency')
ax[0,0].set_ylabel('Liquidity')
ax[0,0].semilogy()
ax[0,0].semilogx()
ax[0,0].set_xlim((1e-2,1))
ax[0,0].set_ylim((1e-5,1))


ax[1,0].scatter(df['solvency'].values,df['HTM'].values, marker = '.',
           c=tag,cmap=cmap, norm=norm, edgecolors='None')
ax[1,0].set_xlabel('Solvency')
ax[1,0].set_ylabel('HTM')
ax[1,0].semilogy()
ax[1,0].semilogx()
ax[1,0].set_xlim((1e-2,1))
ax[1,0].set_ylim((1e-6,1))

ax[0,1].scatter(df['solvency'].values,df['NPLofCI'].values, marker = '.',
           c=tag,cmap=cmap, norm=norm, edgecolors='None')
ax[0,1].set_xlabel('Solvency')
ax[0,1].set_ylabel('NPLofCI')
ax[0,1].semilogy()
ax[0,1].semilogx()
ax[0,1].set_xlim((1e-2,1))
ax[0,1].set_ylim((1e-7,0.06))

ax[1,1].scatter(df['solvency'].values,df['liquidityBonds'].values, marker = '.',
           c=tag,cmap=cmap, norm=norm, edgecolors='None')
ax[1,1].set_xlabel('Solvency')
ax[1,1].set_ylabel('Liquidity from U.S. Bonds')
ax[1,1].semilogy()
ax[1,1].semilogx()
ax[1,1].set_xlim((1e-2,1))
ax[1,1].set_ylim((1e-6,1))



ax2 = fig.add_axes([0.95, 0.1, 0.03, 0.8])
cb = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, spacing='proportional',
                               ticks=bounds, boundaries=bounds, format='%6.2f')
plt.savefig('./all2.pdf',dpi=800,bbox_inches='tight',pad_inches=0.02, format='pdf')
plt.show()


# In[9]:


val = 1e-1
dfElite = df[(df['solvency']>=val)&(df['liquidityBonds']>=val)&(df['liquidity']>=val)&(df['HTM']<=(val*1e-2))]


# In[10]:


fig, ax = plt.subplots(figsize=(10,10))
tag = np.log10(dfElite['UBPR2170'].values)
cmap = plt.cm.CMRmap
cmaplist = [cmap(i) for i in range(cmap.N)]
cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)

bounds = np.linspace(2,10,20)
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)


ax.scatter(dfElite['solvency'].values,dfElite['liquidity'].values, marker = '.',
           c=tag,cmap=cmap, norm=norm, edgecolors='None', s =100)
ax.set_xlabel('Solvency')
ax.set_ylabel('Liquidity')
ax.semilogy()
ax.semilogx()
ax.set_xlim((1e-2,1))
ax.set_ylim((1e-2,1))

ax2 = fig.add_axes([0.95, 0.1, 0.03, 0.8])
cb = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, spacing='proportional',
                               ticks=bounds, boundaries=bounds, format='%6.2f')
plt.savefig('./Elite.pdf',dpi=800,bbox_inches='tight',pad_inches=0.02, format='pdf')
plt.show()


# In[11]:


dfElite.loc[:,['Financial Institution Name','Financial Institution State','solvency','liquidity']]


# In[12]:


dfBig = df[(df['UBPR2170']>=1e8)]
dfBig.loc[:,['Financial Institution Name','Financial Institution State','solvency','liquidity']]


# In[13]:


fig, ax = plt.subplots(figsize=(10,10))
tag = np.log10(df['UBPR2170'].values)
cmap = plt.cm.CMRmap
cmaplist = [cmap(i) for i in range(cmap.N)]
cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)

bounds = np.linspace(2,10,20)
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)




ax.scatter(df['solvency'].values,df['liquidity'].values, marker = '.',
           c=tag,cmap=cmap, norm=norm, edgecolors='None')
ax.scatter(dfBig['solvency'].values,dfBig['liquidity'].values, marker = '.',
           edgecolors='None', s=200, c='c')
ax.scatter(dfElite['solvency'].values,dfElite['liquidity'].values, marker = '.',
           edgecolors='None', s = 200, c= 'g')

ax.set_xlabel('Solvency')
ax.set_ylabel('Liquidity')
ax.semilogy()
ax.semilogx()
ax.set_xlim((1e-2,1))
ax.set_ylim((1e-5,1))

ax2 = fig.add_axes([0.95, 0.1, 0.03, 0.8])
cb = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, spacing='proportional',
                               ticks=bounds, boundaries=bounds, format='%6.2f')
plt.savefig('./all.pdf',dpi=800,bbox_inches='tight',pad_inches=0.02, format='pdf')
plt.show()


# In[27]:


def filterArray(Filt, ToFilt, lLim, uLim):
    out1  = ToFilt[np.where( Filt<uLim )]
    filt1 = Filt[np.where( Filt<uLim )]
    out2 = out1[np.where( filt1>lLim )]
    return out2

def percentFilter(Filt, ToFilt):
    out1 = filterArray(Filt, ToFilt, np.percentile(Filt, 0),    np.percentile(Filt, 25))
    out2 = filterArray(Filt, ToFilt, np.percentile(Filt, 25), np.percentile(Filt, 50))
    out3 = filterArray(Filt, ToFilt, np.percentile(Filt, 50),  np.percentile(Filt, 75))
    out4 = filterArray(Filt, ToFilt, np.percentile(Filt, 75), np.percentile(Filt, 100))
    return [out1, out2, out3, out4]


# In[34]:


# ConsLiq_Liq = percentFilter(df['liquidityBonds'].values, df['liquidity'].values)
# ConsLiq_Sol = percentFilter(df['liquidityBonds'].values, df['solvency'].values)
# ConsLiq_Sec = percentFilter(df['liquidityBonds'].values, df['NPLofCI'].values)
# ConsLiq_Ass = percentFilter(df['liquidityBonds'].values, df['UBPR2170'].values)

# Liq_ConsLiq = percentFilter(df['liquidity'].values, df['liquidityBonds'].values)
# Liq_Sol = percentFilter(df['liquidity'].values, df['solvency'].values)
# Liq_Sec = percentFilter(df['liquidity'].values, df['NPLofCI'].values)
# Liq_Ass = percentFilter(df['liquidity'].values, df['UBPR2170'].values)

# Sol_ConsLiq = percentFilter(df['solvency'].values, df['liquidityBonds'].values)
# Sol_Liq = percentFilter(df['solvency'].values, df['liquidity'].values)
# Sol_Sec = percentFilter(df['solvency'].values, df['NPLofCI'].values)
# Sol_Ass = percentFilter(df['solvency'].values, df['UBPR2170'].values)

Sec_ConsLiq = percentFilter(df['NPLofCI'].values, df['liquidityBonds'].values)
Sec_Liq = percentFilter(df['NPLofCI'].values, df['liquidity'].values)
Sec_Sol = percentFilter(df['NPLofCI'].values, df['solvency'].values)
Sec_Ass = percentFilter(df['NPLofCI'].values, df['UBPR2170'].values)


# In[39]:


fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(10,10))

colorsList = ['darkred', 'red','orangered','darkorange']

labelList = ['0<p<25', '25<p<50','50<p<75','75<p<100']
kwargs1 = dict(histtype='stepfilled', alpha=0.3, bins=np.logspace(-3, 1.0, 25))
kwargs2 = dict(histtype='stepfilled', alpha=0.3, bins=np.logspace(-2, 1.0, 25))
kwargs3 = dict(histtype='stepfilled', alpha=0.3, bins=np.logspace(-11, 2, 25))
kwargs4 = dict(histtype='stepfilled', alpha=0.3, bins=np.logspace(-5, 2, 25))

axes[0,0].hist(df['liquidityBonds'].values, bins=np.logspace(-3, 1.0, 25), color = 'cyan')
axes[0,0].set_xscale("log")
axes[0,0].set_yscale("log")

axes[1,0].hist(Sol_Liq, color = colorsList,**kwargs1, label=labelList)
axes[1,0].set_xscale("log")
axes[1,0].set_yscale("log")

axes[2,0].hist(ConsLiq_Liq, color = colorsList,**kwargs1)
axes[2,0].set_xscale("log")
axes[2,0].set_yscale("log")

# axes[3,0].hist(Sec_Liq, color = colorsList,**kwargs1)
# axes[3,0].set_xscale("log")
# axes[3,0].set_yscale("log")

#=============================================
#=============================================

axes[0,1].hist(Liq_Sol, color = colorsList,**kwargs2)
axes[0,1].set_xscale("log")
axes[0,1].set_yscale("log")
axes[0,1].set_xlim([1e-2,1e0])

axes[1,1].hist(df['solvency'].values, bins=np.logspace(-2, 1.0, 25), color = 'cyan')
axes[1,1].set_xscale("log")
axes[1,1].set_yscale("log")
axes[1,1].set_xlim([1e-2,1e0])

axes[2,1].hist(ConsLiq_Sol, color = colorsList,**kwargs2)
axes[2,1].set_xscale("log")
axes[2,1].set_yscale("log")
axes[2,1].set_xlim([1e-2,1e0])

# axes[3,1].hist(Sec_Sol, color = colorsList,**kwargs2)
# axes[3,1].set_xscale("log")
# axes[3,1].set_yscale("log")
# axes[3,1].set_xlim([1e-2,1e0])

#=============================================
#=============================================

axes[0,2].hist(Liq_ConsLiq, color = colorsList,**kwargs3)
axes[0,2].set_xscale("log")
axes[0,2].set_yscale("log")

axes[1,2].hist(Sol_ConsLiq, color = colorsList,**kwargs3)
axes[1,2].set_xscale("log")
axes[1,2].set_yscale("log")

axes[2,2].hist(df['liquidityBonds'].values,bins=np.logspace(-11, 1, 25), color = 'cyan')
axes[2,2].set_xscale("log")
axes[2,2].set_yscale("log")

# axes[3,2].hist(Sec_ConsLiq, color = colorsList,**kwargs3)
# axes[3,2].set_xscale("log")
# axes[3,2].set_yscale("log")

#=============================================
#=============================================

# axes[0,3].hist(Liq_Sec, color = colorsList,**kwargs4)
# axes[0,3].set_xscale("log")
# axes[0,3].set_yscale("log")

# axes[1,3].hist(Sol_Sec, color = colorsList,**kwargs4)
# axes[1,3].set_xscale("log")
# axes[1,3].set_yscale("log")

# axes[2,3].hist(ConsLiq_Sec, color = colorsList,**kwargs4)
# axes[2,3].set_xscale("log")
# axes[2,3].set_yscale("log")

# axes[3,3].hist(df['NPLofCI'].values,bins=np.logspace(-5, 2, 25), color = 'cyan')
# axes[3,3].set_xscale("log")
# axes[3,3].set_yscale("log")

axes[0,1].set_yticks([])
axes[0,2].set_yticks([])
# axes[0,3].set_yticks([])

axes[1,1].set_yticks([])
axes[1,2].set_yticks([])
# axes[1,3].set_yticks([])

axes[2,1].set_yticks([])
axes[2,2].set_yticks([])
# axes[2,3].set_yticks([])

# axes[3,1].set_yticks([])
# axes[3,2].set_yticks([])
# axes[3,3].set_yticks([])

axes[0,0].set_xticks([])
axes[0,1].set_xticks([])
axes[0,2].set_xticks([])
# axes[0,3].set_xticks([])

axes[1,0].set_xticks([])
axes[1,1].set_xticks([])
axes[1,2].set_xticks([])
# axes[1,3].set_xticks([])

axes[2,0].set_xticks([])
axes[2,1].set_xticks([])
axes[2,2].set_xticks([])
# axes[2,3].set_xticks([])

axes[2,0].set_xlabel('Liquidity')
axes[2,1].set_xlabel('Solvency')
axes[2,2].set_xlabel('ConsLiqui')
# axes[2,3].set_xlabel('Security')

plt.subplots_adjust(hspace=0, wspace=0)

axes[1,0].legend(bbox_to_anchor=(0, 0), loc=3, borderaxespad=0, fontsize = 10)

# fig.tight_layout()
plt.savefig('test.pdf',dpi=800,bbox_inches='tight',pad_inches=0.02, format='pdf')
plt.show()


