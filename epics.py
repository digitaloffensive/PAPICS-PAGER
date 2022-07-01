import requests
import re
import bs4
from bs4 import BeautifulSoup
import linecache
import csv
import os
from twilio.rest import Client

#EPICS status check pager
#REGSTRING for SESSION KEY: T\$CU_SESSION_KEY=(.*);\s

#Authentication and session keys
#Change CU_USER and CU_Pass to your PICS credentials
#bkey becoems the session key for use durign running, new key generate each time.

##################################################################################
try:
    bg_back = "https://epics.pa.gov:443/PICS/PicsWeb.dll/Login"

    bg_headers = {"Cache-Control": "max-age=0", "Sec-Ch-Ua": "\"Chromium\";v=\"95\", \";Not A Brand\";v=\"99\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"macOS\"", "Upgrade-Insecure-Requests": "1", "Origin": "https://epics.pa.gov", "Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://epics.pa.gov/Pics/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}

    bg_data = {"T$CU_USER": "ENTER YOUR INFO HERE", "T$CU_PASS": "ENTER YOUR INFO HERE", "T$CU_SEND": "Login"}

    res = requests.post(bg_back, headers=bg_headers, data=bg_data)

    bstring = str(res.headers)

    bg_key = re.search(r"\w{61}", bstring)

    bkey = bg_key.group()

    #print (bkey)

####################################################################################
# Check Status of a customer
# Eventually tie this to a database of users.
####################################################################################

## Communicate with epics and get status log
###################################################################################
    stat_url = "https://epics.pa.gov:443/PICS/PicsWeb.dll/Firearms?T$CU_cmd=Status&T$CU_DB=1"

    stat_cookies = {"T$CU_SESSION_KEY": bkey, "T$CU_TRANSACTION_TYPE": "1"}
    #print (stat_cookies)

    stat_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"95\", \";Not A Brand\";v=\"99\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"macOS\"", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://epics.pa.gov/PICS/PicsWeb.dll/Firearms?T$CU_cmd=Purchase&T$CU_TRANSACTION_TYPE=1", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}

    status = requests.get(stat_url, headers=stat_headers, cookies=stat_cookies)

## Save status so we are only making one request to pics per cycle check
#################################################################################

    f = open("status.log", "w+")
    f.write(status.text)
    f.close()

################################################################################
##
## Twillio Conf stuff
    account_sid = 'ENTER YOUR INFO HERE'
    auth_token = 'ENTR YOUR INFO HERE'
 ## Canned responses
    mre = "Your Background status is: Research, Come see us for more info!"
    mde = "Your Background status is: Denied, Come see us for more info!"
    maw = "Your Background status is: Approved, Come see us to complete purchase!"
###############################################################################

## Change looup to be user to find status of . Then find status, status is always 
## 9 lines below their name
#################################################################################
    with open('client.txt') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            lookup = row[0]
            filepath = 'status.log'
            with open("status.log") as myFile:
                try:
                    for num, line in enumerate(myFile, 1):
                        if lookup in line:
                            #print ('found at line:', num)
                            numstat = (num + 9)
                            linestat = linecache.getline(filepath,numstat)
                            #print (linestat)
                            stats  = [linestat]
                            for s in stats:

                                if 'Research' in s:
                                    #print("Research")
                                    client = Client(account_sid, auth_token)

                                    message = client.messages.create(
                                        messaging_service_sid='MGa6bb580e067d9f57377994f1e9ccc21b',
                                        body= lookup +': '+ mre,
                                        to='+1'+row[1])
                                    os.system('python /var/www/html/remove.py ' +  row[1])

                                elif 'Denied' in s:
                                    client = Client(account_sid, auth_token)

                                    message = client.messages.create(
                                        messaging_service_sid='MGa6bb580e067d9f57377994f1e9ccc21b',
                                        body= lookup +': '+ mde,
                                        to='+1'+row[1])

                                    os.system('python /var/www/html/remove.py ' +  row[1])

                                elif 'Approved - Waiting Acceptance' in s:
                                    client = Client(account_sid, auth_token)

                                    message = client.messages.create(
                                        messaging_service_sid='MGa6bb580e067d9f57377994f1e9ccc21b',
                                        body= lookup +': '+ maw,
                                        to='+1'+row[1])

                                    os.system('python /var/www/html/remove.py ' +  row[1])

                                elif '' in s:
                                    os.system('echo etf > /var/pics.log')

                                else:
                                    os.system('echo'+ lookup + ': Status: Pending >> /var/www/html/status.html')

                except:
                    print ("condition not matched")
except:
    print("connection to PICS FAILED")
