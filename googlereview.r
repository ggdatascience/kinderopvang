##kinderopvang reviews koppelen via googleway package
#ChrisV/ChrisE, GGD Flevoland, mei 2019

library(tidyverse)
library(googleway)
library(curl)
library(readxl)
library(git2r)
library(jsonlite)
library(secret)

#secrets file aanmaken voor api key, nog niet helemaal gelukt
Sys.chmod("secret.file", mode = "0400")

my_secrets <- function() {
  path <- "C:/Users/chrise/secrets/secret.json"
  if (!file.exists(path)) {
    stop("Can't find secret file: '", path, "'")
  }
  
  jsonlite::read_json(path)
}


#gebruik proxy settings via curl
#(ivm firewall issues)

curl_proxy <- function(url, verbose = TRUE){
  proxy <- ie_get_proxy_for_url(url)
  h <- new_handle(verbose = verbose, proxy = proxy)
  curl(url, handle = h)
}

#API-key
API_key <- Sys.getenv("API_key")

#inlezen data kinderopvang
fpo <- read_excel("//hvdf-san-01/Data/DataBureau X/3-PROGRAMMA INFORMATIE & INNOVATIE/Datavisualisatie/DATA/AGZ/Kinderdagopvang/stamtabel kinderopvang.xlsx")
#soort opvang afkortingen (BSO, KDV) van naam centrum afknippen
fpo$Naam <- substr(fpo$Centrum,5,stop = length(fpo$Centrum))

#kleine subset maken voor eventuele testen met minder data
#fpo <- head(fpo,50)

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
  #Sys.sleep(0.5) # time to not overload  the google API
    }}

fpo$google_lat <- res_lat
fpo$google_lon <-res_lat
fpo$google_place_ID <- res_place_id
fpo$google_name <- res_name
fpo$google_adress <- res_form_adr
fpo$google_plus_code <- res_pluscode
fpo$google_rating <- res_rating
fpo$google_user_ratings_total <- res_user_ratings_total

#mogelijk Verkeerde place_id achterhalen: optie 1
library(data.table)
library(caret)
library(e1071)
dt_verkeerd <- data.table(tolower(fpo$Naam), tolower(fpo$google_name)) 
dt_verkeerd[, test := grepl(V1, V2), by = V1]


#mogelijk Verkeerde place_id achterhalen: optie 2
dt_verkeerd$fuzzytest <- NULL
dt_verkeerd[, fuzzytest := agrepl(V1, V2, max.distance = 0.2), by = V1] #max.distance = 0.2, value = FALSE
warnings(agrepl)

#optie 1 en 2 vergelijken
confusionMatrix(as.factor(dt_verkeerd$test), as.factor(dt_verkeerd$fuzzytest)) #de fuzzytest is nauwkeuriger zoals verwacht

dt_verkeerd_test <- subset(dt_verkeerd, dt_verkeerd$test != dt_verkeerd$fuzzytest)
View(dt_verkeerd_test, "check naam matches opties")

fpo$match_naam <- dt_verkeerd$fuzzytest

#TO DO: 
#google variabelen leegmaken voor fuzzytest=false
#als fuzzytest is FALSE dan opnieuw google api doorlopen?




write.csv2(dt_verkeerd,"testset_tekstmining_google_placeID.csv")
write.csv2(fpo,"kinderopvang_google_stamtabel_volledig_review_gecleaned.csv")










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

#git nog instellen, hoe api keys verbergen??
#commit(repo = ".", message = NULL, all = FALSE, session = FALSE,
#        author = CVCE, committer = graskaas2014)