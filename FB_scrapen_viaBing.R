#https://www.datacamp.com/community/tutorials/r-web-scraping-rvest
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

#inlezen data kinderopvang (zie google drive voor bestand)
#datascrape <- read.csv2("<vulje bestandlocatie in")
datascrape <- FBSCRAPE_export_opendata_lrk_authCE...IMPORTXML_FBdata


#URL friendly format (UTF-8) 
url <- str_conv(datascrape$URL, "UTF-8")
#test met 100
url <- head(url,100)
url <- str_replace_all(url, " ", "+") #spaties vervangen door + voor zoekmachines
html <- read_html(url[2])

#Set-up pagination: niet nodig nu omdat we meerdere url's al hebben in een var
# get_last_page <- function(html){
#   
#   pages_data <- html %>% 
#     # The '.' indicates the class
#     html_nodes('.pagination-page') %>% 
#     # Extract the raw text as a list
#     html_text()                   
#   
#   # The second to last of the buttons is the one
#   pages_data[(length(pages_data)-1)] %>%            
#     # Take the raw string
#     unname() %>%                                     
#     # Convert to number
#     as.numeric()                                     
#}

#first_page <- read_html(url)
                       
#(latest_page_number <- get_last_page(first_page))
#list_of_pages <- str_c(url, '?page=', 1:latest_page_number)



# Afzonderlijke pagina's scrapen
# url facebook ophalen
get_url <- function(html){
  FBurl <- html %>% 
    # The relevant html tag voor de url in de zoekresultaten van bing
    html_nodes(".b_algo") %>% html_nodes("a") %>% 
    html_attr("href") 
    #html_text() %>% 
    # Trim additional white space
    #str_trim() %>%                      
    # Convert the list into a vector
    unlist()
    FBtable <- data.table(FBurl)
    FBtable[, test := grepl("facebook", FBurl), by = FBurl]
    FBtable <- subset(FBtable, test == TRUE, FBurl)
    FBurl <- head(FBtable, 1)
}

get_rating <- function(html){
  rating <- html%>%
    html_nodes(".b_algo") %>% html_nodes(".b_sritem") %>% html_nodes("span") %>% html_attr("aria-label")  %>%
    map(1)
    rating <- rating[1]
}


#TOT HIER GEDAAN
get_data_table <- function(html, URL){
  
  # Extract the Basic information from the HTML
  fburl <- get_url(html)
  rating <- get_rating(html)
  
  
  # Combine into a tibble
  combined_data <- tibble(facebook = fburl,
                          fbrating = rating,
                          review = reviews) 
  
  # Tag the individual data with the company name
  combined_data %>% 
    mutate(company = company_name) %>% 
    select(company, reviewer, date, rating, review)
}

get_data_from_url <- function(url, company_name){
  html <- read_html(url)
  get_data_table(html, company_name)
}

