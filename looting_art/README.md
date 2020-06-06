# GLAMhack2020 Django Prototype
This is a prototype written in Django to upload a csv-file and give the name of the column to do the provenance-flagging.
As output, a flagged csv file is provided to download.

## How to use it
Run 
```
pip install -r requirements.txt
```
Then
```
cd looting_art_prototype 
```
Then
```
python3 manage.py runserver
```

Go to http://127.0.0.1:8000/ to tests it locally.

## Pitfalls and warning
There are no input/security checks done, so do not use it in productive more just yet.
It currently uses the counting.py file from another project (in parent folder), so if that is updated, you have to copy paste the code in this prototype and wother case adapt the code...

## Frontend (so far)
![Alt text](/looting_art/screenshot.jpg?raw=true)