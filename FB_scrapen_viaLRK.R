#https://www.datacamp.com/community/tutorials/r-web-scraping-rvest

options(stringsAsFactors = FALSE)

# General-purpose data wrangling
require(tidyverse)  

# Parsing of HTML/XML files  
require(rvest)    

# String manipulation
require(stringr)   

# Verbose regular expressions
require(rebus)     

# Eases DateTime manipulation
require(lubridate)
# tekst matching
library(data.table)
library(caret)
library(e1071)

#gebruik proxy settings via curl (ivm firewall issues))
curl_proxy <- function(url, verbose = TRUE){
  proxy <- ie_get_proxy_for_url(url)
  h <- new_handle(verbose = verbose, proxy = proxy)
  curl(url, handle = h)
}

#inlezen data kinderopvang, excl gastouders (zie google drive voor bestand)
#datascrape <- read.csv2("<vulje bestandlocatie in")
datascrape <- filter(export_opendata_lrk, type_oko != 'VGO')


#URL friendly format (UTF-8) 
#url <- str_conv(datascrape$contact_website, "UTF-8")
url <- as.data.frame(as.character(datascrape$contact_website))
names(url)[1] <- 'v1'
#test met 100
url <- head(url,100)


# Afzonderlijke pagina's scrapen
# url facebook ophalen
get_url <- function(url){
  html <- read_html(url)
  FBurl <- html %>% html_nodes("a") %>% html_attr("href") 
  #unlist()                    
  # Alleen de facebook link opslaan
  FBtable <- data.table(FBurl)
  FBtable[, test := grepl("facebook.com", FBurl), by = FBurl]
  FBtable <- subset(FBtable, test == TRUE, FBurl)
  FBlink <- head(FBtable, 1)
  return(FBlink)
  
} # 

df.fb <- data.frame(id = integer(), url= character(), fburl = character())

for (i in 1:nrow(url)){
  
  if (url$v1[i] == '' ){
    
    #df.fb[i, 1] <- id # nog ergens ophalen en wegschrijven
    df.fb[i, 2] <- url$v1[i]
    df.fb[i, 3] <- 'geen fb link'
    
  } else {
    
  df.fb[i, 2] <- url$v1[i]
  df.fb[i, 3] <- get_url(url$v1[i]) #try catch inbouwen, gaat fout in de functie
  
  }
}

results <- NULL

   
}
