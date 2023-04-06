# Storyshell miscellaneous API

# Endpoints
POST "/transcribe" - it transcribes audio and return it`s 'text', 'segments', 'language' properties using "openai/whisper"

POST "/thumbnails" - it generates thumbnails from a presentation file using "soffice" and "ImageMagick"

# Running the project
If you will use docker run "docker compose up" in the root of the project.

The server is listening - localhost:5000


IF YOU WILL NOT USE DOCKER. Execute these commands in order to install the needed packages by this repo:
1. pip install virtualenv
2. virtualenv venv
3. source venv/bin/activate
4. pip install -r requirements.txt
5. install OpenOffice and ImageMagick in order to use the presentation converter

After that you can run the server via - uvicorn main:app --reload
