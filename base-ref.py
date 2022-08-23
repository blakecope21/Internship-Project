import requests, itertools, csv, os
import pandas as pd
import numpy as np
import bs4 as bs
os.chdir("/Users/pblase/Documents/scraping_data")
headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}
s = requests.Session()

#Pull URL for WS
ws_url = "https://www.baseball-reference.com/postseason/2019_WS.shtml"

#Request html from page; load BeautifulSoup
r = requests.get(url = ws_url, headers = headers)
soup = bs.BeautifulSoup(r.text, 'lxml')

#Scrape for tables (tbody); pull Nationals batting data
len(soup.find_all('tbody'))
len(soup.find_all("table", {'id': 'post_batting_WSN'}))
nats_bat = soup.find("table", {'id': 'post_batting_WSN'})

#Inspect element; create DF
print(nats_bat)
#Loop to find player names
plyr_name = []
for i in nats_bat.find('tbody').find_all('tr'):
    plyr_name.append(i.find("th")["csk"])
    print(i.find("th")["csk"])

#Loop to find player names
#Row method
plyr_stat = []
plyr_col = ["AB", "HR", "OBP"]
for i in nats_bat.find('tbody').find_all('tr'):
    #Record Player Stats
    indiv_stat = []
    #AB
    indiv_stat.append(i.find("td", {"data-stat": "AB"}).get_text())
    #HR
    indiv_stat.append(i.find("td", {"data-stat": "HR"}).get_text())
    #OBP
    indiv_stat.append(i.find("td", {"data-stat": "onbase_perc"}).get_text())
    plyr_stat.append(indiv_stat)

#Finalize DF
plyr_stat = pd.DataFrame(plyr_stat, columns=plyr_col)
plyr_stat["Name"] = plyr_name
print(plyr_stat.head())

#Reorder columns
reord_col = ["Name", "AB", "HR", "OBP"]
plyr_stat = plyr_stat[reord_col]
print(plyr_stat.head())

#Column method
R = []
H = []
DOU = []
TPL = []
for i in nats_bat.find('tbody').find_all('tr'):
    #Runs
    R.append(i.find("td", {"data-stat": "R"}).get_text())    
    #Hits
    H.append(i.find("td", {"data-stat": "H"}).get_text())    
    #Doubles
    DOU.append(i.find("td", {"data-stat": "2B"}).get_text())    
    #Triples
    TPL.append(i.find("td", {"data-stat": "3B"}).get_text())

#Form with Dictionary
hit_df = pd.DataFrame({"Hits": H, "Runs": R, "Doubles": DOU, "Triples": TPL})
print(hit_df.head())

#Bind by Columns
plyr_stat = pd.concat([plyr_stat, hit_df], axis=1)
print(plyr_stat.head())
del hit_df

#Row binding
#Pull Astros Data
astros_bat = soup.find("table", {'id': 'post_batting_HOU'})
#Set up DF
plyr_stat1 = []
plyr_col = plyr_stat.columns.values
print(plyr_col)
for i in astros_bat.find('tbody').find_all('tr'):
    #Record Player Stats
    indiv_stat = []
    #Name
    indiv_stat.append(i.find("th")["csk"])
    #AB
    indiv_stat.append(i.find("td", {"data-stat": "AB"}).get_text())
    #HR
    indiv_stat.append(i.find("td", {"data-stat": "HR"}).get_text())
    #OBP
    indiv_stat.append(i.find("td", {"data-stat": "onbase_perc"}).get_text())
    #Runs
    indiv_stat.append(i.find("td", {"data-stat": "R"}).get_text())    
    #Hits
    indiv_stat.append(i.find("td", {"data-stat": "H"}).get_text())    
    #Doubles
    indiv_stat.append(i.find("td", {"data-stat": "2B"}).get_text())    
    #Triples
    indiv_stat.append(i.find("td", {"data-stat": "3B"}).get_text())
    #VCreate Row
    plyr_stat1.append(indiv_stat)

#Finalize DF1
plyr_stat1 = pd.DataFrame(plyr_stat1, columns=plyr_col)
print(plyr_stat1.head())

#Add team names
plyr_stat["Team"] = "WSH"
plyr_stat1["Team"] = "HOU"

#Row bind DFs
print(pd.concat([plyr_stat, plyr_stat1], axis=0).head())
plyr_stat = pd.concat([plyr_stat, plyr_stat1], axis=0)

#Reset Index; Save
print(plyr_stat.index)
plyr_stat = plyr_stat.reset_index(drop=True)
# plyr_stat.to_csv("plyr_stat.csv", index=False)
