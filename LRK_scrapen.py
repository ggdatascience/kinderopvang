# -*- coding: utf-8 -*-
"""
Created on Fri May 10 21:11:24 2019

@author: j.ten.velden
"""

from bs4 import BeautifulSoup
import requests
import re
import time 
import random
import json
import math
import os

# Pas current directory aan
os.chdir('G:/Kinderopvang scrapen/')
cd = os.getcwd()

# Bestandsnamen
resultaat_loop_1 = cd + "\\" + "Resultaat loop 1.json"
resultaat_loop_2 = cd + "\\" + "Resultaat loop 2.json"
resultaat_loop_3 = cd + "\\" + "Resultaat loop 3.json"

####################
# Pick your region #
####################

# Landelijk, zoals uit het landelijk register kinderopvang
gemeenteNR = [518, 796, 1680, 358, 197, 59, 482, 613, 361, 141, 34, 484, 1723, 1959, 60, 307, 362, 363, 200, 3, 202, 106, 743, 744, 308, 489, 203, 888, 1954, 370, 889, 1945, 1724, 893, 373, 748, 1859, 1721, 753, 209, 375, 1728, 376, 377, 1901, 755, 1681, 147, 654, 756, 757, 758, 501, 1876, 213, 899, 312, 313, 214, 502, 383, 109, 1706, 1684, 216, 148, 1891, 310, 1940, 736, 1690, 503, 10, 400, 762, 150, 384, 1774, 221, 222, 766, 505, 498, 1719, 303, 225, 226, 1711, 385, 228, 317, 770, 1903, 772, 230, 114, 388, 153, 232, 233, 777, 779, 1771, 1652, 907, 784, 1924, 664, 785, 1942, 512, 513, 786, 14, 1729, 158, 788, 392, 394, 1655, 160, 243, 523, 72, 244, 396, 397, 246, 74, 398, 917, 1658, 399, 163, 530, 794, 531, 164, 1966, 252, 797, 534, 798, 402, 1963, 1735, 1911, 118, 405, 1507, 321, 406, 677, 353, 1884, 166, 678, 537, 928, 1598, 542, 1931, 1659, 1685, 882, 415, 416, 1621, 417, 80, 546, 547, 1916, 995, 1640, 327, 1705, 553, 262, 809, 331, 24, 168, 263, 1641, 556, 935, 420, 938, 1948, 119, 687, 1842, 1731, 1952, 815, 1709, 1978, 1955, 335, 944, 1740, 946, 356, 569, 267, 268, 1930, 1970, 1695, 1699, 171, 575, 820, 302, 579, 823, 824, 1895, 269, 173, 1773, 175, 1586, 826, 85, 431, 432, 86, 828, 1509, 437, 589, 1734, 590, 1894, 765, 1926, 439, 273, 177, 703, 274, 339, 1667, 275, 340, 597, 1742, 603, 1669, 957, 1674, 599, 277, 840, 441, 279, 606, 88, 1676, 965, 1702, 845, 1883, 610, 1714, 90, 342, 847, 848, 37, 180, 532, 851, 1708, 971, 1904, 1900, 715, 93, 448, 1525, 716, 281, 855, 183, 1700, 1730, 737, 856, 450, 451, 184, 344, 1581, 981, 994, 858, 47, 345, 717, 861, 453, 983, 984, 1961, 622, 96, 718, 986, 626, 285, 865, 1949, 866, 867, 627, 289, 629, 852, 988, 457, 1960, 668, 1969, 1701, 293, 1950, 1783, 98, 614, 189, 296, 1696, 352, 294, 873, 632, 880, 351, 479, 297, 473, 50, 355, 299, 637, 638, 1892, 879, 301, 1896, 642, 193 ]

## Per GGD, met de CBS codes die in het landelijk register kinderopvang staan 

