In this project we are accessing Vimeo API to get all categories and users for each category(directly we can't get users)
and details of each user were stored in MySql Database until user count reaches 5000(can be altered in settings -SEARCH_USERS_TOTAL).
And a search feature was in place to search the users present in DB and can be filtered using filters available. The results of
search were cached for a small time(Default:5min can be altered in settings -SEARCH_CACHE_TIME) to decrease no.of DB hits for
similar queries.



## Inclusions
* Django 1.4.2
* python-memcached - For Caching backend
* simplejson 2.6.1
* distribute 0.6.28
* mysql-python - For mysql Db connection
* requests 0.14.0 - For accessing Vimeo API



## Project Setup
Steps:-
* Download the project codebase
* In Terminal change path to project (cd ~/Desktop/App is App is in Desktop)
* Run the following command to install requirements
    ```
    pip install -R requirements.txt #(if pip was not installed then - sudo apt-get install pip)
    ```
* Create a Database on your mysql server
* Open settings.py an update the following Database settings

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'DB NAME',                      # Or path to database file if using sqlite3.
            'USER': 'MYSQL USERNAME',                      # Not used with sqlite3.
            'PASSWORD': '',                  # Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    }
    ```
* Now the following command to create schema
    ```
    python manage.py syncdb
    ```



## Running Script to crawl Vimeo users

After the project setup do the following steps. To fetch all users(i.e 5000) it will take time(3Hrs approx) because to get
Uploaded Video status Vimeo API call should be done for each and every user. So if Uploaded video status was not needed or
to execute the script fast 'UPLOADED_VIDEO_STATUS' setting in settings.py file can be set to False(Default: True), then
uploaded video status for all users will be False


Steps:-
* python manage.py shell
    (Note: '>>>' indicates these commands should be run on python shell)
* >>> from project.utils import *
* >>> get_vimeo_categories()



## Running Application	
    python manage.py runserver


## Searching Users

* abc                     all users whose name contains abc
* ^abc                    all users whose name starts with abc
* =abc                    all users whose name is equal to abc
