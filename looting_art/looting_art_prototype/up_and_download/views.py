from django.http import HttpResponse, Http404
from django.shortcuts import render
import os
from django.conf import settings
import csv

from .forms import UploadFileForm

import up_and_download.scripts.counting as flagging

import subprocess

column = ''

def flag(file, col):
    cmd = 'python3 ./up_and_download/scripts/counting.py ' + file + ' looting_art_prototype/output_flagged.csv '
    subprocess.call(cmd, shell=True)

def returnDownload(file, col):
    with open('output_test.csv', 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    flag('output_test.csv', col)
    

# Index.html
def index(request):
    return render(request, 'index.html')

# Upload file and give column to check/flag
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            column = request.POST.get('column')
            returnDownload(request.FILES['testCSV'], column)

            path = 'looting_art_prototype/output_flagged.csv'
            file_path = os.path.join(settings.BASE_DIR, path)
            if os.path.exists(file_path):
                with open(file_path, 'r') as fh:
                    response = HttpResponse(fh.read(), content_type="text/csv")
                    response['Content-Disposition'] = 'attachment; filename=test.csv'
                    return response
            raise Http404
    else:
        return HttpResponse('ERROR: somethong went wrong...')

