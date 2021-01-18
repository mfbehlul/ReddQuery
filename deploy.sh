# build our heroku-ready local Docker image
docker build -t reddquery-dockerized -f Dockerfile .


# push your directory container for the web process to heroku
heroku container:push web -a reddquery


# promote the web process with your container 
heroku container:release web -a reddquery


# run migrations
heroku run python3 manage.py migrate -a reddquery
