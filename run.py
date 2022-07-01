import os
import time

os.system('echo Pics > /var/pics.log')
try:
    os.system('> /var/www/html/client.txt')
    time.sleep(2)
    os.system('python /var/www/html/status.py')
    time.sleep(2)
    os.system('python3 /var/www/html/epics.py')
    time.sleep(2)
    os.system('cp /var/www/html/status.log /var/www/status.html && chmod 755 /var/www/html/status.html')
except:
    os.system('echo failed > /var/pics.log')
