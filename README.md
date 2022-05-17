# Cost-Effective-Job-Network
The Network is a collection of freelance job boards and marketplaces on Telegram and Discord. The Network bot automatically posts messages to these chatrooms, allowing employers to get free applications.


<h1>Main.py Setup</h1><br>

**1. GMAIL SMTP**<br>
-Install the lastest version of chromedriver: https://chromedriver.chromium.org/downloads and put it in the same folder as main.py.<br>
-Sign up for a Gmail account: https://gmail.com and configure a custom app password: https://support.google.com/mail/answer/185833?hl=en. <br>
-Configure your Gmail SMTP details at the top of main.py (lines 33-34) using your Gmail email and the newly created app password.<br>

**2. UPLOAD PHP FILES TO WEBSERVER**<br>
-Setup a domain and hosting plan (I personally recommend Hostinger: https://hostinger.com). Buy a cheap $1 for the first year domain.<br>
-Upload the "mmbot" directory to your web hosting plan.<br>
-Create a new MySQL DB. Grab the database name, username, password. <br>
-Open your MySQL DB in PHPMyAdmin. Create a new table, name it "main". Create text columns named "jobid", "email", and "sent". <br>
-Configure moderation.php with your database details. It should look like: mysqli_connect("localhost", "DBusername", "DBpassword", "DBname");<br>

**3. TELEGRAM API SETUP**<br>
-Setup a new Telegram account and join groups that you want to broadcast job applications to. I've included multiple lists that you can use. You will have to manually join every group that the bot will broadcast in. <br>
-Setup new Telegram API ID and hash https://core.telegram.org/api/obtaining_api_id<br>
-Input your Telegram API ID and hash on lines 171-172<br>

**4. DISCORD SETUP**<br>
-This part is a bit tricky. There is a high likelyhood of your Discord account being banned, especially if you are running this 24/7. Discord is very ban-heavy so you will most likely need multiple phone numbers to create new Discord accounts each time one gets banned. If you run it sparingly and only join legit Discord servers, then it's much less likely you will be banned.<br>
-Join all the Discord servers you want the bot to broadcast in. **Use the web version of Discord to get links to every channel you want to broadcast in.**<br>
-Add every Discord server channel link to a custom named file. The main.py program will automatically grab new lists and you can choose to post to one or all of the lists. This allows you to create super niched down lists of servers. You can also use the lists that I included in /discordnetwork. Make sure to put all Discord list files in /discordnetwork.<br>
-You will need to be logged into Discord already on the computer you are running this bot. It's much safer to stay logged in and post. If the bot needs to log in every time it runs, you will be at much more risk of being banned.<br>
