If you will use docker perform the steps listed below:
1. docker build -t storyshell-miscellaneous-api (to build the docker image)
2. docker run --rm -p 5000:5000 storyshell-miscellaneous-api (to run the docker container using the image above)

The server is listening - localhost:5000


IF YOU WILL NOT USE DOCKER. Execute these commands in order to install the needed packages by this repo:
1. pip install virtualenv
2. virtualenv venv
3. source venv/bin/activate
4. pip install -r requirements.txt
5. install OpenOffice and ImageMagick in order to use the presentation converter

After that you can run the server via - uvicorn main:app --reload