# Amsterdam
# gemeenteNR = [358, 362, 363, 384, 437, 451]
# Brabant Zuidoost
# gemeenteNR = [743, 753, 762, 770, 772, 794, 820, 823, 847, 848, 858, 861, 866, 1652, 1658, 1659, 1667, 1706, 1724, 1728, 1771]
# Drenthe
# gemeenteNR = [106, 109, 114 ,118, 119, 1680, 1681, 1690, 1699, 1701, 1730, 1731]
# Flevoland
# gemeenteNR = [34, 50, 171, 184, 303, 995]
# Fryslan
# gemeenteNR = [59, 60, 72, 74, 80, 85, 86, 88, 90, 93, 96, 98, 737, 1891, 1900, 1940, 1970, 1949]
# Gelderland-Midden
# gemeenteNR = [202, 203, 221, 226, 228, 267, 274, 275, 277, 279, 289, 293, 299, 1705, 1734]
# Gelderland-Zuid
# gemeenteNR = [209, 214, 216, 225, 252, 263, 268, 281, 296, 297, 668, 1740, 1945, 1960]
# Gooi en Vechtstreek
# gemeenteNR = [376, 402 ,406, 417, 457, 1696, 1942]
# Groningen
# gemeenteNR = [3, 10, 14, 24, 37, 47, 765, 1895, 1952, 1966, 1969, 1950]
# Haaglanden
# gemeenteNR = [503, 518, 603, 629, 637, 1783, 1842, 1916, 1926]
# Hart voor Brabant
# gemeenteNR = [796, 1721, 755, 756, 757, 1684, 766, 784, 785, 786, 788, 797, 798, 1685, 809, 1948, 815, 824, 828, 1702, 845, 855, 856, 865, 867]
# Hollands-Midden
# gemeenteNR = [484, 513, 534, 537, 546, 547, 553, 569, 575, 579, 626, 627, 638, 1525, 1884, 1892, 1901, 1931]
# Hollands Noorden
# gemeenteNR = [361, 373, 383, 388, 398, 399, 400, 405, 416, 420, 432, 441, 448, 498, 532, 1598, 1911]
# IJsselland
# gemeenteNR = [148, 150, 160, 166, 175, 177, 180, 193, 1708, 1773, 1896]
# Kennemerland
# gemeenteNR = [375, 377, 392, 394, 396, 397, 450, 453, 473]
# Limburg-Noord
# gemeenteNR = [889, 893, 907, 944, 946, 957, 983, 984, 988, 1507, 1640, 1641, 1669, 1711, 1894]
# Noord- en Oost-Gelderland
# gemeenteNR = [197, 200, 213, 222, 230, 232, 233, 243, 244, 246, 262, 269, 273, 285, 294, 301, 302, 1509, 1586, 1859, 1876, 1955]
# Regio Utrecht
# gemeenteNR = [307, 308, 310, 312, 313, 317, 321, 327, 331, 335, 339, 340, 342, 344, 345, 351, 352, 353, 355, 356, 589, 632, 736, 1581, 1904, 1961]
# Rotterdam-Rijnmond
# gemeenteNR = [489, 501, 502, 530, 542, 556, 597, 599, 606, 613, 614, 622, 1621, 1924, 1930]
# Twente
# gemeenteNR = [141, 147, 153, 158, 163, 164, 168, 173, 183, 189, 1700, 1735, 1742, 1774]
# West Brabant
# gemeenteNR = [744, 748, 758, 777, 779, 826, 840, 851, 873, 879, 1655, 1674, 1709, 1719, 1723, 1959]
# Zaanstreek-Waterland
# gemeenteNR = [370, 385, 415, 431, 439, 479, 852, 880]
# Zeeland
# gemeenteNR = [654, 664, 677, 678, 687, 703, 715, 716, 717, 718, 1676, 1695, 1714]
# Zuid-Limburg
# gemeenteNR = [882, 888, 899, 917, 928, 935, 938, 965, 971, 981, 986, 994, 1729, 1883, 1903, 1954]
# Zuid-Holland Zuid
# gemeenteNR = [482, 505, 512, 523, 531, 590, 610, 642, 1963, 1978]



