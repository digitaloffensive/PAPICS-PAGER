# PAPICS-PAGER
As a gun dealer one of the most problematic items is background checks when they are not instantly approved due to delays in the system. Individuals will constantly hound you is their background done. Many times you are super busy to keep checking. With this script it will monitor the status of their check and alert them with one of three messages.

- Approved
- Reesearch
- Denied

While they are pending it does not send them anything however they can visit the status page of the app which will provide a visual which is updated everytime the status check is done so the ycan monitor themselves without needing access to the actual PICS system.

This is in beta testing.
The code is not very pretty as Iam using this to work on my python coding and due to limitations of certain libraries especially the mysql one for python 2 and 3 we had to use both versions of python. We also make use of dirty os.system. 

- You will need a twillio account to send pages. You can also send emails instead without a twilio account this can be done with ssmtp and configuring a ssmtp account from your trusted domain.

- You will need an acccount with access to PA PICS website. I would create an account dedicated for the script as it makes a request to PICS and gets a new auth token which will invalidate yours and cause connection issues if running backgrounds.

- Server to host script or have us host it for you for a small monthly fee.

Things to do:
- Pretty the UI and status board.
- Add sql injection protecction to the contact form. Posible add a pin access to avoid randos adding data to database.
- More testing to run it through it paces to kick out bugs. 
- collect metrics to graph how long it takes to process people
-- think race
-- age
-- sex

Can we correlate why it seems new gun owners are instantly approved while others are not? Will be share that info if we anon it?

How it works: The parts:

run.py: this script is added to the crontab, currently it is running between 9 am and 10 pm est as that is the hours of PICS. It will call the status.py and the epics.py. It also provides logging of its run and cleanup of the clients.txt.

status.py: this sccript creates a csv of the clients awaiting their background and stores it in client.txt which is used by epics.py

epics.py: This is the meat of the application it contaccts PICS using a rude authentication which was captured through burp and coverted into python. This is important as you will need to have the session key to run any checks. We used burp to parse out all teh calls to run it through python vs a web browsr. Once it is authenticated it will save the status tab to a local file, this local file feeds teh dashboard for end users but allows the sccript to search locally and loop through all the clients for their status. Once it finds the status it will alert them if the conditions are met to deem that they are to be contacted.

contact.php: this is the form client puts their first and last name and phone. Very simple, needs some security added to it.

insert.php: used to insert the contact .php into mysql database, will also format name in proper format.
