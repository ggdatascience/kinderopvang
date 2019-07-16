#Script om reviewscore en aantal reviews van alle LRK open data op te halen via Google places API 
#Author: ChrisV/ChrisE

library(tidyverse)
library(googleway)
library(curl)
library(readxl)
library(git2r)
library(stringi) 

#gebruik proxy settings via curl
#(ivm firewall issues)

curl_proxy <- function(url, verbose = TRUE){
  proxy <- ie_get_proxy_for_url(url)
  h <- new_handle(verbose = verbose, proxy = proxy)
  curl(url, handle = h)
}

#API-key toevoegen
#file.edit("~/.Renviron")

#APIkey aanroepen
API_key <- Sys.getenv("VAR1")

#inlezen data kinderopvang
lrk_def <- read.csv2("//hvdf-san-01/Data/DataBureau X/3-PROGRAMMA INFORMATIE & INNOVATIE/Datavisualisatie/DATA/AGZ/Kinderdagopvang/export_opendata_lrk.csv")

#evt kleine subset maken voor eventuele testen met minder data
#lrk_def <- head(lrk_def,50)

#for loop bouwen via naam, adres en woonplaats.
adres <- NULL
res_lat <- NULL #latitude van google api
res_lon <- NULL #longitude van google api
res_place_id <- NULL #google placeID, nodig voor place_details
res_form_adr <- NULL #google adres
res_name <- NULL      #google naam vanuit places api
res_pluscode <- NULL #toevoegen pluscode ivm url opbouwen.
res_rating <- NULL #toevoegen rating
res_user_ratings_total <- NULL #toevoegen rating aantal

#Google friendly format 
lrk_def$googlesearchnaam <- stri_enc_toutf8(lrk_def$actuele_naam_oko)
lrk_def$googlesearchadres <- stri_enc_toutf8(lrk_def$opvanglocatie_adres)
lrk_def$googlesearchwoonplaats <- stri_enc_toutf8(lrk_def$opvanglocatie_woonplaats)

#test run
# test <- NULL
# t = 314 #specificeer testrij
# #zonder naam variabele werkt niet: lrk_def$actuele_naam_oko[t]
# 
# test <- google_places(search_string = paste(lrk_def$googlesearch[t],lrk_def$googlesearchadres[t],lrk_def$opvanglocatie_postcode[t],lrk_def$googlesearchwoonplaats[t]),
#                             key = API_key,
#                             curl_proxy = "google.com",
#                             simplify = TRUE)



#for loop Google places API aanroepen
#FPO#testloop
#for(i in 1:20) 

require(svMisc)

for(i in 1:nrow(lrk_def))
{ progress(i)
  adres[[i]] <- google_places(search_string = paste(lrk_def$googlesearch[i],lrk_def$googlesearchadres[i],lrk_def$opvanglocatie_postcode[i],lrk_def$googlesearchwoonplaats[i]),
                              key = API_key,
                              curl_proxy = "google.com",
                              simplify = TRUE)
  
  
  
  if(is.null(adres[[i]][["results"]][["reference"]])){
    
    res_lat[[i]] <- ""
    res_lon[[i]] <- ""
    res_place_id[[i]] <- ""
    res_form_adr[[i]] <- ""
    res_name[[i]] <- ""
    res_pluscode[[i]] <- ""
    res_rating[[i]] <- ""
    res_user_ratings_total[[i]] <- ""
  }
  #head gebruiken voor workaround als goole api meer dan 1 rij teruggeeft op een request
  else {
    res_lat[[i]] <- head(adres[[i]][["results"]][["geometry"]][["location"]][["lat"]], 1)
    res_lon[[i]] <- head(adres[[i]][["results"]][["geometry"]][["location"]][["lng"]], 1)
    res_place_id[[i]] <- head(adres[[i]][["results"]][["place_id"]], 1)
    res_form_adr[[i]] <- head(adres[[i]][["results"]][["formatted_address"]],1)
    res_name[[i]] <- head(adres[[i]][["results"]][["name"]],1)
    res_pluscode[[i]] <- head(ifelse(!is.null(adres[[i]][["results"]][["plus_code"]][["compound_code"]]), adres[[i]][["results"]][["plus_code"]][["compound_code"]], NA), 1)
    res_rating[[i]] <- head(ifelse(!is.null(adres[[i]][["results"]][["rating"]]), adres[[i]][["results"]][["rating"]], NA), 1)
    res_user_ratings_total[[i]] <- head(ifelse(!is.null(adres[[i]][["results"]][["user_ratings_total"]]), 
                                               adres[[i]][["results"]][["user_ratings_total"]], NA), 1)
    Sys.sleep(0.5) # time to not overload  the google API
  }}

