#created by Kenneth Shinn and Stacey Chen

import requests
import csv
from unidecode import unidecode

api_key = 'ADD API KEY HERE'

with open('inputs/affiliationnamefreq100.tsv', encoding='latin-1') as tsvfile:
    with open('outputs/bing_output.tsv', 'w', newline="\n", encoding='utf-8') as out_file:
        
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(['affiliation', 'freq', 'formatted_address', 'locality', 'admin_district', 'country', 'lat', 'lng'])
        reader = csv.DictReader(tsvfile, dialect='excel-tab')
        cnt = 0
        
        for row in reader:
            cnt += 1
            
            #only print out every 100th number
            if cnt % 100 == 0:
                print(cnt)
            
            input_name = unidecode(str(row['affiliationname']))
            freq = row['freq']
            
            #bing
            response = requests.get("http://dev.virtualearth.net/REST/v1/Locations/?",
                        params={"query": input_name,
                                "include": "queryParse",
                                "key": api_key})
            
            #check if the API key is inputed
            if response.status_code == 401:
                print('API Key error: make sure that your API key is valid and inputed above')
                break
            
            try:
                response.json()
            except ValueError:
                tsv_writer.writerow([input_name, freq, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
                continue
           
            try:
                data = response.json()
                
                row_list = []
                row_list.append(input_name)
                row_list.append(freq)
                
                #note that we are assuming that the search engine returns the best result first
                address_data = None
                try:
                    address_data = data['resourceSets'][0]['resources'][0]['address']
                except IndexError:
                    #if there is no data returned from the API, just write out N/A and move on
                    tsv_writer.writerow([input_name, freq, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
                    continue
                
                # formatted_address
                try:
                    #bing
                    address = address_data['formattedAddress']
                    row_list.append(address)
                except:
                    row_list.append("N/A")
                
                # locality
                try:
                    #bing
                    locality = address_data['locality']
                    row_list.append(locality)
                except:
                    row_list.append("N/A")
                
                #admin district or state
                try:
                    #bing
                    admin_district = address_data['adminDistrict']
                    row_list.append(admin_district)
                except:
                    row_list.append("N/A")
                    
                # country
                try:
                    #bing
                    country = address_data['countryRegion']
                    row_list.append(country)
                except:
                    row_list.append("N/A")
                
                
                # get lat and long
                try:
                    #bing
                    lat = data['resourceSets'][0]['resources'][0]['point']['coordinates'][0]
                    lng = data['resourceSets'][0]['resources'][0]['point']['coordinates'][1]
                    row_list.append(lat)
                    row_list.append(lng)
                except:
                    row_list.append("N/A")
                    row_list.append("N/A")
                    
                tsv_writer.writerow(row_list)
                
            except:
                #try again, except now, print out the "unidecode" conversion to ASCII characters
                data = response.json()
            
                row_list = []
                row_list.append(input_name)
                row_list.append(freq)
                
                #note that we are assuming that the search engine returns the best result first
                address_data = data['resourceSets'][0]['resources'][0]['address']
                
                # formatted_address
                address = address_data['formattedAddress']
                row_list.append(unidecode(address))
                
                # locality
                locality = address_data['locality']
                row_list.append(unidecode(locality))
                
                #admin district or state
                admin_district = address_data['adminDistrict']
                row_list.append(unidecode(admin_district))
                
                # country
                country = address_data['countryRegion']
                row_list.append(unidecode(country))
                
                
                # get lat and long
                try:
                    #bing
                    lat = data['resourceSets'][0]['resources'][0]['point']['coordinates'][0]
                    lng = data['resourceSets'][0]['resources'][0]['point']['coordinates'][1]
                    row_list.append(lat)
                    row_list.append(lng)
                except:
                    row_list.append("N/A")
                    row_list.append("N/A")
                    
                tsv_writer.writerow(row_list)

                