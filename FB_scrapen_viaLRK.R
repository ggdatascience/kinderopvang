#Verkrijgen facebooklinks adv open LRK dataset
#Chris Elschot & Jeroen ter Voert
#Laatste update oktober 2019

#factors omzetten naar strings
options(stringsAsFactors = FALSE)

#vereiste packages laden
#library(curl)
library(rvest)

#data via https://data.overheid.nl/dataset/gegevens-kinderopvanglocaties-lrk
#inlezen data kinderopvang
df.lrk <- read.csv2("http://www.landelijkregisterkinderopvang.nl/opendata/export_opendata_lrk.csv")
#gastouders eruit
df.lrk <- df.lrk[df.lrk$type_oko != "VGO", ]
#geen website naar NA
df.lrk$contact_website[which(df.lrk$contact_website == "")] <- NA

#gebruik proxy settings via curl (ivm firewall issues))
#curl_proxy <- function(url, verbose = TRUE){
#  proxy <- ie_get_proxy_for_url(url)
#  h <- new_handle(verbose = verbose, proxy = proxy)
#  curl(url, handle = h)
#}

#functie die op contact_website zoekt naar facebook websites
get_FBurl <- function(url){
  if (is.na(url)){
    return(list(homepage = url, facebookpage = NA)) #testen of input NA is, zoja return NA
  }
  try(html <- read_html(url)) #Inlezen html van de webpagina
  if (exists('html')){ #kijken of object all_urls bestaat
    all_urls <- html %>%
      html_nodes("a") %>% #Hyperlinks worden gedefinieerd met de HTML <a> tag
      html_attr("href") #Het href attribuut bevat het webadres waar naar gelinkt wordt
    FBurl <- unique(all_urls[which(grepl('facebook.com', all_urls))]) #Alleen de unieke adressen met "facebook.com" erin
    if (length(FBurl) > 0){
      return(list(homepage = url, facebookpage = FBurl)) #kan meerdere waarden bevatten dus returnen als list
    }
  }
  return(list(homepage = url, facebookpage = NA)) # Indien er geen valid homepage is of er geen facebook links zijn return NA
}

#fb urls voor de 1e 20
#fburls <- lapply(df.lrk$contact_website[1:20], get_FBurl)

#fb urls voor hele bestand. Index is gelijk aan die van het dataframe df.lrk
#om het script sneller te maken zouden de NA's uit de input gefilterd kunnen worden, deze returnen namelijk toch altijd NA.
fburls <- lapply(df.lrk$contact_website, get_FBurl)