. env/bin/activate
echo '========================= Installing python3 and pip3 ==============================='
echo 'y' | apt install python3
echo 'y' | apt install python3-pip
echo 'y' | apt install pylint

echo '========================= Installing Flask and Flask-RESTful ========================'
echo 'y' | pip install Flask
echo 'y' | pip install Flask-RESTful
echo 'y' | pip install requests
echo 'y' | pip install oauth2client
echo 'y' | pip install jwt
echo 'y' | pip install azure-cosmos
