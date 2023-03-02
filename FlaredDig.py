""""
FlaredDig V1

Is a directory crawler for the CloudScraper python module

It pulls the default seetings for a session, however they can be changed in the script when the session is created

It will save all 200 returs in a seperate sheet for easy access. It drops all 404 errors and logs the reast in other csv

CloudFlare error 520 exits the script since CloudFlare is now blocking the session


"""

import cloudscraper
import contextlib
from bs4 import BeautifulSoup
import string
import warnings
from bs4 import GuessedAtParserWarning
import os
import re
import random
from datetime import datetime
from time import sleep


# Define global variables


wordlist = input("Enter full path of wordlist: ")
domain = input("Enter toplevel Domain ie ibm.com: ")
scanLevelInput = input("Enter levels you wish to scan domain you wish to scan (1-3): ")
scraper = cloudscraper.create_scraper(
    delay=10, browser=())
# counter to show amount of request remaing on current passthrough
counter = float(0)
RootScanArray = []
subd1ScanArray = []
subd2ScanArray = []
wordlistArray = []
stamp = datetime.now()

# Open wordlist and create wordlist variable
wordListParse = open(wordlist, "r")

for dirs in wordListParse:
    fixedDirs = re.sub('\n', '', dirs)
    wordlistArray.append(fixedDirs)
# Filter out warnings about issues with xml documents
warnings.filterwarnings('ignore', category=GuessedAtParserWarning)


# For loop to scan and parse directory info in to csv files

# level 1 root Scan
for dir in wordlistArray:
    
    #Random sleep timer btween 0.000000 and 2.00000 on seconds
    sleep (random.uniform(0, 2))

    # Variables for the loop.
    urlStr = str("https://"+domain+"/"+dir)
    urlStr = urlStr.translate({ord(c): None for c in string.whitespace})
    output200 = open(""+domain+".valid.csv", "a")
    output300 = open(domain+".redirects.csv", "a")
    totalRequests = float(len(wordlistArray))
    htmlResponce = scraper.get(urlStr, allow_redirects=False )
    soup = BeautifulSoup(htmlResponce.text, "html5lib")



    if htmlResponce.status_code == 200:
        os.system('clear')
        with contextlib.redirect_stdout(output200):
            print(htmlResponce.status_code, ",", soup.find(
                "head").find("title"), ",", dir, ",", stamp)
        RootScanArray.append(dir)
        counter += 1
        print("Total requets remaining in root scan: ",
              (totalRequests - counter))

        # 404 errors incremnet the count put are not logged
    elif htmlResponce.status_code == 404:
        os.system('clear')
        counter += 1
        print("Total requets remaining in root scan:",
              (totalRequests - counter))
    elif htmlResponce.status_code == 520:
        with contextlib.redirect_stdout(output300):
            print(htmlResponce.status_code, ",", stamp, ", exiting program because of cloudflare error 520")
            exit()

        # all other codes are logged
    else:
        os.system('clear')
        with contextlib.redirect_stdout(output300):
            print(htmlResponce.status_code, ",", soup.find(
                "head").find("title"), ",", dir,",", stamp)
            counter += 1
        print("Total requets remaining in root scan:",
                  (totalRequests - counter))

# repeats the scans with the successful urls from the first scan

scanLevel = int(3 - scanLevelInput)
RootScanArray.clear()

# level 2 scan
if scanLevel != 3:
    for sub in RootScanArray:
        for dir in wordlistArray:
            #Random sleep timer btween 0.000000 and 2.00000 on seconds
            sleep (random.uniform(0, 2))

            # Variables for the loop.
            urlStr = ("https://"+domain+"/"+sub+"/"+dir)
            urlStr = urlStr.translate(
                {ord(c): None for c in string.whitespace})
            output200 = open(""+domain+".valid.csv", "a")
            output300 = open(domain+".redirects.csv", "a")
            totalRequests = float(len(RootScanArray) + 1 * len(wordlistArray))
            htmlResponce = scraper.get(urlStr, allow_redirects=False)
            soup = BeautifulSoup(htmlResponce.text, "html5lib")
            counter = 0  # reset couter

            if htmlResponce.status_code == 200:
                os.system('clear')
                with contextlib.redirect_stdout(output200):
                    print(htmlResponce.status_code, ",", soup.find(
                        "head").find("title"), ",", sub, "/", dir, ",", stamp)
                currentDir = sub, "/", dir, ""
                subd2ScanArray.append(currentDir)
                counter += 1
                print("Total requets remaining in scan level 2: ",
                      (totalRequests - counter))

            elif htmlResponce.status_code == 404:
                os.system('clear')
                counter += 1
                print("Total requets remaining in scan level 2: ",
                      (totalRequests - counter))
        
            elif htmlResponce.status_code == 520:
                with contextlib.redirect_stdout(output300):
                    print(htmlResponce.status_code, ",", stamp, ", exiting program because of cloudflare error 520")
                    exit()
            else:
                os.system('clear')
                with contextlib.redirect_stdout(output300):
                    print(htmlResponce.status_code, ",", soup.find(
                        "head").find("title"), ",", currentDir,",",  stamp)
                counter += 1
                print("Total requets remaining in scan level 2: ",
                      (totalRequests - counter))
else:
    scanLevelInput -= 1

scanLevel = int(3 - scanLevelInput)

# level 3 Scan
if scanLevel != 3 or 2:
    for sub2 in subd2ScanArray:
        for dir in wordlistArray:
            # Variables for the loop.
            
            #Random sleep timer btween 0.000000 and 2.00000 on seconds
            sleep (random.uniform(0, 2))
            
            urlStr = ("https://"+domain+"/"+sub2+"/"+dir)
            urlStr = urlStr.translate(
                {ord(c): None for c in string.whitespace})
            output200 = open(""+domain+".valid.csv", "a")
            output300 = open(domain+".redirects.csv", "a")
            totalRequests = float(len(RootScanArray) +
                                  1 * len(wordListParse.readlines()))
            htmlResponce = scraper.get(urlStr, allow_redirects=False)
            soup = BeautifulSoup(htmlResponce.text, "html5lib")
            counter = 0  # reset counter

            # First loop runs untill a valid url is found or it runs through the list

            if htmlResponce.status_code == 200:
                os.system('clear')
                with contextlib.redirect_stdout(output200):
                    print(htmlResponce.status_code, ",", soup.find(
                        "head").find("title"), ",", sub2, "/", dir, ",", stamp)
                
                counter += 1
                print("Total requets remaining in scan level 3: ",
                      (totalRequests - counter))

            elif htmlResponce.status_code == 404:
                os.system('clear')
                counter += 1
                print("Total requets remaining in scan level 3: ",
                      (totalRequests - counter))
            
            elif htmlResponce.status_code == 520:
                with contextlib.redirect_stdout(output300):
                    print(htmlResponce.status_code, ",", stamp, ", exiting program because of cloudflare error 520")
                    exit()

            else:
                os.system('clear')
                with contextlib.redirect_stdout(output300):
                    print(htmlResponce.status_code, ",", soup.find(
                        "head").find("title"), ",", currentDir)
                counter += 1
                print("Total requets remaining in scan level 3: ",
                      (totalRequests - counter))
else:
    scanLevelInput -= 1

scanLevel = int(3 - scanLevelInput)

if scanLevel != 3 or 2 or 1:
    exit
