#Verkrijgen facebooklinks adv open LRK dataset
#author: Chris Elschot & Jeroen ter Voert
#Laatste update oktober 2019

#factors omzetten naar strings
options(stringsAsFactors = FALSE)

#evt vereiste packages laden met pacman
#if (!require("pacman")) install.packages("pacman")
#pacman::p_load("curl", "tidyverse", "rvest", "data.table", "Rcrawler")
library(curl)
library(rvest)
library(data.table)
library(Rcrawler)

#data ophalen via https://data.overheid.nl/dataset/gegevens-kinderopvanglocaties-lrk
#ophalen en inlezen data kinderopvang
df.lrk <- read.csv2("http://www.landelijkregisterkinderopvang.nl/opendata/export_opendata_lrk.csv")
#gastouders eruit
df.lrk <- df.lrk[df.lrk$type_oko != "VGO", ]
#geen website naar NA
df.lrk$contact_website[which(df.lrk$contact_website == "")] <- NA

#gebruik evt proxy settings via curl (ivm firewall issues, met name op remotes))
curl_proxy <- function(url, verbose = TRUE){
 proxy <- ie_get_proxy_for_url(url)
 h <- new_handle(verbose = verbose, proxy = proxy)
 curl(url, handle = h)
}

#functie die op contact_website zoekt naar facebook websites met Rcrawler
get_FBurl <- function(url){
  if (is.na(url)){
    return(list(homepage = url, facebookpagina = NA)) #testen of input NA is, zoja return NA
  }
  try(rcrawl<- LinkExtractor(url, ExternalLInks = TRUE, Useragent = "Chrome/41.0.2228.0")) ## #Inlezen html van de webpagina
  options(show.error.messages = TRUE) 
  if (rcrawl$Info['Status_code'] != '404'){ 
    FBurl <- head(unique(rcrawl$ExternalLinks[which(grepl('facebook', rcrawl$ExternalLinks))]),1) #Alleen de unieke adressen met "facebook.com" erin en daar de eerste van
    if (length(FBurl) > 0){
      return(list(homepage = url, facebookpagina = FBurl)) #kan meerdere waarden bevatten dus returnen als list
    }
  }
  if(rcrawl$Info['Status_code'] == '404'){
    url<-gsub("http", "https",url)
    try(rcrawl<- LinkExtractor(url, ExternalLInks = TRUE, Useragent = "Chrome/41.0.2228.0")) ## #Inlezen html van de webpagina
    if (rcrawl$Info['Status_code'] != '404'){ 
      FBurl <- head(unique(rcrawl$ExternalLinks[which(grepl('facebook', rcrawl$ExternalLinks))]),1) #Alleen de unieke adressen met "facebook.com" erin en daar de eerste van
      if (length(FBurl) > 0){
        return(list(homepage = url, facebookpagina = FBurl))
      }
    }
  }
  return(list(homepage = url, facebookpagina = NA)) # Indien er geen valid homepage is of er geen facebook links zijn return NA
}

#test fb urls voor de 1e 20
#fburls <- lapply(df.lrk$contact_website[22:50], get_FBurl)

#fb urls voor hele bestand. Index is gelijk aan die van het dataframe df.lrk. Runtime op LRK bestand is ongeveer 4 uur.
links<- gsub(" ", "", (df.lrk$contact_website[which(df.lrk$contact_website!='NA')]), fixed = TRUE)
#start runtime meting
start_time <- Sys.time()
fburls <- lapply(links, get_FBurl)
#einde runtime meting
end_time <- Sys.time()
#print runtime
end_time - start_time
df.fb2 <- rbindlist(fburls,use.names=TRUE,fill=TRUE)
write.csv2(df.fb,"lrk_fburls_scrape_v2.csv")

# #alternatieve methode 
# #met for loop om troubleshooting makkelijker te maken, trycatch als connectie niet lukt en error counter
# #runtime is wel stuk hoger rond 19u, geen paralel computing.
# 
# #lege list aanmaken voor resultaten en var voor urls
# d <- NULL
# #Alleen opvang waarvan een url beschikbaar is runnen.En spaties weghalen met gsub.
# links<- gsub(" ", "", (df.lrk$contact_website[which(df.lrk$contact_website!='NA')]), fixed = TRUE)
# d <- vector("list", length(links))
# #start runtime meting
# start_time <- Sys.time()
# 
# 
# #for (i in 13000:13100)  { # testrun 100
# for (i in seq_along(links))  { # volledige loop
#     if (!(links[i] %in% names(d))) {
#     cat(paste("Scraping", links[i], "..."))
#     ok <- FALSE
#     counter <- 0
#     while (ok == FALSE & counter <= 5) {
#       counter <- counter + 1
#       out <- tryCatch({                  
#         get_FBurl(links[i])
#       },
#       error = function(e) {
#         Sys.sleep(3)
#         e
#       }
#       )
#       if ("error" %in% class(out)) {
#         cat(".")
#       } else {
#         ok <- TRUE
#         cat(" Done.")
#       }
#     }
#     cat("\n")
#     d[[i]] <- out
#     names(d)[i] <- links[i]
#   }
#   #evt pauze inbouwen om connecties te closen
#   Sys.sleep(3) 
#   closeAllConnections()
#   gc()
# } 
# #output van geneste lists naar dataframe
# df.fb <- rbindlist(d,use.names=TRUE,fill=TRUE)
# #einde runtime meting
# end_time <- Sys.time()
# #print runtime
# end_time - start_time
# 
# #write.csv2 fburls naar csv
# write.csv2(df.fb,"lrk_fburls_scrape.csv")

