#created by Kenneth Shinn and Stacey Chen

import requests
import csv
from unidecode import unidecode

api_key = 'ADD API KEY HERE'

with open('inputs/affiliationnamefreq100.tsv', encoding='latin-1') as tsvfile:
    with open('outputs/google_output.tsv', 'w', newline="\n", encoding='utf-8') as out_file:
        
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(['affiliation', 'freq', "formatted_address",'locality', 'admin_district', 'country', 'lat', 'lng'])
        reader = csv.DictReader(tsvfile, dialect='excel-tab')
        cnt = 0
        
        for row in reader:
            cnt += 1
            
            #only print out every 100th number
            if cnt % 100 == 0:
                print(cnt)
                
            row_information = []
            
            input_name = unidecode(str(row['affiliationname']))
            row_information.append(input_name)
            
            freq = row['freq']
            row_information.append(freq)
            
            #google
            response = requests.get("https://maps.googleapis.com/maps/api/geocode/json", 
                    params={"key": api_key, 
                            "address": input_name})
            
            #check if the API key is inputed
            if response.json()['status'] == 'REQUEST_DENIED':
                print('API Key error: make sure that your API key is valid and inputed above')
                break
            
            try:
                response.json()
            except ValueError:
                tsv_writer.writerow([input_name, freq, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
                continue
            
            try:
                data = response.json()
                
                #note that we are assuming that the search engine returns the best result first
                data_results = None
                if data['status'] == 'ZERO_RESULTS':
                    #if there is no data returned from the API, just write out N/A and move on
                    tsv_writer.writerow([input_name, freq, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
                    continue
                else:
                    data_results = data['results'][0]
                
            
                #get the formatted address
                try:
                    formatted_address = data_results['formatted_address']
                    row_information.append(formatted_address)
                except:
                    row_information.append("N/A")
                    
                #get locality
                try:
                    for component in data_results['address_components']:
                        if 'locality' in component['types'] or 'sublocality' in component['types']:
                            locality = component['long_name']
                    row_information.append(locality)
                except:
                    row_information.append("N/A")
                    
                #get the admin district
                try:
                    for component in data_results['address_components']:
                        if 'administrative_area_level_1' in component['types']:
                            admin_district = component['long_name']
                    row_information.append(admin_district)
                except:
                    row_information.append("N/A")
                            
                #get the country
                try:
                    for component in data_results['address_components']:
                        if 'country' in component['types']:
                            country = component['long_name']
                    row_information.append(country)
                except:        
                    row_information.append("N/A")
                    
                try:
                    lat = data_results['geometry']['location']['lat']
                    lng = data_results['geometry']['location']['lng']
                except:
                    lat = "N/A"
                    lng = "N/A"
                    
                row_information.append(lat)
                row_information.append(lng)
                
                tsv_writer.writerow(row_information)
            
            except:
                #try again, except now, print out the "unidecode" conversion to ASCII characters
                data = response.json()
                
                #note that we are assuming that the search engine returns the best result first
                data_results = data['results'][0]
                
                row_information = []
                row_information.append(input_name)
                row_information.append(freq)
            
                #get the formatted address
                try:
                    formatted_address = data_results['formatted_address']
                    row_information.append(unidecode(formatted_address))
                except:
                    row_information.append("N/A")
                    
                #get locality
                try:
                    for component in data_results['address_components']:
                        if 'locality' in component['types'] or 'sublocality' in component['types']:
                            locality = component['long_name']
                    row_information.append(unidecode(locality))
                except:
                    row_information.append("N/A")
                    
                #get the admin district
                try:
                    for component in data_results['address_components']:
                        if 'administrative_area_level_1' in component['types']:
                            admin_district = component['long_name']
                    row_information.append(unidecode(admin_district))
                except:
                    row_information.append("N/A")
                            
                #get the country
                try:
                    for component in data_results['address_components']:
                        if 'country' in component['types']:
                            country = component['long_name']
                    row_information.append(unidecode(country))
                except:        
                    row_information.append("N/A")
                    
                try:
                    lat = data_results['geometry']['location']['lat']
                    lng = data_results['geometry']['location']['lng']
                except:
                    lat = "N/A"
                    lng = "N/A"
                    
                row_information.append(lat)
                row_information.append(lng)
                
                tsv_writer.writerow(row_information)
