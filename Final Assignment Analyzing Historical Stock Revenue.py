#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Installing necessary libraries
get_ipython().system('pip install yfinance')
get_ipython().system('pip install bs4')
get_ipython().system('pip install --upgrade nbformat')


# In[2]:


import requests
import pandas as pd
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf


# In[3]:


import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)


# In[4]:


#Defining the function make graph
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data.Date), y=stock_data.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data.Date), y=revenue_data.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


# ## Question 1: Use yfinance to Extract Stock Data
# 

# Reset the index, save, and display the first five rows of the `tesla_data` dataframe using the `head` function. Upload a screenshot of the results and code from the beginning of Question 1 to the results below.
# 

# In[5]:


tesla=yf.Ticker('TSLA')
tesla_data=tesla.history(period="max")
tesla_data.reset_index(inplace=True)
tesla_data.head()


# ## Question 2: Use Webscraping to Extract Tesla Revenue Data
# 

# Display the last five rows of the `tesla_revenue` dataframe using the `tail` function. Upload a screenshot of the results.

# In[6]:


url=" https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data=requests.get(url).text
beautiful_soup=BeautifulSoup(html_data,"html5lib")


# In[7]:


tables=beautiful_soup.find_all("table")
for index,table in enumerate(tables):
    if("Tesla Quarterly Revenue" in str(table)):
        table_index=index
tesla_revenue=pd.DataFrame(columns=["Date","Revenue"])
i = 0
for row in tables[table_index].tbody.find_all('tr'):
    col=row.find_all("td")
    date=col[0].text
    revenue=col[1].text.strip().replace("$","").replace(",","")
    tesla_revenue.loc[i,"Date"] = date=col[0].text
    tesla_revenue.loc[i,"Revenue"] = revenue=col[1].text.strip().replace("$","").replace(",","")
    i = i + 1
# I had to use an iteration with the i variable because the append was not working with tesla_revenue.


# In[8]:


tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
tesla_revenue.tail()


# ## Question 3: Use yfinance to Extract Stock Data
# 

# Reset the index, save, and display the first five rows of the `gme_data` dataframe using the `head` function. Upload a screenshot of the results and code from the beginning of Question 1 to the results below.
# 

# In[9]:


gmestop=yf.Ticker("GME")
gme_data=gmestop.history(period="max")
gme_data.reset_index(inplace=True)
gme_data.head()


# ## Question 4: Use Webscraping to Extract GME Revenue Data
# 

# Display the last five rows of the `gme_revenue` dataframe using the `tail` function. Upload a screenshot of the results.
# 

# In[10]:


url="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data=requests.get(url).text
beautiful_soup=BeautifulSoup(html_data,"html.parser")


# In[11]:


tables=beautiful_soup.find_all("table")
for index,table in enumerate(tables):
    #if(str(table)=="GameStop Quarterly Revenue"):
    if("GameStop Quarterly Revenue" in str(table)):
        table_index=index
gme_revenue=pd.DataFrame(columns=["Date","Revenue"])
i = 0 
for row in tables[table_index].tbody.find_all("tr"):
    col=row.find_all("td")
    date=col[0].text
    revenue=col[1].text.strip().replace("$","").replace(",","")
    gme_revenue.loc[i,"Date"] = date=col[0].text
    gme_revenue.loc[i,"Revenue"] = revenue=col[1].text.strip().replace("$","").replace(",","")
    i = i + 1
gme_revenue.tail()


# ## Question 5: Plot Tesla Stock Graph
# 

# Use the `make_graph` function to graph the Tesla Stock Data, also provide a title for the graph.
# Upload a screenshot of your results.
# 

# In[12]:


make_graph(tesla_data,tesla_revenue,'Tesla')


# ## Question 6: Plot GameStop Stock Graph
# 

# Use the `make_graph` function to graph the GameStop Stock Data, also provide a title for the graph. The structure to call the `make_graph` function is `make_graph(gme_data, gme_revenue, 'GameStop')`.
# 

# In[13]:


make_graph(gme_data,gme_revenue,'GameStop')


# <h2>Author:</h2> 
# 
# Douglas Senra
# 
