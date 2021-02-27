# ReddQuery

ReddQuery( reddquery.herokuapp.com) is a web application that able to make some queries on Reddit for special keywords which are given by user. System is created on Django framework by using Python. PostgreSQL is used as a database. Docker is used in order to deploy the project. Project is deployed to Heroku. JavaScript, CSS and HTML5 are used for developing the UI. Git is used as a version control system.
System consists of following functions.

•	Make new query on reddit submissions and get comments of the submissions
•	Save the query data to database
•	Retrieve the data which collected before
•	Delete the data which saved before
•	Reddit api function
•	Scatter plot function
•	Word cloud function
•	Sentiment score function
•	Data cleaning function

## SYSTEM MANUAL

In order to run this system on local server, following programs must be installed.

•	Python 3.9

•	Django 3.1.4

•	JavaScript

•	CSS

•	HTML

•	Python Reddit Api Wrapper

•	Gunicorn

•	Psycopg2

•	Praw

•	Requests

•	Wordcloud

•	Matplotlib

•	Textblob

•	Pandas

•	Regex

•	Pip

•	Virtual environment 

After the program installation and virtual environment creation and activation, ReddQuery can be download to local. Following commands should write to terminal respectively.

•	git clone https://github.com/mfbehlul/ReddQuery.git

•	cd swe573

•	pipenv install requirements.txt

•	python manage.py makemigrations

•	python manage.py migrate

•	python manage.py runserver


In order to use python reddit api, following informations should be given to the function.

  reddit = praw.Reddit(
        client_id='',
        client_secret='',
        user_agent=''
    )

In order to integrate the database to the system, following informations should be given to the function.

conn = psycopg2.connect(
        database="",
        user="",
        password="",
        host="",
        port=""
    )




## USER MANUAL
ReddQuery is a web application that able to make some queries on Reddit for special keywords which is given by user.

### LOGIN AND REGISTER 
Users are redirecting to login page when they enter to website. After registering to system, users can login to the system.


### HOME PAGE


Home page consists of following elements:
•	Navbar
•	Sidebar
•	Search form
	Side bar consists of three different sub-part. Those are Queries, Analysis and Pages



## QUERY

Users can make a query on any subreddit and examine the results of the query on analysis part. A warning message is displayed under the search button when query process is completed.



## ANALYSIS

### SENTIMENT ANALYSIS

In the sentiment analysis, there are two values that give information about distribution of the comments by polarity and subjectivity.
Subjectivity value gives information either the user comments are common public opinion or personal opinion. Subjectivity value lies in the range of [0,1]
Polarity value lies in the range of [-1,1] and 1 stands for positive statement whereas -1 stands for negative statement.



### WORD CLOUD

Word cloud is an image that consists of different sized words. Size of the words determine via recurrence of the words. Users can understand easily most used words in the subreddit which they queried. In this example we can see the vaccine, variant, moderna ..etc.
are most used words in covid19 subreddit.


### DATA TABLE

User can examine the all data in data table part. Data table consists of following columns.

•	Comments

•	Subjectivity score

•	Sentiment Result

•	Author

•	Subreddit

•	Created time of comment

-User can change number of showing entries.

-User can sort the data table by clicking the up down arrows in the column.

-User can see total number of the comment data on the bottom of the table.

-In order to collect the data python reddit api and praw library is used.

-After data collected from api, cleaning process is started. Cleaning process consists of following stages.

•	Removing the stop words

•	Cleaning the data by using regular expression library (regex)

•	Applying sentiment analysis function (textblob)

-Reddit function is used for fetching comment data from Reddit.

-saveTheQuery function is used for saving comment data to database.

-fetchTheQuery function is used for fetching data from database

 

## SAVING THE QUERY TO DATABASE
Users can save their query to database via clicking the button which is above on the data table. After clicking that button, information message is displayed on the page.

 
## RETRIEVE THE SAVING QUERY
In order to reach saved data, user should go to My Saved Query page. On this page users can select the data which they want to retrieve. After clicking Retrieve the Query button, information message is displayed on the page.
Users should visit analysis sub-part on the side bar in order to see analysis of the retrieved data.


## DELETE THE SAVING QUERY
In order to delete saved query, user should go to Delete Saved Query page. On this page users can delete the query which is saved to database before. After clicking Delete the Query button, an information message is displayed on the page.

 