####################################
#              Loop 1              #
# Scrape pagina met zoekresultaten #
####################################


# Maak een lege dictionary aan, om data in op te slaan
Kinderopvang = {}

# Loop over gemeenten

start = time.time()

for gemeente in gemeenteNR:
    
    # initialiseer data-opslag en ID
    Kinderopvang[gemeente] = {}
    identifier = 0
    
    url = 'http://www.landelijkregisterkinderopvang.nl/pp/zoeken/AlleOkoTypenZoekResultaten.jsf?currentPage=0&verantwoordelijkeGemeente=' + str(gemeente) + '&zoekHistorischeNaam=false&zoekStatusSoort=Ingeschreven'
    
    # Open url met request package
    r = requests.get(url)
    
    # Turn into soup (databestand waar de BeautifulSoup package mee kan werken)
    soup = BeautifulSoup(r.text)
    
    # Zoek in soup de div met class "sort-data"
    temp = soup.find('div',{"class": "sort-data"})
    # Neem de text van die div (temp.text), strip hem van white space, split hem op spaties en neem dan de laatste waarde uit de lijst die ontstaat. Cast dit stukje tekst om naar een integer. Dit is het aantal pagina's.
    max_pages = math.ceil(int(temp.text.strip().split()[-1]) / 15)
    # max_pages = 2 # voor testen
     
    # Loop over aantal pagina's dat gemeente heeft
    for j in range(int(max_pages)): 
        
        # Open pagina j van gemeente i
        url2 ='https://www.landelijkregisterkinderopvang.nl/pp/zoeken/AlleOkoTypenZoekResultaten.jsf?currentPage='+ str(j) + '&verantwoordelijkeGemeente=' + str(gemeente) + '&zoekHistorischeNaam=false&zoekStatusSoort=Ingeschreven'
        r2 = requests.get(url2)
        soup2 = BeautifulSoup(r2.text)
        
        resultaten = soup2.findAll('li',{"class": "aankeiler"})
        
        # Loop over het aantal kinderopvangen op de pagina
        for k in range(len(resultaten)):
            
            print("Loop 1, CBS code: " + gemeente + ", kinderopvang " + identifier)
            
            # Maak entry aan in dictionary
            Kinderopvang[gemeente][identifier] = {}
            
            # Naam van de opvang
            Kinderopvang[gemeente][identifier]["Naam"] = resultaten[k].find('h2').find('a').text.strip()
            
            # Link naar de pagina van de opvang
            Kinderopvang[gemeente][identifier]["Link"] = resultaten[k].find('h2').find('a')['href']
            
            # Soort opvang (kinderdagverblijf, gastouder, etc)
            Kinderopvang[gemeente][identifier]["Soort"] = resultaten[k].find('h2').find('a').next.next.strip() 
            
            # Adres
            adres = resultaten[k].find('span',{"id": re.compile("ToonAdres")}).text.replace(u'\xa0', u' ').replace(u'\n',u'')
            Kinderopvang[gemeente][identifier]["Adres"] = re.sub(' +', ' ',adres) # Verwijder duplicate spaces
            
            # Postcode en woonplaats
            postcode_wpl = resultaten[k].find('span',{"id": re.compile("ToonPostcodeWoonplaats")}).text.replace(u'\xa0', u' ').replace(u'\n',u'')
            Kinderopvang[gemeente][identifier]["Pc_Wpl"] = re.sub(' +', ' ',postcode_wpl) # Verwijder duplicate spaces
            
            # Info die niet bij elke opvang is ingevuld
            #initialisatie om vorig resultaat weg te laten en later wel te kunnen checken of ie in deze ronde gevonden is.
            extra_info = []
            extra_info = resultaten[k].findAll('p', {"class": "resultaat-excerpt"})
                
            if len(extra_info) > 0: 
                for m in range(len(extra_info)-1):
                    if re.search('Houder/eigenaar:', extra_info[m].text):
                        Kinderopvang[gemeente][identifier]["Houder_link"] = extra_info[m].find('a')['href']
                        Kinderopvang[gemeente][identifier]["Houder_naam"] = extra_info[m].find('a').text.strip()
                    if re.search('Huidige status:', extra_info[m].text):
                        Kinderopvang[gemeente][identifier]["Status"] = extra_info[m].text.strip()
                    if re.search('Voorschoolse educatie', extra_info[m].text):
                        Kinderopvang[gemeente][identifier]["Voorsch_Educ"] = extra_info[m].text.strip()
            
            # Hoog id op met 1
            identifier += 1

        datadump = json.dumps(Kinderopvang)
        f = open("Resultaat loop 1.json", "w")
        f.write(datadump)
        f.close()

        # Random aantal seconden wachten (tussen 1 en 3 sec) om de server niet boos te maken
        time.sleep(random.randint(1,3))
        
        
