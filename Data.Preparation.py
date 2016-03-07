# -*- coding: utf-8 -*-
"""
Retrieve data from World Bank API (wbdata) and stored into MySQL database
"""

import wbdata
import pandas as pd
import datetime
import MySQLdb as myDB

#### test if data for certain indicator, country and year is available
def test_year(ind, ctry, year):
    import wbdata    
    data = []    
    #### limit time frame to one year as the study only need one year data    
    data_date = (datetime.datetime(year, 1, 1), datetime.datetime(year, 1, 1))
    data = wbdata.get_data(ind, ctry, data_date)
    for c in data:
        if c['value'] == None:
            print 'Country:', c['country']['value']
            print 'Data:', c['indicator']['value']
            print 'Year:', c['date']
            print 'Staus:', 'NOT available'
        else:
            print 'Country:', c['country']['value']
            print 'Data:', c['indicator']['value']
            print 'Year:', c['date']            
            print 'Staus:', 'Available'
    
#### extract data from returned dictionary
def get_value(ind, ctry, year):
    raw_data = []
    data_date = (datetime.datetime(year, 1, 1), datetime.datetime(year, 1, 1))
    raw_data = wbdata.get_data(ind, country = ctry, data_date=data_date)
  
    data = []
    for country in raw_data:
        data.append(country['value'])
    return data
    
#### extract country names from returned dictionary
def get_countryList(ind, ctry, year):
    raw_data = []
    data_date = (datetime.datetime(year, 1, 1), datetime.datetime(year, 1, 1))
    raw_data = wbdata.get_data(ind, country = ctry, data_date=data_date)    
    
    data = []    
    for country in raw_data:
        data.append(country['country']['value'])
    return data
    
countries=["AGO","BEN","GMB","ZMB","SAU","IND","EGY","IRN","USA",
           "GBR","FRA","MLI","AUS","COL","NPL","BTN","ALB","TGO",
           "SEN","TZA","NZL","PER","LBN","PAK","PHL","IDN","THA",
           "OMN","ISR","BRA","CHL","GIN","SLE"]

#### convert string type to float type for numeric data
GDP = [float(x) for x in get_value("NY.GDP.PCAP.KD",countries,2005)]
Exp_Edu = [float(x) for x in get_value("SE.XPD.TOTL.GD.ZS",countries,2005)]
Fer_Rate = [float(x) for x in get_value("SP.DYN.TFRT.IN",countries,2005)]
Country = get_countryList("NY.GDP.PCAP.KD",countries,2005)

#### get region information for given country
def get_region(countries):
    regions = []
    all = wbdata.get_country(countries)    
    for country in all:
        region = country['region']['value']
        #### cut residual information        
        flag = region.find('(')
        if flag>0:        
            region = region[0:flag-1]
        regions.append(region)
    return regions
    
#### get income level information for given country
def get_incomeLevel(countries):
    incomes = []
    all = wbdata.get_country(countries)
    for country in all:
        income = country['incomeLevel']['value']
        #### cut residual information          
        flag = income.find(':')
        if flag>0:
            income = income[0:flag]
        incomes.append(income)
    return incomes
        
Region = get_region(countries)
Income_Level = get_incomeLevel(countries)
        
#### create a dictionary for data frame
myDic = { 'Country':  Country,
          'GDP':      GDP,
          'Expenditure on Education': Exp_Edu,
          'Fertility Rate': Fer_Rate,
          'Income Level': Income_Level,
          'Region': Region
        }

#### convert dictionary to data frame
myDF = pd.DataFrame(myDic)

#### create connection to MySQL
conn = myDB.connect('localhost','root')
cursor = conn.cursor()

sql = ' SHOW DATABASES; '
cursor.execute(sql)

#### test if the database name is used before, drop if used
sql = ' DROP DATABASE IF EXISTS DB; '
cursor.execute(sql)

sql = ' CREATE DATABASE DB; '
cursor.execute(sql)

#### create connection to the database created in last step
mydb = myDB.connect(host='localhost', user='root',passwd='', db='DB')

#### upload data frame to MySQL
myDF.to_sql(con = mydb, name = 'mydata', if_exists = 'replace', flavor = 'mysql')

