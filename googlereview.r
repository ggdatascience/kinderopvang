##kinderopvang reviews koppelen via googleway package
#ChrisV/ChrisE, GGD Flevoland, mei 2019

library(tidyverse)
library(googleway)
library(curl)
library(readxl)
library(git2r)

#gebruik proxy settings via curl
#(ivm firewall issues)

curl_proxy <- function(url, verbose = TRUE){
  proxy <- ie_get_proxy_for_url(url)
  h <- new_handle(verbose = verbose, proxy = proxy)
  curl(url, handle = h)
}

#API-key
API_key <- ""

#inlezen data kinderopvang
fpo <- read_excel("//hvdf-san-01/Data/DataBureau X/3-PROGRAMMA INFORMATIE & INNOVATIE/Datavisualisatie/DATA/AGZ/Kinderdagopvang/stamtabel kinderopvang.xlsx")
#soort opvang afkortingen (BSO, KDV) van naam centrum afknippen
fpo$Naam <- substr(fpo$Centrum,5,stop = length(fpo$Centrum))

#kleine subset maken voor eventuele testen met minder data
fpo <- head(fpo,50)

#for loop bouwen via naam, adres en woonplaats.
adres <- NULL
res_place_id <- NULL
res_form_adr <- NULL
res_name <- NULL
res_pluscode <- NULL #toevoegen pluscode ivm url opbouwen.
res_rating <- NULL #toevoegen rating
res_user_ratings_total <- NULL #toevoegen rating aantal


#test run
#t = 5 #specificeer testrij
# test <- google_places(paste(fpo$Naam[t],fpo$Adres[t],fpo$Postcode[t],fpo$Woonplaats[t]),
#                             key = API_key,
#                             curl_proxy = "google.com",
#                             simplify = TRUE)

#for loop FPO#testloop
#for(i in 1:20) 
for(i in 1:nrow(fpo))
  {
  adres[[i]] <- google_places(search_string = paste(fpo$Naam[i],fpo$Adres[i],fpo$Postcode[i],fpo$Woonplaats[i]),
                              key = API_key,
                              curl_proxy = "google.com",
                              simplify = TRUE)
  


  #als er geen rating is op de google pagina dan neemt google die ook niet mee in de results
  #immers de api request geeft op dat punt niets terug. 
  #Daardoor loopt de for loop vast want googleway kan daar niet mee overweg. het aantal datapunten in in de frame is niet gelijk aan het totaal.
  #if(length(adres$results) <12) next
  #if(is.na(adres[[i]][["results"]][["reference"]]) next ){
# 
#     res_rating[[i]] next
#     res_user_ratings_total[[i]] next
#  }
  
  if(is.null(adres[[i]][["results"]][["reference"]])){

    res_place_id[[i]] <- "onbekend"
    res_form_adr[[i]] <- "onbekend"
    res_name[[i]] <- "onbekend"
    res_pluscode[[i]] <- "onbekend"
    res_rating[[i]] <- ""
    res_user_ratings_total[[i]] <- ""
  }
  
  else {
  
  res_place_id[[i]] <- adres[[i]][["results"]][["place_id"]]
  res_form_adr[[i]] <- adres[[i]][["results"]][["formatted_address"]]
  res_name[[i]] <- adres[[i]][["results"]][["name"]]
  res_pluscode[[i]] <- adres[[i]][["results"]][["plus_code"]]
  res_rating[[i]] <- adres[[i]][["results"]][["rating"]]
  res_user_ratings_total[[i]] <- adres[[i]][["results"]][["user_ratings_total"]]
    }}

fpo$place_ID <- res_place_id
fpo$google_name <- res_name
fpo$google_adress <- res_form_adr
fpo$google_plus_code <- res_pluscode
fpo$google_rating <- res_rating
fpo$google_user_ratings_total <- res_user_ratings_total

write.csv2(fpo,"kinderopvang_google_stamtabel_volledig.csv")