end = time.time()

Duur_loop1 = end - start
print(Duur_loop1)

##############################################
#                  Loop 2                    #
# Scrape pagina van individuele kinderopvang #
##############################################

# Open opgeslagen json bestand
with open("Resultaat loop 1.json", 'r') as f:
        Kinderopvang = json.load(f)
        
# Haal de gemeentenummers uit de dictionary
gemeenteNR = list(Kinderopvang.keys())

# Lijst beperken
# gemeenteNR = ['845', '855', '856', '865', '867']

start = time.time()

for gemeente in gemeenteNR:
    
    for identifier in Kinderopvang[gemeente].keys(): # De identifiers in Kinderopvang worden vanaf 0 opgehoogd met 1, dus kan makkelijk over een vast deel loopen (aangezien dictionaries eigenlijk ongeordend zijn)
        
        print("Loop 2, CBS code: " + gemeente + ", kinderopvang " + identifier)
        
        url3 = 'https://www.landelijkregisterkinderopvang.nl'+ Kinderopvang[gemeente][identifier]["Link"]
        
        # Url voor testdoeleinden gehardcode.     
        # url3 = 'https://www.landelijkregisterkinderopvang.nl/pp/inzien/Oko/Kdv/GegevensOKO.jsf?selectedResultId=85158'
        # Met handhavingsbesluit
        # url3 = 'https://www.landelijkregisterkinderopvang.nl/pp/inzien/Oko/Kdv/GegevensOKO.jsf?selectedResultId=85194'
        
        r3 = requests.get(url3)
        soup3 = BeautifulSoup(r3.text)
        
        ##
        ## Kerngegevens
        ##
        
        # Zoek html brok met kerngegevens
        kerngegevens = soup3.find('h2', {"class": "subtitle marge-cap"}).next.next.next
        
        # Zoek naar html brok in linkerkolom en html brok in rechterkolom
        kerngegevens_rechts = kerngegevens.findAll('div',{"class": "row-right"})
        kerngegevens_links = kerngegevens.findAll('div',{"class": "row-left"})
        
        # Initialiseer arrays om data tijdelijk op te slaan
        rechts = []
        links = []
        
        # Lees html brokken uit en voeg toe aan hierboven geinitialiseerde arrays
        for element in kerngegevens_rechts:
            rechts.append(element.text.strip())
            
        for element in kerngegevens_links:
            links.append(element.text.strip())    
        
        # Initialiseer entry in dictionary om data in op te slaan
        Kinderopvang[gemeente][identifier]['Kerngegevens'] = {}
        
        # Sla data op in dictionary
        if len(rechts) == len(links):
            for i in range(len(rechts)):
                Kinderopvang[gemeente][identifier]['Kerngegevens'][links[i]] = rechts[i]
        
        ##
        ## Contactgegevens
        ##
        
        # Zoek html brok met contactgegevens
        blok2 = soup3.find('div', {"class": "table-blok marge-top2"})
        
        
        blok2_data = blok2.findAll('div', {'class': 'table-set'}) # voor de html per blok
        blok2_titel = blok2.findAll('h2', {'class': 'subtitle'}) # voor de titel van het blok
        
        # Initialiseer entry in dictionary om data in op te slaan
        Kinderopvang[gemeente][identifier]['Contactgegevens'] = {}
        
        # Initialiseer blokken voor de aanwezige contactinfo (minimaal 1, maximaal 3)
        for i in range(len(blok2_titel)):
            Kinderopvang[gemeente][identifier]['Contactgegevens'][blok2_titel[i].text] = {}
            
            links2 = blok2_data[i].findAll('div',{"class": "row-left"})
            rechts2 = blok2_data[i].findAll('div',{"class": "row-right"})
            
            for j in range(len(links2)):
                Kinderopvang[gemeente][identifier]['Contactgegevens'][blok2_titel[i].text][links2[j].text.strip().replace(u'\xa0', u' ')] = rechts2[j].text.strip().replace(u'\xa0', u' ')
                if rechts2[j].text.strip().replace(u'\xa0', u' ') == "Link naar website":
                    Kinderopvang[gemeente][identifier]['Contactgegevens'][blok2_titel[i].text][links2[j].text.strip().replace(u'\xa0', u' ')] = rechts2[j].find('a')['href']
        
        
        
        ##
        ## Houdergegevens
        ##
        
        data_soup = soup3.find('div', {"id": "inhoud-kolom"})
        data_soepje = data_soup.findAll('div', {'class': 'table-blok'})
        houdergegevens = data_soepje[-1]
        
        houder_links = houdergegevens.findAll('div',{"class": "row-left"})
        houder_rechts = houdergegevens.findAll('div',{"class": "row-right"})
        
        # Initialiseer entry in dictionary om data in op te slaan
        Kinderopvang[gemeente][identifier]['Houdergegevens'] = {}
        
        for i in range(len(houder_links)):
             Kinderopvang[gemeente][identifier]['Houdergegevens'][houder_links[i].text.strip().replace(u'\xa0', u' ')] = houder_rechts[i].text.strip().replace(u'\xa0', u' ')
             
        ##
        ## Inspectierapporten
        ##
        
        inspectie = soup3.findAll('a',{"title": "Inspectie-overzicht"})      
        
        link = []
        datum = []
        
        for element in inspectie:
            datum.append(element.text.strip())
            link.append(element['href'])
            
        Kinderopvang[gemeente][identifier]['Inspectie'] = {}
        
        Kinderopvang[gemeente][identifier]['Inspectie']['link'] = link
        Kinderopvang[gemeente][identifier]['Inspectie']['datum'] = datum
        

        ##
        ## Handhavingsbesluit
        ##
        
        temp = [] 
        temp = soup3.findAll('a',{"title": "Handhavingsbesluiten"})
        
        if len(temp) > 0:
            handhaving = temp[0]['href'] 
            Kinderopvang[gemeente][identifier]['Handhaving'] = handhaving
            
        datadump = json.dumps(Kinderopvang)
        f = open("Resultaat loop 2.json", "w")
        f.write(datadump)
        f.close()
        
        # Random aantal seconden wachten (tussen 1 en 3 sec) om de server niet boos te maken
        time.sleep(random.randint(1,3))
        