lrk_def$google_lat <- res_lat
lrk_def$google_lon <-res_lat
lrk_def$google_place_ID <- res_place_id
lrk_def$google_name <- res_name
lrk_def$google_adress <- res_form_adr
lrk_def$google_plus_code <- res_pluscode
lrk_def$google_rating <- res_rating
lrk_def$google_user_ratings_total <- res_user_ratings_total

#mogelijk Verkeerde place_id achterhalen
library(data.table)
library(caret)
library(e1071)
dt_verkeerd <- NULL

#mogelijk Verkeerde place_id achterhalen: optie 1 tekstmatch test
dt_verkeerd <- data.table(tolower(lrk_def$actuele_naam_oko), tolower(lrk_def$google_name)) 
dt_verkeerd[, test := grepl(V1, V2), by = V1]

#mogelijk Verkeerde place_id achterhalen: optie 2 fuzzytekst test
dt_verkeerd$fuzzytest <- NULL
dt_verkeerd[, fuzzytest := agrepl(V1, V2, max.distance = 0.2), by = V1] #max.distance = 0.2, value = FALSE
warnings(agrepl)

#optie 1 en 2 vergelijken
confusionMatrix(as.factor(dt_verkeerd$test), as.factor(dt_verkeerd$fuzzytest)) #de fuzzytest is nauwkeuriger zoals verwacht

dt_verkeerd_test <- subset(dt_verkeerd, dt_verkeerd$test != dt_verkeerd$fuzzytest)
View(dt_verkeerd_test, "check naam matches opties")

lrk_def$match_naam_google <- dt_verkeerd$fuzzytest

write.csv2(dt_verkeerd,"testset_tekstmining_google_placeID.csv")
write.csv2(lrk_def,"lrk_def_googlereview.csv")

#TO DO: 
# error gogle api indien niet utf8 characters in search string zoals "Sórensen" line 36
#"error_message" : "Invalid request. One of the input parameters contains a non-UTF-8 string."
#als fuzzytest is FALSE dan opnieuw google api doorlopen? andere opties?















#reviews ophalen uit google places detaillijst, nu even on hold want probleem: max 5 reviews
# detail <- NULL
# rat_df <- NULL
# rat_dfAll <- NULL
# 
# res_place_id_noNulls <- subset(res_place_id,res_place_id!="")
# 
# #detail lijst
# for(i in 1:length(res_place_id_noNulls)){
#   
#   detail[[i]] <- google_place_details(res_place_id_noNulls[i],
#                                       key = API_key,
#                                       curl_proxy = "google.com",
#                                       simplify = TRUE)
#   
#   if(is.null(detail[[i]][["result"]][["reviews"]])){
#     print("onbekend")  }
#     
#   else {
#   
#   rat_df[[i]] <- detail[[i]][["result"]][["reviews"]]
#   rat_df[[i]]$place_id <- detail[[i]][["result"]][["reference"]]
#   
#   rat_dfAll <- bind_rows(rat_dfAll,rat_df)
#    }}
# 
# 
# write.csv2(rat_dfAll,"kinderopvang_google_reviews_volledig.csv")

#commit(repo = "kinderopvang", message = NULL, all = FALSE, session = FALSE,
#        author = CVCE, committer = graskaas2014)