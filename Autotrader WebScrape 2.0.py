from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

### This is a web scrapping script for scrapping details from adverts on autotrader.com and writing them to CSV ###
### The specific URL is from an intial search for cars £500 - £1,000, within 5 miles of a local area and excluding cars written off ###
### conditions: must excluding cars written off and select used cars only


def scrape_vehicle_info(number_of_pages_to_parse):

    # Page counter to parse through each page of results
    page_number = 1

    # Setting up the CSV file
    filename = "Autotrader Listings.csv"
    headers = "Name,Price,Year and Reg Plate,Class,Mileage,Engine Capacity,BHP,Gearbox\n"
    file = open(filename, "w")
    file.write(headers)

    # While loop to be able to parse through each page of results
    # Change page number limit as desired
    while page_number <= number_of_pages_to_parse:

        # Sense checking
        print(page_number)

        # URL page for Autotrader to web scrape including results page number
        page_url = "https://www.autotrader.co.uk/car-search?sort=relevance&postcode=kt153sl&radius=5&onesearchad=Used" \
                   "&onesearchad=Nearly%20New&onesearchad=New&price-from=500&price-to=1000&exclude-writeoff" \
                   "-categories=on&page="+ str(page_number)

        # Opening connection to Autotrader website
        uClient = urlopen(page_url)

        # Storing raw html as a variable
        page_html = uClient.read()

        # Closing connection
        uClient.close()

        # Reading the raw html code with bs4 to be able to parse
        page_soup = soup(page_html, "html.parser")

        # Gathering all the containers with info to scrape from the 1st results page
        ad_containers = page_soup.findAll("article")

        # for loop to scrape vehicle prices for all listings across each web page
        for details in ad_containers:
            # Advert Description (car name)
            a = details.h2.a.text
            print("Description: " + details.h2.a.text)

            # Advert Price
            car_price = (details.findAll("div", {"class": "vehicle-price"}))
            b = car_price[0].text
            print("vehicle price: " + car_price[0].text)

            ### Generic container for the other key specs. Used below to scrape additional details
            list_of_key_specs = details.findAll("ul", {"class": "listing-key-specs"})

            # Year and Reg
            c = list_of_key_specs[0].findAll("li")[0].text
            print("Year and Reg: " + list_of_key_specs[0].findAll("li")[0].text)

            # Car Class
            d = list_of_key_specs[0].findAll("li")[1].text
            print("Car Class: " + list_of_key_specs[0].findAll("li")[1].text)

            # Mileage
            e = list_of_key_specs[0].findAll("li")[2].text
            print("Mileage: " + list_of_key_specs[0].findAll("li")[2].text)

            # Engine Capacity
            f = list_of_key_specs[0].findAll("li")[3].text
            print("Engine Capacity: " + list_of_key_specs[0].findAll("li")[3].text)

            # Horsepower
            g = list_of_key_specs[0].findAll("li")[4].text
            print("Horsepower: " + list_of_key_specs[0].findAll("li")[4].text)

            # Gearbox
            h = list_of_key_specs[0].findAll("li")[5].text
            print("Gearbox: " + list_of_key_specs[0].findAll("li")[5].text)

            # Writing all scraped features to open CSV file (deliminator: comma)
            file.write(a.replace(",", "|") + "," + b.replace(",", "") + "," + c + "," + d + "," + e.replace(",", "") + "," + f + "," + g + "," + h + "\n")


        # Adds one to page counter to enable while loop to continue and parse the next results page
        page_number += 1

    # Closing the file
    file.close()


scrape_vehicle_info(5)

### end of code ###
