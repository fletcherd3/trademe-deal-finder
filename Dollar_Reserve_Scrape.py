'''
Dollar_reserve_self.scrape.py
One Dollar Reserve self.scrape and Compare

Created by Fletcher Dick on 8/07/18.
Copyright © 2018 Fletcher Dick. All rights reserved.
'''

import requests
from bs4 import BeautifulSoup
import time  # For delaying request intervals
import random  # For setting random time delays

from lxml.html import fromstring
from itertools import cycle  # For cycling through proxies
import traceback


class TradeMe:

    def __init__(self):

        # List of possible headers
        self.user_agent_list = [
            # Chrome
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML'
            ', like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML,'
            'like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML,'
            'like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML,'
            'like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gec'
            'ko) Chrome/44.0.2403.157 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML,'
            'like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML'
            ',like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML,'
            'like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML'
            ', like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML,'
            'like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            # Firefox
            'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Geck'
            'o',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5'
            '.0)',
            'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Geck'
            'o',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gec'
            'ko',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
            'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Geck'
            'o',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like'
            'Gecko',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/'
            '6.0)',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NE'
            'T CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
        ]

    def welcome(self):
        '''Welcomes the User and asks for inputs.
        '''

        if self.yes_or_no('Do you want to use default settings?'):
            self.category, self.freeShipping, self.max_pay, self.buyNow, \
                self.page_amount, self.time_interval = '', '', 10000000, '', 1, 1
            return
        print()
        self.time_interval = 0
        if self.yes_or_no('Do you want random time intervals between each request?'):
            self.time_interval = 1  # Will run the time intervals
        print()
        if self.yes_or_no('Would you like to select a specific category?'):
            self.category = self.showCategories()
            if self.category == 0:  # If custom self.category was selected
                print()
                self.category = input("Please enter your category number. eg: 202 ")
                self.category = ("&cid={}" .format(self.category))
        else:
            self.category = ''
        print()
        if self.yes_or_no('Do you want to only show listings with free shipping?'):
            self.freeShipping = '&shipping=free'
        else:
            self.freeShipping = ''
        print()
        if self.yes_or_no('Do you want to only show listings with a Buy Now?'):
            self.buyNow = '&buy=buyNow'
        else:
            self.buyNow = ''
        print()
        while True:
            try:
                self.max_pay = input(
                    "Enter a price limit (Enter nothing for no limit)... ")

                if self.max_pay == '':
                    self.max_pay = 10000000
                    break
                else:
                    self.max_pay = int(self.max_pay)  # Check if input was type'int'

                    if self.max_pay <= 0:
                        print("Error: '{}' is not a valid option Try Again." .format(self.max_pay))
                        print()
                    else:
                        break
            except ValueError:
                print("Error: You didn't enter a number. Try Again.")
                print()
        print()
        while True:
            try:
                self.page_amount = int(input(
                    "How many pages do you want to scrape? (50 listings per page) "))

                if self.page_amount <= 0 or self.page_amount > 460:
                    print("Error: '{}' is not a valid option Try Again." .format(self.page_amount))
                    print()
                else:
                    break
            except ValueError:
                print("Error: You didn't enter a number. Try Again.")
                print()

    def showCategories(self):
        '''Displays the user a nice option menu with 'Previous' and 'Next'
        page options to select their category. The function return the categories
        id.
        '''

        # List of Trade Me categories linked with their URL code
        self.categories = [
                      ['Trade Me Motors', '&cid=1'],
                      ['Antiques & collectables', '&cid=187'],
                      ['Art', '&cid=339'], ['Baby gear', '&cid=351'],
                      ['Books', '&cid=193'],
                      ['Building & renovation', '&cid=5964'],
                      ['Business, farming & industry', '&cid=10'],
                      ['Clothing & Fashion', '&cid=153'], ['Computers', '&cid=2'],
                      ['Crafts', '&cid=341'],
                      ['Electronics & photography', '&cid=124'],
                      ['Gaming', '&cid=202'], ['Health & beauty', '&cid=4798'],
                      ['Home & living', '&cid=4'],
                      ['Jewellery & watches', '&cid=246'],
                      ['Mobile phones', '&cid=344'],
                      ['Movies & TV', '&cid=3'],
                      ['Music & instruments', '&cid=343'],
                      ['Pets & animals', '&cid=9425'],
                      ['Pottery & glass', '&cid=340'], ['Sports', '&cid=5'],
                      ['Toys & models', '&cid=347'],
                      ['Travel, events & activities', '&cid=9374'],
                      ['Enter custom category code', 0]]

        def invalidOption():
            '''Checks given input for choosing category and checks if it is valid.
            '''
            try:
                self.ans = int(self.ans)
                if self.ans < 0 or self.ans > 9:  # Outside of range
                    print("Error: Enter a listed number. Try Again." .format(self.ans))
                    passTest = False
                else:
                    passTest = self.ans  # Valid Option
            except ValueError:
                print("Error: '{}' is not a number. Try Again." .format(self.ans))
                passTest = False

            return passTest

        def page0():
            '''Lists first 8 categories. Also automatically cleans input.
            '''
            print("PAGE 1")
            for i in range(1, 9):
                print("({}) {}" .format(i, self.categories[i-1][0]))
            print()
            print("(0) Next Page")
            print()
            print()
            self.ans = input("Select a category... ")

            if self.ans == '0':
                return 'page1'
            elif self.ans == '9':  # Invalid option
                self.ans = 10  # Will produce error

            if not invalidOption():
                return 'page0'

            return int(self.ans)

        def page1():
            '''Lists next 8 categories. Also automatically cleans input.
            '''

            print("PAGE 2")
            for i in range(9, 17):
                print("({}) {}" .format(i - 8, self.categories[i-1][0]))
            print()
            print("(9) Previous Page")
            print("(0) Next Page")
            print()
            print()
            self.ans = input("Select a category... ")

            if self.ans == '0':
                return 'page2'
            elif self.ans == '9':
                return 'page0'

            if not invalidOption():
                return 'page0'

            return int(self.ans) + 8

        def page2():
            '''Lists last 8 categories. Also automatically cleans input.
            '''

            print("PAGE 3")
            for i in range(17, 25):
                print("({}) {}" .format(i - 16, self.categories[i-1][0]))
            print()
            print("(9) Previous Page")
            print()
            print()
            self.ans = input("Select a category... ")

            if self.ans == '0':  # Invalid option
                self.ans = 10  # Will produce error
            elif self.ans == '9':
                return 'page1'

            if not invalidOption():
                return 'page0'

            return int(self.ans) + 16

        self.ans = 'page0'  # Start at the first page

        while True:  # This is the selector for the pages of categories
            if self.ans == 'page0':
                self.ans = page0()
            elif self.ans == 'page1':
                self.ans = page1()
            elif self.ans == 'page2':
                self.ans = page2()
            else:
                break

        self.category = self.categories[self.ans-1][1]
        return self.category

    def yes_or_no(self, question):
        '''Builds a simple Yes or No question from the passed question string.
        '''

        while True:  # Asks given yes or no question
            ans = input('{} (Y/N) ' .format(question)).lower().strip()

            if ans == 'y':
                return True

            if ans == 'n':
                return False

            print("Please enter a valid option")  # Error given if invalid ans
            print()

    def cleanTitle(self, title):
        '''Returns a clean title by striping unnecessary words/phrases.
        '''

        title = title.lower()
        deletePhrases = [
            '$1 reserve', '$1 res', '$1reserve', '$1res', '1 reserve',
                          '1 res', 'reserve', 'res', 'blue', 'green', 'red', 'brown', 'white',
                          'black', 'orange', 'pink', 'purple', 'yellow']  # delete these phrases from title

        for phrase in deletePhrases:
            if phrase in title:
                title = title.replace(phrase, '')
        title = " ".join(title.split())  # Delete double spaces

        return title

    def get_proxies(self):
        '''I do not take credit for this function, this was written by
        'SIM'(Stack OverFlow).

        The function scrapes 'free-proxy-list.net' for proxy ip and ports in the
        form of 'ip:port'.
        '''

        print()
        print("Obtaining Proxies...")
        res = requests.get('https://free-proxy-list.net/', headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(res.text, "lxml")
        self.proxies = []
        for items in soup.select("tbody tr"):
            proxy = ':'.join([item.text for item in items.select("td")[:2]])
            self.proxies.append(proxy)

        if not self.proxies:  # If no proxies were found
            print("Error: No proxies were scraped. Try Again.")
            quit()
        self.proxy_pool = cycle(self.proxies)

    def scrape(self):
        '''This function scrapes the Trade Me $1 Reserve site, it returns a
        dictionary in the form of:

        {Listing's Title : [Listings ID, Location, Remaining Time,
                            Highest Current Bid, Current Buy Now (default=0)]}

        The function returns a dictionary (listings).
        '''

        self.listings = {}  # Will hold all Trade Me listings

        for page_num in range(1, self.page_amount + 1):

            # One Dollar Reserve listing URL
            self.url = (
                'https://www.trademe.co.nz/Browse/OneDollarReserve.aspx/listings-onedollar.htm?page={}&sort_order=expiry_asc{}{}{}&v=List'
                .format(page_num, self.category, self.freeShipping, self.buyNow))

            # Pick a random user agent
            user_agent = random.choice(self.user_agent_list)
            # Set the headers
            headers = {'User-Agent': user_agent}
            # Make the request

            # Get a proxy from the pool
            proxy = next(self.proxy_pool)
            print()
            print("Scraping page '{}', {:.1f}% completed..." .format(
                page_num, ((page_num / self.page_amount) * 100)))
            try:
                source = requests.get(self.url, proxies=dict(
                    http="http://proxy_user:proxy_pass@{}" .format(proxy),
                    headers=headers, timeout=7))
                pageHTML = source.text
                soup = BeautifulSoup(pageHTML, "lxml")
            except:
                print("Skipping. Connnection error")

            if "blocked" in pageHTML:  # Ran if Trade Me has blocked Bot
                print ("Error: Your IP has been blocked.")
                exit()

            for item in soup.find_all('div', attrs={'class': 'supergrid-bucket largelist'}):

                itemsInfo = []

                # Grabbing listings current highest Bid
                bidPrice = item.find('div', class_='listingBidPrice').text
                bidPrice = bidPrice[1:]  # Taking out '$' Sign
                bidPrice = bidPrice.replace(',', '')  # Taking out commas
                bidPrice = float(bidPrice)  # Changing type to float

                # Skip Listing if the current bid price is higher than max_pay
                if bidPrice > self.max_pay:
                    continue

                # This grabs the link of the listing and the appends the items \id that
                # is in the link.
                for a in item.find_all('a'):
                    link = a.get('href')
                    itemsInfo.append(link[-53:-43])

                # Grabbing listings title
                title = item.find('div', class_='title').text
                title = title.strip()
                title = self.cleanTitle(title)

                # Grabbing listings location and appending to Info
                location = item.find('div', class_='location').text
                location = location.strip()
                itemsInfo.append(location)

                # Grabbing listings remaining time and appending to Info
                remainTime = item.find('div', class_='closing-soon-location').text
                remainTime = remainTime.strip()
                itemsInfo.append(remainTime)

                # Checking if listing has a Buy Now price, also appennding prices into
                # itemsInfo list
                try:
                    buyPrice = item.find('div', class_='listingself.buyNowPrice').text
                    buyPrice = buyPrice[1:]  # Taking out '$' Sign
                    buyPrice = buyPrice.replace(',', '')  # Taking out commas
                    buyPrice = float(buyPrice)  # Changing type to float

                    itemsInfo.append(bidPrice)
                    itemsInfo.append(buyPrice)

                except AttributeError:
                    itemsInfo.append(bidPrice)
                    itemsInfo.append(0)  # Enter '0' for buyNow price if Nill

                # If the current Bid Price is bellow users 'max_pay' then add to items Dict
                if bidPrice <= self.max_pay:
                    self.listings[title] = itemsInfo

            '''Before scraping next page check if user wanted multiple pages and
            introduce a random time interval.
            '''
            if self.page_amount != 1:  # Dont run if scraping one page
                if self.time_interval == 1:
                    timeDelay = random.randrange(0, 5)
                    time.sleep(timeDelay)

    def compareListing(self):
        '''This function takes each listings title and searches it through
        Trade Me and then compares the Current Bid Price with its simaler listings.
        '''

        compareCount = 1
        toDelete = []
        for listing in self.listings:

            # Replacing symbols with their URL code
            search = listing.replace('%', '+%25')

            search = search.replace('+', '%2B')
            search = search.replace('=', '%3D')
            search = search.replace('@', '%40')
            search = search.replace('# ', '%23')
            search = search.replace('$', '%24')
            search = search.replace('&', '%26')
            search = search.replace('/', '%2F')
            search = search.replace('?', '%3F')
            search = search.replace(';', '%3B')
            search = search.replace(':', '%3A')
            search = search.replace(' ', '+')

            url = ("https://www.trademe.co.nz/Browse/SearchResults.aspx?sort_order=&searchString={}&type=Search&searchType=all&v=List" .format(search))

            # Status/Loading bar
            print("Comparing Listing '{}', {:.1f}% completed..." .format(
                compareCount, ((compareCount / len(self.listings)) * 100)))
            compareCount += 1

            # Pick a random user agent
            user_agent = random.choice(self.user_agent_list)
            # Set the headers
            headers = {'User-Agent': user_agent}
            # Make the request

            # Get a proxy from the pool
            proxy = next(self.proxy_pool)
            print()
            # print("Scraping page '{}', {:.0f}% completed..." .format(page_num, ((page_num / page_amount) * 100)))
            try:
                source = requests.get(url, proxies=dict(
                    http="http://proxy_user:proxy_pass@{}" .format(proxy),
                    headers=headers, timeout=7))
                pageHTML = source.text
                soup = BeautifulSoup(pageHTML, "lxml")
            except:
                print("Skipping. Connnection error")

            if "blocked" in pageHTML:
                print ("Error: Your IP has been blocked.")
                print("Trying next listing with new IP.")
                continue

            '''You cannot delete a dictionaries key while iterating so the Key of
            a unique Listing is saved for after the for loop and then deleted.
            '''
            if 'No results matching' in pageHTML:
                print("No Results for listing.")
                print()
                toDelete.append(listing)
                continue

            bidPrices = []
            buyPrices = []

            for item in soup.find_all('div', attrs={'class': 'supergrid-bucket largelist'}):

                try:
                    # Grabbing listings current highest Bid
                    bidPrice = item.find('div', class_='listingBidPrice').text
                    bidPrice = bidPrice[1:]  # Taking out '$' Sign
                    bidPrice = bidPrice.replace(',', '')  # Taking out commas
                    bidPrice = float(bidPrice)  # Changing type to float
                    bidPrices.append(bidPrice)
                except AttributeError:
                    continue

                try:
                    buyPrice = item.find('div', class_='listingbuyNowPrice').text
                    buyPrice = buyPrice[1:]  # Taking out '$' Sign
                    buyPrice = buyPrice.replace(',', '')  # Taking out commas
                    buyPrice = float(buyPrice)  # Changing type to float

                    buyPrices.append(buyPrice)

                except AttributeError:
                    continue

            # Calculating average prices
            if len(bidPrices) == 0:
                avg_bidPrices = 0
            else:
                avg_bidPrices = (sum(bidPrices) / len(bidPrices))

            if len(buyPrices) == 0:
                avg_buyPrices = 0
            else:
                avg_buyPrices = (sum(buyPrices) / len(buyPrices))

            avg_bidPrices = float("{0:.2f}".format(avg_bidPrices))
            avg_buyPrices = float("{0:.2f}".format(avg_buyPrices))

            self.listings[listing].append(avg_bidPrices)
            self.listings[listing].append(avg_buyPrices)

            # Random time delay to avoid scrape detection
            if self.time_interval == 1:
                timeDelay = random.randrange(0, 5)
                time.sleep(timeDelay)

        # Delete unique lisitngs
        for key in toDelete:
            del self.listings[key]

    def getScore(self):
        '''Calculate score for each listing based on how well the current price
        compares to the average price for that item.
        '''

        for listing in self.listings:

            if self.listings[listing][5] == 0:
                score = (self.listings[listing][6] / self.listings[listing][3])

            elif self.listings[listing][6] == 0:
                score = (self.listings[listing][5] / self.listings[listing][3])

            else:
                score = (
                    (self.listings[listing][5] + self.listings[listing][6]) / 2) / self.listings[listing][3]

            self.listings[listing].append(score)

    def printListings(self):
        '''Sort listings by best score and print neatly.
        '''

        input("Program Completed! Press 'Enter' to see results!!")
        print()
        print()
        print("Ordered by highest returned score.")

        i = 0
        # Sorting by Score
        sortedListings = sorted(self.listings.items(), key=lambda e: e[1][7], reverse=True)
        for listing in sortedListings:
            i += 1
            print()
            print()
            print("Listing number '{}'" .format(i))
            print(listing[0])  # Title
            print(listing[1][2])  # Remaining Time
            print("Score: {:.0f}" .format(listing[1][7]))
            print("Location: {}" .format(listing[1][1]))

            # Only print price if it is not '0' (0 = no price)
            if listing[1][3] == 0:
                print("Buy Now: ${}" .format(listing[1][4]))
            if listing[1][4] == 0:
                print("Current Bid: ${}" .format(listing[1][3]))
            if listing[1][4] != 0 and listing[1][3] != 0:
                print("Current Bid: ${}" .format(listing[1][3]))
                print("Buy Now: ${}" .format(listing[1][4]))

            # Only print price if it is not '0' (0 = no price)
            if listing[1][5] == 0:
                print("Average Buy Now: ${}" .format(listing[1][6]))
            if listing[1][6] == 0:
                print("Average Current Bid: ${}" .format(listing[1][5]))
            if listing[1][6] != 0 and listing[1][5] != 0:
                print("Average Current Bid: ${}" .format(listing[1][5]))
                print("Average Buy Now: ${}" .format(listing[1][6]))

            print("Trade Me Listing ID: {}" .format(listing[1][0]))

    def Main(self):
        '''Call all functions.
        '''

        self.welcome()
        self.get_proxies()
        self.scrape()
        print()
        if self.listings == {}:  # If not listings found user was probably blocked
            print("Error: scrape returned no listings, you have been blocked :(")
            quit()
        else:
            print("scrape Successful! Data Secured.")
            print()
            print("Starting to compare listings.")
            print()
        self.compareListing()
        self.getScore()
        self.printListings()

while True:
    run = TradeMe()
    run.Main()
    ans = input("Press 'Enter' to make another scrape ")
