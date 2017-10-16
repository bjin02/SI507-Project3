from bs4 import BeautifulSoup
import unittest
import requests
import csv

#########
## Instr note: the outline comments will stay as suggestions, otherwise it's too difficult.
## Of course, it could be structured in an easier/neater way, and if a student decides to commit to that, that is OK.

## NOTE OF ADVICE:
## When you go to make your GitHub milestones, think pretty seriously about all the different parts and their requirements, and what you need to understand. Make sure you've asked your questions about Part 2 as much as you need to before Fall Break!


######### PART 0 #########
def read_cache_data(url, file):
    try:
        data = open(file,'r', encoding='utf-8').read()
    except:
        data = requests.get(url).text
        f = open(file, 'w', encoding='utf-8')
        f.write(data)
        f.close()
    return data

gallery_data = read_cache_data("http://newmantaylor.com/gallery.html", "gallery.html")

gallery = BeautifulSoup(gallery_data, 'html.parser')

all_imgs = gallery.find_all('img')
for img in all_imgs:
    print(img.get('alt', "No alternative text provided!"))

######### PART 1 #########

# Get the main page data...

# Try to get and cache main page data if not yet cached
# Result of a following try/except block should be that
# there exists a file nps_gov_data.html,
# and the html text saved in it is stored in a variable 
# that the rest of the program can access.

# We've provided comments to guide you through the complex try/except, but if you prefer to build up the code to do this scraping and caching yourself, that is OK.

NPS_URL = "https://www.nps.gov"
nps_gov_data = read_cache_data("https://www.nps.gov/index.htm", "nps_gov_data.html")
nps_gov = BeautifulSoup(nps_gov_data, 'html.parser')

# Get individual states' data...

# Result of a following try/except block should be that
# there exist 3 files -- arkansas_data.html, california_data.html, michigan_data.html
# and the HTML-formatted text stored in each one is available
# in a variable or data structure 
# that the rest of the program can access.

# TRY: 
# To open and read all 3 of the files

# But if you can't, EXCEPT:

# Create a BeautifulSoup instance of main page data 
# Access the unordered list with the states' dropdown

# Get a list of all the li (list elements) from the unordered list, using the BeautifulSoup find_all method

# Use a list comprehension or accumulation to get all of the 'href' attributes of the 'a' tag objects in each li, instead of the full li objects

# Filter the list of relative URLs you just got to include only the 3 you want: AR's, CA's, MI's, using the accumulator pattern & conditional statements


# Create 3 URLs to access data from by appending those 3 href values to the main part of the NPS url. Save each URL in a variable.


## To figure out what URLs you want to get data from (as if you weren't told initially)...
# As seen if you debug on the actual site. e.g. Maine parks URL is "http://www.nps.gov/state/me/index.htm", Michigan's is "http://www.nps.gov/state/mi/index.htm" -- so if you compare that to the values in those href attributes you just got... how can you build the full URLs?


# Finally, get the HTML data from each of these URLs, and save it in the variables you used in the try clause
# (Make sure they're the same variables you used in the try clause! Otherwise, all this code will run every time you run the program!)


# And then, write each set of data to a file so this won't have to run again.
def read_cache_state_data(filter_id, file, nps_gov):
    try:
        data = open(file, 'r', encoding='utf-8').read()
        return data
    except:
        all_li = nps_gov.find_all('li')
        for li in all_li:
            for x in li.find_all('a'):
                url = x['href']
                if filter_id in url:
                    state_url = NPS_URL + url
                    data = requests.get(state_url).text
                    f = open(file, 'w', encoding='utf-8')
                    f.write(data)
                    f.close()
                    return data

arkansas_data = read_cache_state_data('ar', 'arkansas_data.html', nps_gov)
california_data = read_cache_state_data('ca', 'california_data.html', nps_gov)
michigan_data = read_cache_state_data('mi', 'michigan_data.html', nps_gov)


######### PART 2 #########

## Before truly embarking on Part 2, we recommend you do a few things:

# - Create BeautifulSoup objects out of all the data you have access to in variables from Part 1
# - Do some investigation on those BeautifulSoup objects. What data do you have about each state? How is it organized in HTML?

# HINT: remember the method .prettify() on a BeautifulSoup object -- might be useful for your investigation! So, of course, might be .find or .find_all, etc...

