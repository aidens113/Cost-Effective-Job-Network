# Cost-Effective-Job-Network
The Network is a collection of freelance job boards and marketplaces on Telegram and Discord. The Network bot automatically posts messages to these chatrooms, allowing employers to get free applications.


<h1>SETUP</h1><br>

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




