# # pip install zenrows
# from zenrows import ZenRowsClient

# client = ZenRowsClient("e908ef9fa9c2ac53517423bb4e0469e6f5cabb0a")
# url = "https://www.mcmaster.com/products/base-plates/strut-channel-framing-component~floor-mount/material~rubber-2/material~stainless-steel-2/"
# params = {"js_render":"true","wait":"10000"}

# response = client.get(url, params=params)

# fpt=open("with_js_render_10SecWait.txt", "w")
# fpt.write(response.text)
# fpt.close()
#print(response.text)

# pip install zenrows
# pip install zenrows

import pandas as pd
import re
from bs4 import BeautifulSoup

# # pip install zenrows
from zenrows import ZenRowsClient

client = ZenRowsClient("e908ef9fa9c2ac53517423bb4e0469e6f5cabb0a")
url = "https://www.mcmaster.com/products/base-plates/strut-channel-framing-component~floor-mount/material~rubber-2/material~stainless-steel-2/"
params = {"js_render":"true","wait":"30000","js_instructions":"%5B%7B%22click%22%3A%22.PartNbrLnk%22%7D%2C%7B%22wait%22%3A500%7D%2C%7B%22wait_for%22%3A%22.slow_selector%22%7D%2C%7B%22click%22%3A%22.CadControl_downloadButton__1aJXP%22%7D%2C%7B%22wait%22%3A1000%7D%2C%7B%22wait_for%22%3A%22.slow_selector%22%7D%5D"}

response = client.get(url, params=params)

#print(response.text)
# import pandas as pd

# <a href="/mvD/Library/M4/20240306/12FBF2C9/33145T54_Strut Channel Floor Mount.SLDPRT" download="" class="CadControl_downloadAnchor__oAeur" tabindex="-1" aria-hidden="true">
# <button class="CadControl_downloadButton__1aJXP">Download

#data = response.text
class_to_col_map= {'dx ea ek eq eu':'Ht.', 'dx ea ek ev 1':'Wd.', 'dx ea ek es 1':'Lg.', 'dx ea ek es 2':'Wd_.', 'dx ea ek es 3':'Ht_.', 'dx ea ek es 4':'Thick.', 'dx ea ek es 5':'Fasteners Included', 'dx ea ek eu 1':'No. of', 'dx ea ek eu 2':'Dia.1', 'dx ea ek ev 2':'Ctr.-to-Ctr.MH', 'dx ea ek eu 3':'Dia.2', 'dx ea ek ew':'Ctr.-to-Ctr.PH', 'dx eb ek ex':'CadControl', 'dx ec ek fb fc':'Price'}
data_dictionary= {'Header':[], 'SubHeader':[], 'Ht.':[], 'Wd.':[], 'Lg.':[], 'Wd_.':[], 'Ht_.':[], 'Thick.':[], 'Fasteners Included':[], 'No. of':[], 'Dia.1':[], 'Ctr.-to-Ctr.MH':[], 'Dia.2':[], 'Ctr.-to-Ctr.PH':[], 'CadControl':[], 'Price':[], 'url_sldprt':[]}
# fpt=open("with_js_render_30SecWait.txt", "r")
# data = fpt.readlines()
# fpt.close()
soup = BeautifulSoup(response.text, 'html.parser')
#soup = BeautifulSoup(open("with_js_render_30SecWait.html", encoding="latin-1"), 'html.parser')
#soup = BeautifulSoup(response.text, 'html.parser')
parent_url ='https://www.mcmaster.com'
a_tag = soup.find('a', class_='CadControl_downloadAnchor__oAeur')

table = soup.find('table', class_='hn')
div_tag = soup.find("div", class_="hl ie")

