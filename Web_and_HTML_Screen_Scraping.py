#Go to the Top500 SuperComputer Web site at https://www.top500.org/list/2018/06/

#View the page source and inspect the HTML table code for the entries.

#Note the fields in the table: Rank, System, Cores, RMax, RPeak, Power.
#Using Python with BeautifulSoup, extract the data from the Web site and create a csv dataset containing that data.
#Clean & explore the dataset, producing summary statistics for Cores, RMax, RPeak, and Power.
#Display and explain the relationship between
#Cores and RPeak
#Cores and Power

import csv, os, math, operator, pickle, time, random, re, collections

import numpy as np

import pandas as pd

import matplotlib.pyplot as plt
#%matplotlib inline

from collections import Counter
import statistics as stat

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

data_dir = "C:\PythonData"

os.chdir(data_dir)

for page in range(1, 6):
    my_url = 'https://www.top500.org/list/2018/06/?page={}'.format(page)
    #print(my_url)
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()

    #Parse the page
    page_soup = soup(page_html, 'html.parser')
    #print(page_soup.h1) #Check page header

    #for sibling in page_soup.find('br').next_siblings:
    #    data = br.find('br').next_sibling
     #print(sibling)

    cols = page_soup.find_all('tr')

    filecountry = "TOP500ListJune2018_Country.txt"

    if(page == 1):
        f = open(filecountry, "w")
    else:
        f = open(filecountry, "a")

    for col in cols:
        brs = col.find_all('br', limit =1)
        for br in brs:
            #print(br.next_sibling)
            f.write(br.next_sibling + '\n')
    f.close()


    ## a.Using Python with BeautifulSoup, extract the data from the Web site and create a csv dataset containing that data.
    ## Scrape data from 'https://www.top500.org/list/2018/06/'
    filename = "TOP500ListJune2018.txt"

    if(page == 1):
        f = open(filename, "w")
    else:
        f = open(filename, "a")

    for col in cols:
        td = col.findChildren('td')

        i = 1
        for child in td:
            if (i % 7 == 0):
                ##print(child.text + "\t")
                string = "\t".join(child.text.splitlines())
                f.write(string.replace(',', '') + '\t' + '\n')
            else:
                ##print(child.text)
                string = "\t".join(child.text.splitlines())
                f.write(string.replace(',','') + "\t")
            i = i+1
    f.close()


## b.Clean & explore the dataset, producing summary statistics for Cores, RMax, RPeak, and Power.
## Read text file, Clean data, and Create csv file
ColumnNames = ['Rank', 'Site', 'System', 'Cores', 'RMax', 'RPeak', 'Power']
df = pd.read_table('./TOP500ListJune2018.txt', sep = r'\t{1,}', engine = 'python',
                    usecols=[0, 1, 3, 4, 5, 6, 7],
                   skipinitialspace = True, header = None, names = ColumnNames)

df.replace({'System':' '}, '', regex = True, inplace = True)
df.Cores = pd.to_numeric(df.Cores, errors='coerce')

df1 = pd.read_table('./TOP500ListJune2018_Country.txt', sep = '\r\n', engine = 'python', names = ['Country'], header = None)

bigdata = pd.concat([df, df1], ignore_index = False, sort = False, axis = 1)
bigdata.to_csv('TOP500ListJune2018.csv')
#print(bigdata)
#print(bigdata.dtypes)

##Drop rows including missing values
bigdata_withoutNA = bigdata.dropna()
#bigdata_withoutNA.to_csv('test.csv')

##produce summary statistics for Cores, RMax, RPeak, and Power.
print(bigdata_withoutNA)
print(bigdata_withoutNA.dtypes)
print(bigdata_withoutNA.describe(include = [np.float64])) #RMax, #RPeak, #Power

##c. Display and explain the relationship between
#Cores and RPeak
ax = bigdata_withoutNA.Cores
ay = bigdata_withoutNA.RPeak

plt.xscale('log')
plt.yscale('log')
plt.scatter(ax, ay)

plt.title("Relationship between Cores and RPeak")
plt.xlabel("Cores")
plt.ylabel("RPeak")
plt.show()

#Cores and Power
ax = bigdata_withoutNA.Cores
ay = bigdata_withoutNA.Power

plt.xscale('log')
plt.yscale('log')
plt.scatter(ax, ay)

plt.title("Relationship between Cores and Power")
plt.xlabel("Cores")
plt.ylabel("Power")
plt.show()

##Display summary statistics and visualizations for the Country data.
Count_Country = Counter(bigdata_withoutNA.Country)
print(Count_Country)

x = collections.Counter(bigdata_withoutNA.Country)
l = range(len(x.keys()))
plt.bar(l, x.values(), align = 'center')
plt.xticks(l, x.keys(), fontsize = 7, rotation = 25)
plt.show()
