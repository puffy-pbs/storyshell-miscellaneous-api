Preliminary steps. Execute these commands in order to install the needed packages by this repo:
1. pip install virtualenv
2. virtualenv venv
3. source venv/bin/activate
4. pip install -r requirements.txt
5. install OpenOffice and ImageMagick in order to use the presentation converter

After that you can run the server via - uvicorn main:app --reload