# title = div_tag.text.strip()
# if title:
#     print(title.find('div').text.strip())
table_data = []
main_hdr_text, sub_hdr_text = "", ""
for row in table.tbody.find_all('tr'):
    header = row.find('th')
    if header:
        main_header = header.find('div', class_='hl ie')
        if main_header:
            main_hdr_text = main_header.text

        if  header.find('div', class_='hw ig'):
            sub_hdr_text =  header.find('div', class_='hw ig').text
        elif header.find('div', class_='hw ig dv'):
            sub_hdr_text =  header.find('div', class_='hw ig dv').text

    if main_hdr_text and sub_hdr_text:
        data_dictionary['Header'].append(main_hdr_text)
        data_dictionary['SubHeader'].append(sub_hdr_text)
    
    #print(header.find('div').text)

    #.find('div', class_='hw ig').text.strip()
    columns = row.find_all('td')

    if columns != []:
        #print(len(columns))
        dx_ea_ek_es=1
        dx_ea_ek_eu=1
        dx_ea_ek_ev=1

        for i,cols in enumerate(columns):
            if cols.find(class_='CadControl_downloadAnchor__oAeur'):
                if a_tag and 'download' in a_tag.text.lower():
                    data_dictionary['url_sldprt'].append(parent_url+a_tag['href'])
            
            attr=""
            elements = cols.get('class')
            if isinstance(elements , (list)):
                attr = " ".join(elements)
            # for elem in elements:
            #     attr = attr + " " + elem
            # print(attr)

            if attr == "dx ea ek eq eu": #and len(cols.text.strip())>0:                  # <td class="dx ea ek eq eu">1 <span class="ae">5/8</span>"</td>
                data_dictionary[class_to_col_map["dx ea ek eq eu"]].append(cols.text.strip())
            
            if attr == "dx ea ek ev" and dx_ea_ek_ev == 1:                   # <td class="dx ea ek ev">1 <span class="ae">5/8</span>"</td>
                data_dictionary[class_to_col_map["dx ea ek ev 1"]].append(cols.text.strip())
                dx_ea_ek_ev += 1

            elif attr == "dx ea ek ev" and dx_ea_ek_ev == 2:                 # <td class="dx ea ek ev" style="text-indent:7px;">4 <span class="ae">1/4</span>"</td>
                data_dictionary[class_to_col_map["dx ea ek ev 2"]].append(cols.text.strip())
                dx_ea_ek_ev = 1

            if attr == "dx ea ek es" and dx_ea_ek_es == 1:                     # <td class="dx ea ek es" style="text-indent:7px;">6"</td>
                data_dictionary[class_to_col_map["dx ea ek es 1"]].append(cols.text.strip())
                dx_ea_ek_es += 1

            elif attr == "dx ea ek es" and dx_ea_ek_es == 2:                     # <td class="dx ea ek es" style="text-indent:7px;">6"</td>
                data_dictionary[class_to_col_map["dx ea ek es 2"]].append(cols.text.strip())
                dx_ea_ek_es += 1

            elif attr == "dx ea ek es" and dx_ea_ek_es == 3:                     #  <td class="dx ea ek es">3 <span class="ae">3/4</span>"</td>
                data_dictionary[class_to_col_map["dx ea ek es 3"]].append(cols.text.strip())
                dx_ea_ek_es += 1

            elif attr == "dx ea ek es" and dx_ea_ek_es == 4:                     # <td class="dx ea ek es"><span class="ae">1/4</span>"</td>
                data_dictionary[class_to_col_map["dx ea ek es 4"]].append(cols.text.strip())
                dx_ea_ek_es += 1

            elif attr == "dx ea ek es" and dx_ea_ek_es == 5:                    #  <td class="dx ea ek es">No</td> 
                data_dictionary[class_to_col_map["dx ea ek es 5"]].append(cols.text.strip())
                dx_ea_ek_es = 1

            if attr == "dx ea ek eu" and dx_ea_ek_eu == 1:                       # <td class="dx ea ek eu">4</td>               
                data_dictionary[class_to_col_map["dx ea ek eu 1"]].append(cols.text.strip())   
                dx_ea_ek_eu += 1

            elif attr == "dx ea ek eu" and dx_ea_ek_eu == 2:                    #  <td class="dx ea ek eu"><span class="ae">3/4</span>"</td>
                data_dictionary[class_to_col_map["dx ea ek eu 2"]].append(cols.text.strip())
                dx_ea_ek_eu += 1

            elif attr == "dx ea ek eu" and dx_ea_ek_eu == 3:                    # <td class="dx ea ek eu"><span class="ae">9/16</span>"</td>
                data_dictionary[class_to_col_map["dx ea ek eu 3"]].append(cols.text.strip())
                dx_ea_ek_eu = 1

            if re.search(r"^dx ea ek ew", attr):                                            # <td class="dx ea ek ew">1 <span class="ae">7/8</span>"</td>
                data_dictionary[class_to_col_map["dx ea ek ew"]].append(cols.text.strip())        

            if (attr == "dx eb ek ex" or attr == "dx eb ek InLnOrdWebPartLayout_ItmTblPartNbrCell AddToOrdBxCreated"):                                            # <td class="dx eb ek ex">
                data_dictionary[class_to_col_map["dx eb ek ex"]].append(cols.text.strip())

            if attr == "dx ec ek fb fc":                   # <td class="dx ec ek fb fc">125.12</td>
                data_dictionary[class_to_col_map["dx ec ek fb fc"]].append(cols.text.strip())

print(data_dictionary)
max_so_far = 0
for key,val in data_dictionary.items():
    max_so_far = max ( len(data_dictionary[key]), max_so_far)

for key,val in data_dictionary.items():
    for i in range(max_so_far-len(data_dictionary[key])):
        data_dictionary[key].append(None)

#print("key : ", key, "Total Value = ", len(data_dictionary[key]))

df = pd.DataFrame(data_dictionary)
df.to_csv('all_data.csv')