# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 10:44:53 2019

@author: ywestra
"""

import json
import os
import geocoder
import time 
import pandas as pd

startrun = time.time()
os.chdir('C:\Python\CSV')
cd = os.getcwd()

########################################
#               Loop 1                 #
# Locaties                             #
########################################
start = time.time()


df_locaties = pd.DataFrame(columns = ['UniqueID','GemeenteNr', 'Locatie', 'Naam', 'Link', 'Soort','Adres','Pc_Wpl','Houder_link','Houder_naam','Lat','Lng'])

with open('Resultaat loop 4.json') as f:
    data = json.load(f)

gemeenteNR = list(data.keys())

for gemeente in gemeenteNR:
   
    for identifier in data[gemeente].keys():
        
        if data[gemeente][identifier]['Soort']  == '(Gastouderbureau)':
            
            lookupadres = data[gemeente][identifier]['Contactgegevens']['Vestigingsadres']['Adres'] +", "+data[gemeente][identifier]['Contactgegevens']['Vestigingsadres']['Postcode']+" "+data[gemeente][identifier]['Contactgegevens']['Vestigingsadres']['Plaats']
            g = geocoder.arcgis(lookupadres)

            new_row = {'UniqueID':str(gemeente)+"-"+str(identifier),'GemeenteNr':str(gemeente), 'Locatie':str(identifier), 'Naam':data[gemeente][identifier]['Naam'], 'Link':data[gemeente][identifier]['Link'], 'Soort':data[gemeente][identifier]['Soort'], 'Adres':data[gemeente][identifier]['Adres'], 'Pc_Wpl':data[gemeente][identifier]['Pc_Wpl'], 'Houder_link':data[gemeente][identifier]['Houder_link'], 'Houder_naam':data[gemeente][identifier]['Houder_naam'],'Lat':g.lat, 'Lng':g.lng}
            df_locaties = df_locaties.append(new_row, ignore_index=True)
             
        else:
            new_row = {'UniqueID':str(gemeente)+"-"+str(identifier),'GemeenteNr':str(gemeente), 'Locatie':str(identifier), 'Naam':data[gemeente][identifier]['Naam'], 'Link':data[gemeente][identifier]['Link'], 'Soort':data[gemeente][identifier]['Soort'], 'Adres':data[gemeente][identifier]['Adres'], 'Pc_Wpl':data[gemeente][identifier]['Pc_Wpl'], 'Houder_link':data[gemeente][identifier]['Houder_link'], 'Houder_naam':data[gemeente][identifier]['Houder_naam'],'Lat':data[gemeente][identifier]['Coordinaten']['Lat'], 'Lng':data[gemeente][identifier]['Coordinaten']['Lng']}
            df_locaties = df_locaties.append(new_row, ignore_index=True)
        
export_csv = df_locaties.to_csv (r'locaties.csv', index = None, header=True, sep='\t')  

end = time.time()

Duur_loop1 = end - start
print("Loop 1: "+str(Duur_loop1))

########################################
#               Loop 2                 #
# Kerngegevens                         #
########################################
start = time.time()
df_kerngegevens = pd.DataFrame(columns = ['UniqueID','GemeenteNr', 'Locatie', 'Naam', 'Soort_voorziening', 'Aantal_kindplaatsen','Huidige_status','Geregistreerd_vanaf','Verantwoordelijke_gemeente','LRK_nummer'])

with open('Resultaat loop 4.json') as f:
    data = json.load(f)

gemeenteNR = list(data.keys())

for gemeente in gemeenteNR:
   
    for identifier in data[gemeente].keys():
        if data[gemeente][identifier]['Soort']  == '(Gastouderbureau)':  
            new_row = {'UniqueID':str(gemeente)+"-"+str(identifier),'GemeenteNr':str(gemeente),'Locatie':str(identifier),'Naam':data[gemeente][identifier]['Kerngegevens']['Naam'],'Soort_voorziening':data[gemeente][identifier]['Kerngegevens']['Soort voorziening'],'Aantal_kindplaatsen':None,'Huidige_status':data[gemeente][identifier]['Kerngegevens']['Huidige status'],'Geregistreerd_vanaf':data[gemeente][identifier]['Kerngegevens']['Geregistreerd vanaf'],'Verantwoordelijke_gemeente':data[gemeente][identifier]['Kerngegevens']['Verantwoordelijke gemeente'],'LRK_nummer':data[gemeente][identifier]['Kerngegevens']['Registratienummer Landelijk Register']}
            df_kerngegevens = df_kerngegevens.append(new_row, ignore_index=True)

        else:
            new_row = {'UniqueID':str(gemeente)+"-"+str(identifier),'GemeenteNr':str(gemeente),'Locatie':str(identifier),'Naam':data[gemeente][identifier]['Kerngegevens']['Naam'],'Soort_voorziening':data[gemeente][identifier]['Kerngegevens']['Soort voorziening'],'Aantal_kindplaatsen':str(data[gemeente][identifier]['Kerngegevens']['Aantal kindplaatsen']),'Huidige_status':data[gemeente][identifier]['Kerngegevens']['Huidige status'],'Geregistreerd_vanaf':data[gemeente][identifier]['Kerngegevens']['Geregistreerd vanaf'],'Verantwoordelijke_gemeente':data[gemeente][identifier]['Kerngegevens']['Verantwoordelijke gemeente'],'LRK_nummer':data[gemeente][identifier]['Kerngegevens']['Registratienummer Landelijk Register']}
            df_kerngegevens = df_kerngegevens.append(new_row, ignore_index=True)    
        
export_csv = df_kerngegevens.to_csv (r'kerngegevens.csv', index = None, header=True, sep='\t') 

end = time.time()

Duur_loop2 = end - start
print("Loop 2: "+str(Duur_loop2))

########################################
#               Loop 3                 #
# Contactgegevens                      #
########################################
start = time.time()
df_contactgegevens = pd.DataFrame(columns = ['UniqueID','GemeenteNr', 'Locatie','Opvang_adres','Opvang_postcode','Opvang_plaats', 'Vestiging_adres', 'Vestiging_postcode', 'Vestiging_plaats','Correspondentie_adres','Correspondentie_postcode','Correspondentie_plaats','Contactpersoon','E-mail','Telefoon','Website'])

with open('Resultaat loop 4.json') as f:
    data = json.load(f)

gemeenteNR = list(data.keys())

for gemeente in gemeenteNR:
   
    for identifier in data[gemeente].keys():
    
        if data[gemeente][identifier]['Soort']  ==  '(Gastouderopvang)':
            new_row = {'UniqueID':str(gemeente)+"-"+str(identifier),'GemeenteNr':str(gemeente),'Locatie':str(identifier),'Opvang_adres':data[gemeente][identifier]['Contactgegevens']['Opvangadres (locatie)']['Adres'],'Opvang_postcode':data[gemeente][identifier]['Contactgegevens']['Opvangadres (locatie)']['Postcode'],'Opvang_plaats':data[gemeente][identifier]['Contactgegevens']['Opvangadres (locatie)']['Plaats'],'Vestiging_adres':None,'Vestiging_postcode':None,'Vestiging_plaats':None,'Correspondentie_adres':None,'Correspondentie_postcode':None,'Correspondentie_plaats':None,'Contactpersoon':None,'E-mail':None,'Telefoon':None,'Website':None}
            df_contactgegevens = df_contactgegevens.append(new_row, ignore_index=True)
         
        if data[gemeente][identifier]['Soort'] in ('(Buitenschoolse opvang)','(Kinderdagverblijf)'):
            new_row = {'UniqueID':str(gemeente)+"-"+str(identifier),'GemeenteNr':str(gemeente),'Locatie':str(identifier),'Opvang_adres':data[gemeente][identifier]['Contactgegevens']['Opvangadres (locatie)']['Adres'],'Opvang_postcode':data[gemeente][identifier]['Contactgegevens']['Opvangadres (locatie)']['Postcode'],'Opvang_plaats':data[gemeente][identifier]['Contactgegevens']['Opvangadres (locatie)']['Plaats'],'Vestiging_adres':None,'Vestiging_postcode':None,'Vestiging_plaats':None,'Correspondentie_adres':data[gemeente][identifier]['Contactgegevens']['Correspondentieadres']['Adres'],'Correspondentie_postcode':data[gemeente][identifier]['Contactgegevens']['Correspondentieadres']['Postcode'],'Correspondentie_plaats':data[gemeente][identifier]['Contactgegevens']['Correspondentieadres']['Plaats'],'Contactpersoon':data[gemeente][identifier]['Contactgegevens']['Contactgegevens']['Contactpersoon'],'E-mail':data[gemeente][identifier]['Contactgegevens']['Contactgegevens']['E-mail'],'Telefoon':data[gemeente][identifier]['Contactgegevens']['Contactgegevens']['Telefoon'],'Website':data[gemeente][identifier]['Contactgegevens']['Contactgegevens']['Website']}                        
            df_contactgegevens = df_contactgegevens.append(new_row, ignore_index=True)
        
        if data[gemeente][identifier]['Soort']  ==  '(Gastouderbureau)':    
            new_row = {'UniqueID':str(gemeente)+"-"+str(identifier),'GemeenteNr':str(gemeente),'Locatie':str(identifier),'Opvang_adres':None,'Opvang_postcode':None,'Opvang_plaats':None,'Vestiging_adres':data[gemeente][identifier]['Contactgegevens']['Vestigingsadres']['Adres'],'Vestiging_postcode':data[gemeente][identifier]['Contactgegevens']['Vestigingsadres']['Postcode'],'Vestiging_plaats':data[gemeente][identifier]['Contactgegevens']['Vestigingsadres']['Plaats'],'Correspondentie_adres':data[gemeente][identifier]['Contactgegevens']['Correspondentieadres']['Adres'],'Correspondentie_postcode':data[gemeente][identifier]['Contactgegevens']['Correspondentieadres']['Postcode'],'Correspondentie_plaats':data[gemeente][identifier]['Contactgegevens']['Correspondentieadres']['Plaats'],'Contactpersoon':data[gemeente][identifier]['Contactgegevens']['Contactgegevens']['Contactpersoon'],'E-mail':data[gemeente][identifier]['Contactgegevens']['Contactgegevens']['E-mail'],'Telefoon':data[gemeente][identifier]['Contactgegevens']['Contactgegevens']['Telefoon'],'Website':data[gemeente][identifier]['Contactgegevens']['Contactgegevens']['Website']}  
            df_contactgegevens = df_contactgegevens.append(new_row, ignore_index=True)

        
export_csv = df_contactgegevens.to_csv (r'contactgegevens.csv', index = None, header=True, sep='\t') 

end = time.time()

Duur_loop3 = end - start
print("Loop 3: "+str(Duur_loop3))

########################################
#               Loop 4                 #
# Houdergegevens                       #
########################################
start = time.time()
df_houdergegevens = pd.DataFrame(columns = ['UniqueID','GemeenteNr', 'Locatie','Houder','Houder_vanaf','Geschillencommissie'])

with open('Resultaat loop 4.json') as f:
    data = json.load(f)

gemeenteNR = list(data.keys())

for gemeente in gemeenteNR:
   
    for identifier in data[gemeente].keys():
    
        if data[gemeente][identifier]['Soort'] in ('(Buitenschoolse opvang)','(Kinderdagverblijf)','(Gastouderbureau)'):
            new_row = {'UniqueID':str(gemeente)+"-"+str(identifier),'GemeenteNr':str(gemeente),'Locatie':str(identifier),'Houder':data[gemeente][identifier]['Houdergegevens']['Houder'],'Houder_vanaf':data[gemeente][identifier]['Houdergegevens']['Houder vanaf'],'Geschillencommissie':data[gemeente][identifier]['Houdergegevens']['Geschillencommissie']}
            df_houdergegevens = df_houdergegevens.append(new_row, ignore_index=True)
     
        
        if data[gemeente][identifier]['Soort']  ==  '(Gastouderopvang)':    
            new_row = {'UniqueID':str(gemeente)+"-"+str(identifier),'GemeenteNr':str(gemeente),'Locatie':str(identifier),'Houder':data[gemeente][identifier]['Houdergegevens']['Houder'],'Houder_vanaf':data[gemeente][identifier]['Houdergegevens']['Houder vanaf'],'Geschillencommissie':None}
            df_houdergegevens = df_houdergegevens.append(new_row, ignore_index=True)

        
export_csv = df_houdergegevens.to_csv (r'houdergegevens.csv', index = None, header=True, sep='\t') 

end = time.time()

Duur_loop4 = end - start
print("Loop 4: "+str(Duur_loop4))

########################################
#               Loop 5                 #
# Inspecties                           #
########################################
start = time.time()
df_inspecties = pd.DataFrame(columns = ['UniqueID','GemeenteNr', 'Locatie','InspectieID','UniqueInspectieID','Inspectie_link','Inspectie_datum'])

with open('Resultaat loop 4.json') as f:
    data = json.load(f)

gemeenteNR = list(data.keys())

for gemeente in gemeenteNR:

    for identifier in data[gemeente].keys():
        for k in range(len(data[gemeente][identifier]['Inspectie']['link'])):

            new_row = {'UniqueID':str(gemeente)+"-"+str(identifier),'GemeenteNr':str(gemeente),'Locatie':str(identifier),'InspectieID':k,'UniqueInspectieID':str(gemeente)+"-"+str(identifier)+"-"+str(k),'Inspectie_link':data[gemeente][identifier]['Inspectie']['link'][k],'Inspectie_datum':data[gemeente][identifier]['Inspectie']['datum'][k]}
            df_inspecties = df_inspecties.append(new_row, ignore_index=True)
            
export_csv = df_inspecties.to_csv (r'inspecties.csv', index = None, header=True, sep='\t')          

end = time.time()

Duur_loop5 = end - start
print("Loop 5: "+str(Duur_loop5))
  
########################################
#               Loop 6                 #
# Inspectierapporten                   #
########################################
start = time.time()
df_inspectierapporten = pd.DataFrame(columns = ['UniqueID','GemeenteNr', 'Locatie','InspectieID','UniqueInspectieID','GGD','Datum_inspectie','Datum_rapport','Soort_inspectieonderzoek','Link_Inspectierapport'])

with open('Resultaat loop 4.json') as f:
    data = json.load(f)

gemeenteNR = list(data.keys())

for gemeente in gemeenteNR:
    for identifier in data[gemeente].keys():
            for identifier2 in data[gemeente][identifier]['Inspectierapporten'].keys():
                print(str(gemeente)+"-"+str(identifier))
                if "Datum inspectie" in data[gemeente][identifier]['Inspectierapporten'][identifier2]['Inspectiegegevens']:
                    new_row = {'UniqueID':str(gemeente)+"-"+str(identifier),'GemeenteNr':str(gemeente),'Locatie':str(identifier),'InspectieID':str(identifier2),'UniqueInspectieID':str(gemeente)+"-"+str(identifier)+"-"+str(identifier2),'GGD':data[gemeente][identifier]['Inspectierapporten'][identifier2]['Inspectiegegevens']['GGD'],'Datum_inspectie':data[gemeente][identifier]['Inspectierapporten'][identifier2]['Inspectiegegevens']['Datum inspectie'],'Datum_rapport':data[gemeente][identifier]['Inspectierapporten'][identifier2]['Inspectiegegevens']['Datum rapport'],'Soort_inspectieonderzoek': data[gemeente][identifier]['Inspectierapporten'][identifier2]['Inspectiegegevens']['Soort inspectieonderzoek'], 'Link_Inspectierapport': data[gemeente][identifier]['Inspectierapporten'][identifier2]['Inspectiegegevens']['Inspectierapport']}
                    df_inspectierapporten = df_inspectierapporten.append(new_row, ignore_index=True)
                else:
                    new_row = {'UniqueID':str(gemeente)+"-"+str(identifier),'GemeenteNr':str(gemeente),'Locatie':str(identifier),'InspectieID':str(identifier2),'UniqueInspectieID':str(gemeente)+"-"+str(identifier)+"-"+str(identifier2),'GGD':data[gemeente][identifier]['Inspectierapporten'][identifier2]['Inspectiegegevens']['GGD'],'Datum_inspectie':None,'Datum_rapport':data[gemeente][identifier]['Inspectierapporten'][identifier2]['Inspectiegegevens']['Datum rapport'],'Soort_inspectieonderzoek': data[gemeente][identifier]['Inspectierapporten'][identifier2]['Inspectiegegevens']['Soort inspectieonderzoek'], 'Link_Inspectierapport': data[gemeente][identifier]['Inspectierapporten'][identifier2]['Inspectiegegevens']['Inspectierapport']}
                    df_inspectierapporten = df_inspectierapporten.append(new_row, ignore_index=True)
            
export_csv = df_inspectierapporten.to_csv (r'inspectierapporten.csv', index = None, header=True, sep='\t') 

end = time.time()

Duur_loop6 = end - start
print("Loop 6: "+str(Duur_loop6))

########################################
#               Loop 7                 #
# Uitkomsten                           #
########################################
start = time.time()
df_uitkomsten = pd.DataFrame(columns = ['UniqueID','GemeenteNr', 'Locatie','InspectieID','UniqueInspectieID','Criterium','Resultaat'])

with open('Resultaat loop 4.json') as f:
    data = json.load(f)

gemeenteNR = list(data.keys())


for gemeente in gemeenteNR:
    numgemeenten = len(data[gemeente].keys())
    for identifier in data[gemeente].keys():
            for identifier2 in data[gemeente][identifier]['Inspectierapporten'].keys():
                tmplist = data[gemeente][identifier]['Inspectierapporten'][identifier2].get('Uitkomsten')
                if tmplist is not None:
                    for indentifier3 in tmplist.keys():
                        new_row = {'UniqueID':str(gemeente)+"-"+str(identifier),'GemeenteNr':str(gemeente),'Locatie':str(identifier),'InspectieID':str(identifier2),'UniqueInspectieID':str(gemeente)+"-"+str(identifier)+"-"+str(identifier2),'Criterium':str(indentifier3),'Resultaat':data[gemeente][identifier]['Inspectierapporten'][identifier2]['Uitkomsten'][indentifier3]}
                        df_uitkomsten = df_uitkomsten.append(new_row, ignore_index=True)           
export_csv = df_uitkomsten.to_csv (r'uitkomsten.csv', index = None, header=True, sep='\t') 

end = time.time()

Duur_loop7 = end - start
print("Loop 7: "+str(Duur_loop7))

########################################
#               Loop 8                 #
# Beeld-Toezichthouder                 #
########################################
start = time.time()
df_beeldtoezichthouder = pd.DataFrame(columns = ['UniqueID','GemeenteNr', 'Locatie','InspectieID','UniqueInspectieID','Beeld-Toezichthouder'])

with open('Resultaat loop 4.json') as f:
    data = json.load(f)

gemeenteNR = list(data.keys())

for gemeente in gemeenteNR:
    for identifier in data[gemeente].keys():
            for identifier2 in data[gemeente][identifier]['Inspectierapporten'].keys():
                print(str(gemeente)+"-"+str(identifier))
                if "Beeld-Toezichthouder" in data[gemeente][identifier]['Inspectierapporten'][identifier2]: 
                    new_row = {'UniqueID':str(gemeente)+"-"+str(identifier),'GemeenteNr':str(gemeente),'Locatie':str(identifier),'InspectieID':str(identifier2),'UniqueInspectieID':str(gemeente)+"-"+str(identifier)+"-"+str(identifier2),'Beeld-Toezichthouder':data[gemeente][identifier]['Inspectierapporten'][identifier2]['Beeld-Toezichthouder']}
                    df_beeldtoezichthouder = df_beeldtoezichthouder.append(new_row, ignore_index=True)
                    
export_csv = df_beeldtoezichthouder.to_csv (r'beeldtoezichthouder.csv', index = None, header=True, sep='\t')

end = time.time()

Duur_loop8 = end - start
print("Loop 8: "+str(Duur_loop8))

########################################
#               Loop 9                 #
# Zienswijze-Houder                    #
########################################
start = time.time()
df_zienswijzehouder = pd.DataFrame(columns = ['UniqueID','GemeenteNr', 'Locatie','InspectieID','UniqueInspectieID','Zienswijze-Houder'])

with open('Resultaat loop 4.json') as f:
    data = json.load(f)

gemeenteNR = list(data.keys())

for gemeente in gemeenteNR:
    for identifier in data[gemeente].keys():
            for identifier2 in data[gemeente][identifier]['Inspectierapporten'].keys():
                print(str(gemeente)+"-"+str(identifier))
                if "Zienswijze-Houder" in data[gemeente][identifier]['Inspectierapporten'][identifier2]: 
                    new_row = {'UniqueID':str(gemeente)+"-"+str(identifier),'GemeenteNr':str(gemeente),'Locatie':str(identifier),'InspectieID':str(identifier2),'UniqueInspectieID':str(gemeente)+"-"+str(identifier)+"-"+str(identifier2),'Beeld-Toezichthouder':data[gemeente][identifier]['Inspectierapporten'][identifier2]['Zienswijze-Houder']}
                    df_zienswijzehouder = df_zienswijzehouder.append(new_row, ignore_index=True)
                    
export_csv = df_zienswijzehouder.to_csv (r'zienswijzehouder.csv', index = None, header=True, sep='\t')

end = time.time()

Duur_loop9 = end - start
print("Loop 9: "+str(Duur_loop9))

endrun = time.time()
Duur_run = endrun - startrun
print("Runtime: "+str(Duur_run))