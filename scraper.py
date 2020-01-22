from bs4 import BeautifulSoup
import requests 
import csv
import re
import time

class Scraper:

    def __init__(self):

        self.url = 'http://338canada.com/districts/districts.htm'

        self.headers= {"User-Agent":
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

        try:
            self.r = requests.get(self.url, headers=self.headers)
        except:
            time.sleep(20)

        self.soup = BeautifulSoup(self.r.content, 'html.parser')
        self.tables = self.soup.findAll("table")[1:]

        self.entries = []

    def run(self):

        count = 0
        for entry in self.tables:
            table = entry.findAll("tr")
            for row in table:
                district = row.findAll("td")[0].renderContents().decode()
                district = district[district.find('_blank')+9: district.find('</a>')]
                district_url = row.findAll("td")[0].renderContents().decode()
                district_url = district_url[district_url.find('href=')+7: district_url.find('.htm')+4]
                projection = row.findAll("td")[1].renderContents().decode()
                projection = projection[projection.find('style="color:')+24: projection.find("</td></td></tr>")-4]

          

                try:
                    dis_r = requests.get(district_url, headers=self.headers)
                except:
                    print("Sleeping\n\n")
                    time.sleep(20)
                
                dis_soup = BeautifulSoup(dis_r.content, 'html.parser')
                
                region = (dis_soup.findAll('table')[0].findAll('tr')[0].findAll("td")[1].text.rstrip('\n').lstrip('\n').strip())
                print(projection)
                
                if region == 'Newfoundland and Labrador':
                    region = 'Newfoundland'
                if region == 'Prince Edward Island':
                    region = 'PEI'
                if region == 'New Brunswick':
                    region = 'NewBrunswick'
                if region == 'Northwest Territories':
                    region = 'NWT'
                if region == 'British Columbia':
                    region = 'BC'
                if region == 'Nova Scotia':
                    region = 'NovaScotia'

                script = dis_soup.findAll("script")[8].renderContents().decode()

                x = re.search('var moyennes = \[.*', script)
                info_arr = script[x.start()+15:x.end()][1:-1].split(',')
                parties = re.search('var parties = \[.*', script)
                parties = script[parties.start()+15:parties.end()-1].split(',')

                lpcIndex = parties.index("'LPC'")
                lpc = 0 if info_arr[lpcIndex] == '' else round(float(info_arr[lpcIndex]))

                cpcIndex = parties.index("'CPC'")
                cpc = 0 if info_arr[cpcIndex] == '' else round(float(info_arr[cpcIndex]))

                ndpIndex = parties.index("'NDP'")
                ndp = 0 if info_arr[ndpIndex] == '' else round(float(info_arr[ndpIndex]))

                gpcIndex = parties.index("'GPC'")
                gpc = 0 if info_arr[gpcIndex] == '' else round(float(info_arr[gpcIndex]))

                try:
                    bqIndex = parties.index("'BQ'")
                    bq = 0 if info_arr[bqIndex] == '' else round(float(info_arr[bqIndex]))
                except ValueError:
                    bq = 0
                
                try:
                    ppcIndex = parties.index("'PPC'")
                    ppc = 0 if info_arr[ppcIndex] == '' else round(float(info_arr[ppcIndex]))
                except ValueError:
                    ppc = 0

                try:
                    indIndex = parties.index("'IND'")
                    ind = 0 if info_arr[indIndex] == '' else round(int(info_arr[indIndex]))
                except ValueError:
                    ind = 0
        
                entry = {
                    'District': district,
                    'Projection': projection,
                    'Region': region,
                    'LPC': lpc,
                    'CPC': cpc,
                    'NDP': ndp,
                    'GPC': gpc,
                    'PPC': ppc,
                    'BQ': bq,
                    'IND': ind
                }
                
                self.entries.append(entry)
                print(entry)
                count += 1
                print(count)

    def save(self):
                        
        with open('updated_election_data.csv', 'w') as csvfile:
            fieldnames = ['District', 'Projection', 'Region', 'LPC', 'CPC', 'NDP', 'GPC', 'PPC', 'BQ', 'IND']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.entries)

        print('Success')