end = time.time()

Duur_loop2 = end - start
print(Duur_loop2)


########################################
#               Loop 3                 #
# Scrape pagina van inspectierapporten #
########################################

with open("Resultaat loop 2.json", 'r') as f:
        Kinderopvang = json.load(f)

# Haal de gemeentenummers uit de dictionary
gemeenteNR = list(Kinderopvang.keys())

# Lijst beperken
# gemeenteNR = ['1721', '855', '856', '865', '867']

# Functie om resultaten-kleurtjes uit te lezen (Pythons switch/case equivalent)
def kleur_naar_oordeel(argument):
    switcher = {
        "background-color: #216692": "in orde",
        "background-color: #B9D8EA": "niet in orde",
        "background-color: #FDCE66": "niet beoordeeld",
    }
    return switcher.get(argument, "error")

start = time.time()

for gemeente in gemeenteNR:
    
    for identifier in Kinderopvang[gemeente].keys(): # De identifiers in Kinderopvang worden vanaf 0 opgehoogd met 1, dus kan makkelijk over een vast deel loopen (aangezien dictionaries eigenlijk ongeordend zijn)
        
        Kinderopvang[gemeente][identifier]['Inspectierapporten'] = {}
        
        for k in range(len(Kinderopvang[gemeente][identifier]['Inspectie']['link'])):
            
            print("Loop 3, CBS code: " + gemeente + ", kinderopvang " + identifier + ", inspectierapport " + k)
        
            # url4 = 'https://www.landelijkregisterkinderopvang.nl/pp/inzien/Oko/InspectieRapport.jsf?selectedResultId=183627&documentId=0'
            url4 = 'https://www.landelijkregisterkinderopvang.nl'+ Kinderopvang[gemeente][identifier]['Inspectie']['link'][k]
            
            r4 = requests.get(url4)
            soup4 = BeautifulSoup(r4.text)
            
            gegevens_inspectie = soup4.find('div', {"class": "table-blok marge-top"})
            
            # Inspectiegegevens
            
            inspectie_links = gegevens_inspectie.findAll('div',{"class": "row-left"})
            inspectie_rechts = gegevens_inspectie.findAll('div',{"class": "row-right"})
            
            # Initialiseer arrays om data tijdelijk op te slaan
            rechts = []
            links = []
            
            # Lees html brokken uit en voeg toe aan hierboven geinitialiseerde arrays
            for i in range(len(inspectie_links)):
                links.append(inspectie_links[i].text.strip().replace(u'\n', u'')) 
                
                if inspectie_links[i].text.strip().replace(u'\n', u'') != "Inspectierapport":
                    rechts.append(inspectie_rechts[i].text.strip().replace(u'\n', u''))
                else:
                    rechts.append(inspectie_rechts[i].find('a')['href'])
            
            # Initialiseer entry in dictionary om data in op te slaan
            Kinderopvang[gemeente][identifier]['Inspectierapporten']['Inspectiegegevens'] = {}
            
            # Sla data op in dictionary
            if len(rechts) == len(links):
                for i in range(len(rechts)):
                    Kinderopvang[gemeente][identifier]['Inspectierapporten']['Inspectiegegevens'][links[i]] = rechts[i]
            
            
            # Uitkomsten van de inspectie
            
            # Alleen doen als ingevuld op pagina
            indicatoren = []

            indicatoren = soup4.findAll("div", {"class": "category-cell"})
            
            if len(indicatoren) > 0:      
                Kinderopvang[gemeente][identifier]['Inspectierapporten']['Uitkomsten'] = {}
                
                for i in range(len(indicatoren)):
                    Kinderopvang[gemeente][identifier]['Inspectierapporten']['Uitkomsten'][indicatoren[i]["title"]] = kleur_naar_oordeel(indicatoren[i]["style"]);
    
                # Algemeen beeld van de opvang door de toezichthouder    
                beeld_toezichthouder = soup4.find('div', {'id': 'i_beschouwing'})
                Kinderopvang[gemeente][identifier]['Inspectierapporten']["Beeld-Toezichthouder"] = beeld_toezichthouder.text
                
                # Zienswijze van de houder
                zienswijze_houder = soup4.find('div', {'id': 'i_InspectieRapportDetails:i_zienswijze:i_data_section'})
                Kinderopvang[gemeente][identifier]['Inspectierapporten']["Zienswijze-Houder"] = zienswijze_houder.text.strip()
                
            datadump = json.dumps(Kinderopvang)
            f = open("Resultaat loop 3.json", "w")
            f.write(datadump)
            f.close()
            
            # Random aantal seconden wachten (tussen 1 en 3 sec) om de server niet boos te maken
            time.sleep(random.randint(1,3))

end = time.time()

Duur_loop3 = end - start
print(Duur_loop3)                 

        
        
