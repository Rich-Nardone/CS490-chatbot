# Set up React  
0. `cd ~/environment && git clone https://github.com/Sresht/project2-m2-rmn9/ && cd project2-m2-rmn9`    
1. Install your stuff!    
  a) `npm install`    
  b) `pip install flask-socketio`    
  c) `pip install eventlet`    
  d) `npm install -g webpack`    
  e) `npm install --save-dev webpack`    
  f) `npm install socket.io-client --save`    
:warning: :warning: :warning: If you see any error messages, make sure you use `sudo pip` or `sudo npm`. If it says "pip cannot be found", run `which pip` and use `sudo [path to pip from which pip] install` :warning: :warning: :warning:    
  
# Getting PSQL to work with Python  
  
1. Update yum: `sudo yum update`, and enter yes to all prompts    
2. Upgrade pip: `sudo /usr/local/bin/pip install --upgrade pip`  
3. Get psycopg2: `sudo /usr/local/bin/pip install psycopg2-binary`    
4. Get SQLAlchemy: `sudo /usr/local/bin/pip install Flask-SQLAlchemy==2.1`    
  
# Setting up PSQL  
  
1. Install PostGreSQL: `sudo yum install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-docs`    
    Enter yes to all prompts.    
2. Initialize PSQL database: `sudo service postgresql initdb`    
3. Start PSQL: `sudo service postgresql start`    
4. Make a new superuser: `sudo -u postgres createuser --superuser $USER`    
    :warning: :warning: :warning: If you get an error saying "could not change directory", that's okay! It worked! :warning: :warning: :warning:    
5. Make a new database: `sudo -u postgres createdb $USER`    
        :warning: :warning: :warning: If you get an error saying "could not change directory", that's okay! It worked! :warning: :warning: :warning:    
6. Make sure your user shows up:    
    a) `psql`    
    b) `\du` look for ec2-user as a user    
    c) `\l` look for ec2-user as a database    
7. Make a new user:    
    a) `psql` (if you already quit out of psql)    
    ## REPLACE THE [VALUES] IN THIS COMMAND! Type this with a new (short) unique password.   
    b) I recommend 4-5 characters - it doesn't have to be very secure. Remember this password!  
        `create user [some_username_here] superuser password '[some_unique_new_password_here]';`    
    c) `\q` to quit out of sql    
8. `cd` into `project2-m2-rmn9` and make a new file called `sql.env` and add `SQL_USER=` and `SQL_PASSWORD=` in it  
9. Fill in those values with the values you put in 7. b)  
  
# Seting up OAuth with Google

1. Go to https://console.developers.google.com/ and sign up using your PERSONAL google account.   
:warning: :warning: Do NOT use your NJIT account! You must use your personal account :warning: :warning:  
2. Click "CREATE PROJECT" or in the dropdown menu called "Select a Project" in the top, click "NEW PROJECT".   
3. Make a new project named cs490-lect12. "No organization" is fine.  
4. Click "Credentials" in the left hand bar, then click "+ CREATE CREDENTIALS" and then click "OAuth client ID".  
4.5. If you see a warning that says "To create an OAuth client ID, you must first set a 
    product name on the consent screen", do the following steps:  
			1. Click the "CONFIGURE CONSENT SCREEN" button.  
			2. Choose "External"  
			3. For "Application name," specify "CS490 Lect12" or something similar.  
			4. Press save.  
5. Go back to Credentials -> Create Credentials -> OAuth client ID. Click "web application".  

6. In your console run ` npm install react-google-login`
  




# Enabling read/write from SQLAlchemy  
There's a special file that you need to enable your db admin password to work for:  
1. Open the file in vim: `sudo vim /var/lib/pgsql9/data/pg_hba.conf`
If that doesn't work: `sudo vim $(psql -c "show hba_file;" | grep pg_hba.conf)`  
2. Replace all values of `ident` with `md5` in Vim: `:%s/ident/md5/g`  
3. After changing those lines, run `sudo service postgresql restart`  
4. Ensure that `sql.env` has the username/password of the superuser you created!  
5. Run your code!    
  a) `npm run watch`. If prompted to install webpack-cli, type "yes"    
  b) In a new terminal, `python app.py`    
  c) Preview Running Application (might have to clear your cache by doing a hard refresh)    
  
  
  
Technical Issues:
1. A technical issue I encountered while developing this app was using the google oauth in react.
 I had trouble getting the redirect URIs to work. After scraping stack overflow and implementing the guess and check 
 method I was able to figure out the url did not need to be the full url but only up to the .com. 
2. Another technical issue I had was getting the images to render in the the <ol> I was using for responses in the chat box. 
 Originally I returned the entire <img> tag as a message but all that did was display a line of html. To fix this I changed my messages database
 to include a who variable for each message, I added server, client, image, link. I used if statements in the react to check which type of message
 then display them as so.

What I would have liked to fix:
1. My URI when deployed to heroku does not work properly. The google tag is their but it constantly displays failed to log in. Because you are not 
  allowed to send messages unless you are logged in it ruins my app. 
2. Another thing which I wish to fix is my inline css. One of the biggest reasons I failed to complete any of this on time was because I spent atleast 
3. 8 hours trying to change my css to a stylesheet to no previal. This upsets me.