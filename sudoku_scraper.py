from bs4 import BeautifulSoup
import requests
import os
import datetime
import urllib.request

baseURL = "http://www.dailysudoku.com/sudoku/png/"

for day in range(1000):
    currDate = datetime.datetime.now() - datetime.timedelta(days = day)
    URL = baseURL + str(currDate.year) + '/' + currDate.strftime("%m") + '/' + currDate.strftime("%Y-%m-") + str(currDate.day) + '.png'

    dirname = 'img/dailysudoku/'
    filename = currDate.strftime("%Y-%m-%d") + '.png'
    filepath = dirname + '/' + filename

    try:
        os.makedirs(dirname)
    except FileExistsError:
        pass

    if not os.path.isfile(filepath): # If file exists already, just skip it
        try:
            resource = urllib.request.urlopen(URL)
            output = open(filepath,"wb")
            output.write(resource.read())
            output.close()
        except Exception as e:
            print("Failed on ", currDate.strftime("%Y-%m-%d"))