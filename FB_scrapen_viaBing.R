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
  html %>% 
    # The relevant html tag voor de url in de zoekresultaten van bing
    html_nodes(".b_algo") %>% html_nodes("a") %>% 
    html_attr("href") 
    #html_text() %>% 
    # Trim additional white space
    str_trim() %>%                      
    # Convert the list into a vector
    unlist()                             
}

get_rating <- function(html){
  
  # The pattern you look for: the first digit after `count-`
  pattern = 'count-'%R% capture(DIGIT)    
  
  ratings <-  html %>% 
    html_nodes('.b_srtxtstarcolor') %>% 
    html_nodes('span') %>%
    html_attr('aria-label') %>%
    #html_text() %>% 
    # Apply the pattern match to all attributes
    #map(str_match, pattern = pattern) %>%
    # str_match[1] is the fully matched string, the second entry
    # is the part you extract with the capture in your pattern  
    map(2) %>%                             
    
    unlist()
  
  # Leave out the first instance, as it is not part of a review
  ratings[2:length(ratings)]               
}


get_data_table <- function(html, company_name){
  
  # Extract the Basic information from the HTML
  reviews <- get_reviews(html)
  reviewer_names <- get_reviewer_names(html)
  dates <- get_review_dates(html)
  ratings <- get_star_rating(html)
  
  # Combine into a tibble
  combined_data <- tibble(reviewer = reviewer_names,
                          date = dates,
                          rating = ratings,
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

