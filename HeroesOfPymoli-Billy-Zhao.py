#!/usr/bin/env python
# coding: utf-8

# ### Observation 1: Male dominate the purchasing of online games with over 85% of total players
# ### Observation 2: Age 15-29 are the most active players, occupying more than 60% of total player population
# ### Observation 3: Purchases seem to be fairly evenly distributed among players, with most of them purchase only 1-2 items (with 5 at most)
# ### Observation 4: Even though female players are a much smaller group, they tend to spend more. On average they spend .40 more (10%) than their male counterpart.

# In[1]:


# import dependencies
import pandas as pd
import numpy as np


# In[2]:


# import input dataset file
fname = 'Resources/purchase_data.csv'
purchase_data = pd.read_csv(fname, encoding='utf8')


# In[3]:


## Player Count - quick review of the dataframe
purchase_data.head()


# In[4]:


# function to add $ sign and formatting to money
def as_currency(amount):
    if amount >= 0:
        return '${:,.2f}'.format(amount)
    else:
        return '-${:,.2f}'.format(-amount)


# In[5]:


# function to add 2 dicimal formatting to percentages
def as_percent(number):
    return '{:.2f}'.format(number)


# In[6]:


# list total players
totalPlayers = len(purchase_data['SN'].unique())
summary_table = pd.DataFrame({'Total Players': [totalPlayers]})
summary_table


# In[7]:


## Purchasing Analysis (Total)
uniqueItems = len(purchase_data['Item ID'].unique())
averagePrice = as_currency(round(purchase_data['Price'].mean(),2))
numberOfPurchases = purchase_data['Purchase ID'].count()
totalRevenue = as_currency(sum(purchase_data['Price']))
summary_table2 = pd.DataFrame({'Unique Items': [uniqueItems], 
                              'Average Price': [averagePrice], 
                              'Number of Purchases': [numberOfPurchases],
                              'Total Revenue': [totalRevenue]})
summary_table2.head()                               


# In[8]:


## Gender Demographics - Observation 1: Male dominate the purchasing of online games with over 85% of total
# this filters out all the duplicated SNs which return unique list of players with Gender
df2 = purchase_data.loc[:, ['Gender','SN','Age']].drop_duplicates()

# this creates a series of Gender and total
genderCount_s = df2.Gender.value_counts()

# creates percentages
genderTotalCount = df2['Gender'].value_counts().sum()
genderPctCount = (genderCount_s / genderTotalCount * 100)

gender_summary_table = pd.DataFrame({'Total Count' : genderCount_s, '% of Players' : genderPctCount.apply(as_percent)})
gender_summary_table


# In[9]:


## Purchasing Analysis (Gender)
gp1 = purchase_data.groupby('Gender')

purchaseCount_s = gp1['Purchase ID'].count()
avgPrice = gp1['Price'].mean()
totalValue = gp1['Price'].sum()
avgPerPerson = (totalValue / genderCount_s)

purchase_summary_table = pd.DataFrame(
    {
        'Purchase Count': purchaseCount_s,
        'Average Purchase Price': avgPrice.apply(as_currency),
        'Total Purchase Value': totalValue.apply(as_currency),
        'Avg Total Purchase per Person': avgPerPerson.apply(as_currency)
        
    }
)
purchase_summary_table


# In[10]:


## Age Demographics

bins = [0, 9, 14, 19, 24, 29, 34, 39, 49]
labels = ['<10', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40+']

df2['Group'] = pd.cut(df2['Age'], bins, labels=labels)
df2.head()

gp2 = df2.groupby('Group')
ageCount = gp2['Age'].count()
ageCountTotal = gp2['Age'].count().sum()
agePctCount = ageCount / ageCountTotal * 100

age_summary_table = pd.DataFrame(
    {
        'Total Count' : ageCount,
        'percentage of Players' : agePctCount.apply(as_percent)
    }
)
age_summary_table


# In[12]:


## Purchasing Analysis (Age)
# add a group column to original dataframe
purchase_data['Group'] = pd.cut(purchase_data['Age'], bins, labels=labels)

gp3 = purchase_data.groupby('Group')

agePurchaseCount = gp3['Purchase ID'].count()
ageTotalPurchasePrice = gp3['Price'].sum()
avgPurchasePrice = gp3['Price'].mean()

avgTotalPerPerson = ageTotalPurchasePrice / ageCount

age_summary_table2 = pd.DataFrame(
    {
        'Purchase Count' : agePurchaseCount,
        'Average Purchase Price' : avgPurchasePrice.apply(as_currency),
        'Total Purchase Value' : ageTotalPurchasePrice.apply(as_currency),
        'Avg Total Per Person' : avgTotalPerPerson.apply(as_currency)
    }
)

age_summary_table2


# In[13]:


## Top Spenders
top_spenders_gp = purchase_data.groupby('SN')

topPurchaseCount = top_spenders_gp['SN'].count()

topTotal = top_spenders_gp['Price'].sum()

topAvgPrice = topTotal / topPurchaseCount


# In[14]:


top_spending_df = pd.DataFrame(
    {
        'Purchase Count': topPurchaseCount,
        'Avg Purchase Price': topAvgPrice.apply(as_currency),
        'Total Purchase Value': topTotal
    }
)
top_spender_summary = top_spending_df.sort_values(['Total Purchase Value'],  ascending=False)


top_spender_summary['Total Purchase Value'] = top_spender_summary['Total Purchase Value'].apply(as_currency)
top_spender_summary.head()


# In[15]:


## Most Popular Items
pop_item_df = purchase_data.loc[:,['Item ID', 'Item Name', 'Price']]

pop_item_gp = pop_item_df.groupby(['Item ID', 'Item Name'])

popPurchaseCount = pop_item_gp['Item ID'].count()

popItemPrice = pop_item_gp['Price'].mean()

popItemTotal = popPurchaseCount * popItemPrice

popPurchaseCount

pop_item_summary = pd.DataFrame(
    {
        'Purchase Count': popPurchaseCount,
        'Item Price': popItemPrice.apply(as_currency),
        'Total Purchase Value': popItemTotal
    }
)
pop_item_summary1 = pop_item_summary.sort_values(['Purchase Count'], ascending=False)
pop_item_summary1['Total Purchase Value'] = pop_item_summary1['Total Purchase Value'].apply(as_currency)
pop_item_summary1.head()


# In[16]:


## Most Profitable Items
pop_item_summary2 = pop_item_summary.sort_values(['Total Purchase Value'], ascending=False)

pop_item_summary2['Total Purchase Value'] = pop_item_summary2['Total Purchase Value'].apply(as_currency)

pop_item_summary2.head()


# In[17]:


get_ipython().system('jupyter nbconvert --to python HeroesOfPymoli-Billy-Zhao.ipynb')