# HINT: Remember that the data you saved is data that includes ALL of the parks/sites/etc in a certain state, but you want the class to represent just ONE park/site/monument/lakeshore.

# We have provided, in sample_html_of_park.html an HTML file that represents the HTML about 1 park. However, your code should rely upon HTML data about Michigan, Arkansas, and Califoria you saved and accessed in Part 1.

# However, to begin your investigation and begin to plan your class definition, you may want to open this file and create a BeautifulSoup instance of it to do investigation on.

# Remember that there are things you'll have to be careful about listed in the instructions -- e.g. if no type of park/site/monument is listed in input, one of your instance variables should have a None value...

arkansas = BeautifulSoup(arkansas_data, 'html.parser')
california = BeautifulSoup(california_data, 'html.parser')
michigan = BeautifulSoup(michigan_data, 'html.parser')

## Define your class NationalSite here:
class NationalSite:
    def __init__(self, data):
        self.data = data
        try:
            self.location = data.find("h4").get_text()
        except:
            self.location = ""
        try:
            self.name = data.find("h3").get_text()
        except:
            self.name = ""
        try:
            self.type = data.find("h2").get_text()
        except:
            self.type = None
        try:
            self.description = data.find("p").get_text()
        except:
            self.description = ""

    def __str__(self):
        return "{} | {}".format(self.name, self.location)

    def __contains__(self, input):
        return input in self.name

    def get_mailing_address(self):
        for li in self.data.find_all("li"):
            for x in li.find_all('a'):
                url = x['href']
                if 'basicinfo' in url:
                    info = BeautifulSoup(requests.get(url).text)
                    try:
                        streetAddress = info.find("span", {"itemprop": "streetAddress"}).get_text().strip()
                    except:
                        streetAddress = ""
                    try:
                        addressLocality = info.find("span", {"itemprop": "addressLocality"}).get_text().strip()
                    except:
                        addressLocality = ""
                    try:
                        addressRegion = info.find("span", {"itemprop": "addressRegion"}).get_text().strip()
                    except:
                        addressRegion = ""
                    try:
                        postalCode = info.find("span", {"itemprop":"postalCode"}).get_text().strip()
                    except:
                        postalCode = ""
                    return "{}, {}, {}, {}".format(streetAddress, addressLocality, addressRegion, postalCode)
        return ""

## Recommendation: to test the class, at various points, uncomment the following code and invoke some of the methods / check out the instance variables of the test instance saved in the variable sample_inst:

# f = open("sample_html_of_park.html",'r')
# soup_park_inst = BeautifulSoup(f.read(), 'html.parser') # an example of 1 BeautifulSoup instance to pass into your class
# sample_inst = NationalSite(soup_park_inst)
# f.close()


######### PART 3 #########

# Create lists of NationalSite objects for each state's parks.

# HINT: Get a Python list of all the HTML BeautifulSoup instances that represent each park, for each state.
def generate_site(data, sites):
    all_sites = data.find_all("li", {"class":"clearfix"})
    for each in all_sites:
        sites.append(NationalSite(each))

california_natl_sites = []
arkansas_natl_sites = []
michigan_natl_sites = []

generate_site(california, california_natl_sites)
generate_site(arkansas, arkansas_natl_sites)
generate_site(michigan, michigan_natl_sites)

##Code to help you test these out:
# for p in california_natl_sites:
# 	print(p)
# for a in arkansas_natl_sites:
# 	print(a)
# for m in michigan_natl_sites:
# 	print(m)



######### PART 4 #########

## Remember the hints / things you learned from Project 2 about writing CSV files from lists of objects!

## Note that running this step for ALL your data make take a minute or few to run -- so it's a good idea to test any methods/functions you write with just a little bit of data, so running the program will take less time!

## Also remember that IF you have None values that may occur, you might run into some problems and have to debug for where you need to put in some None value / error handling!
def writeToCSVFile(fileName, sites):
    with open(fileName, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Location", "Type", "Address", "Description\n"])
        for obj in sites:
            writer.writerow([obj.name, obj.location, obj.type, obj.get_mailing_address(), obj.description])

writeToCSVFile("arkansas.csv", arkansas_natl_sites)
writeToCSVFile("california.csv", california_natl_sites)
writeToCSVFile("michigan.csv", michigan_natl_sites)