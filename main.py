import requests
from bs4 import BeautifulSoup as bs
import json
from utils import c_logging, n_logging
from random import *
import random
import re
import string
import time

with open('config.json') as file:
    config = json.load(file)
file.close()

if config['useproxies'] == "True":
    useproxies = "True"
else:
    useproxies = "False"


def enter(num):

    captchaurl = "https://kithnyc.typeform.com/to/ySnFiu?typeform-embed=popup-blank"
    url = "https://kithnyc.typeform.com/app/form/submit/ySnFiu"
    s = requests.session()
    headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'kithnyc.typeform.com',
    'Origin': 'https://kithnyc.typeform.com',
    'Referer': 'https://kithnyc.typeform.com/to/ySnFiu?typeform-embed=popup-blank',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
    }
    successcount = 0
    print("")

    for i in range(int(num)):
        time.sleep(2)
        print("")
        print("++++++++++++++++++++++++++++++++++")
        if useproxies == "True":
            aproxy = random.choice(open('proxies.txt').readlines())
            proxy = "http://" + aproxy
            print("Using proxy " + aproxy)

        firstname = config['FirstName']
        lastname = config['LastName']
        location = config['Location']
        email = ""

        suffixtitlel = ['jr', 'jr.', 'JR.', 'JR.', 'SR', 'sr.', 'sr', 'sr.',
                        'snr', 'SNR', 'SNR.', 'jnr', 'JNR', 'JNR.', 'II',
                        'III', '2nd', '3rd']
        suffixtitlenum = randint(0, len(suffixtitlel) - 1)
        suffix = suffixtitlel[suffixtitlenum]
        typelist = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
        typenum = randint(0, len(typelist) - 1)
        typee = typelist[typenum]
        if typee == "1":
            firstname = "Mr. " + firstname
        if typee == "2":
            firstname = "Mr. " + firstname
            lastname = lastname + " " + suffix
        if typee == "3":
            firstname = "Mr. " + firstname + " " + suffix
        if typee == "4":
            firstname = "Mr " + firstname
        if typee == "5":
            firstname = "Mr " + firstname
            lastname = lastname + " " + suffix
        if typee == "6":
            firstname = "Mr " + firstname + " " + suffix
        if typee == "7":
            firstname = "Mister " + firstname
        if typee == "8":
            firstname = "Mister " + firstname
            lastname = lastname + " " + suffix
        if typee == "9":
            firstname = "Mister " + firstname + " " + suffix
        if typee == "10":
            lastname = lastname + " " + suffix
        if typee == "11":
            firstname = firstname + " " + suffix
        
        print("Name:  " + firstname + " " + lastname)

        number = randint(111, 9999999)
        if number > 9999999:
            number = randint(111, 9999999)
        for x in range(0, 5):
            email += random.choice(string.ascii_letters)
        email += str(number) + '@' + config["Email"]
        print("Generated Email:  " + email)

        if config['sizegender'] == "male":
            sizelist = ['7', '8', '9', '10', '11']
        else:
            sizelist = ['6', '7', '8', '9', '10', '11']
        sizenum = randint(0, len(sizelist) - 1)
        asize = sizelist[sizenum]
        if config['sizegender'] == "male":
            size = "Men's " + asize
        else:
            size = "Women's " + asize
        print("Chose size:  " + size)

        if location == "soho":
            kithlocation = "Kith Soho"
        else:
            kithlocation = "Kith Brooklyn"

        d = requests.get("https://kithnyc.typeform.com/to/ySnFiu?typeform-embed=popup-blank")
        soup = bs(d.content, "html.parser")
        bigreturn = soup.find_all("script")
        jscap = str(bigreturn[21])
        capnohtml = re.sub("<.*?>", "", jscap)
        capfilter1 = capnohtml[26:]
        capfilter2 = capfilter1.split('"value":"')[1]
        captchavalue = capfilter2.split('"')[0]
        print("Obtained Captcha Answer ({})".format(captchavalue))



        payload = {
        'form[language]': 'en',
        'form[textfield:OSwjNf51Vlq5]': firstname,
        'form[textfield:WS8KFzUfJKZ6]': lastname,
        'form[email:mSTAlyznz1A1]': email,
        'form[list:Z89n81xJhqQK][choices]': kithlocation,
        'form[list:Z89n81xJhqQK][other]': '',
        'form[list:kXPnX9LjujQw][choices]': size,
        'form[list:kXPnX9LjujQw][other]': '',
        'form[textfield:p6P2thoLnUI4]': captchavalue,
        'form[landed_at]': int(time.time()),
        'form[token]': '641e8d6d42680852d04e1623235b7295$2y$11$e2dJZC0zIXZQK1pxbSZbL.iWNMlMlNL.HW4Y/MIZPaow0szjB6mUm'
        }

        if useproxies == "True":
            j = s.post(url, headers=headers, proxies=proxy, data=payload)
            print("Sending Request")
        else:
            j = s.post(url, headers=headers, data=payload)
            print("Sending Request")


        if j.status_code == 200:
            print("Entered Account")
            print("++++++++++++++++++++++++++++++++++")
            print(successcount)
            successcount = successcount + 1
        else:
            print("FAILED TO ENTER ACCOUNT")
            print("++++++++++++++++++++++++++++++++++")
            print(j.text)
            print(j.status_code)
    if successcount < 1:
        print("NO ENTRIES MADE")
    else:
        print("-----------------------------")
        print("Successfully Entered " + str(successcount) + "/" + str(num))


if __name__ == '__main__':
    print("")
    print("##########################################")
    print("Kith Futurecraft Script")
    print("By XO and Rycao18")
    print("Wanna buy me a big mac? paypal.me/rycao18 or paypal.me/daddyxd")
    print("###########################################")
    print("===========================================")
    print("Name: " + config['FirstName'] + " " + config['LastName'])
    print("Email: " + config['Email'])
    print("Size Gender: " + config['sizegender'])
    print("Location: " + config['Location'])
    print("Using Proxies?: " + config['useproxies'])
    print("==========================================")
    num = input("Number of entries?: ")

    enter(num)
