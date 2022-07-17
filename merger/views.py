import imp
from django.shortcuts import render
from django.http import HttpResponse

from .forms import PDF
from pdfrw import PdfReader, PdfWriter
import os
from django.conf import settings
import shortuuid


def merger(inputs, output):
    o = open(settings.MEDIA_URL + output, "wb+")
    writer = PdfWriter()
    for inpfn in inputs:
        writer.addpages(PdfReader(settings.MEDIA_URL + inpfn).pages)
    writer.write(o.name)
    o.close()
    return o


# http://127.0.0.1:8000/media/profile_pics/580b57fcd9996e24bc43c325.png
def handle_uploaded_file(f, id):
    with open(settings.MEDIA_URL + id, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def index(request):
    if request.method == "POST":
        # pdf = PDF(request.POST, request.FILES)
        # if pdf.is_valid():
        # f1 = request.FILES["file1"]
        # f2 = request.FILES["file2"]
        # id1 = shortuuid.uuid() + ".pdf"
        # id2 = shortuuid.uuid() + ".pdf"
        # handle_uploaded_file(f1, id1)
        # handle_uploaded_file(f2, id2)
        # out = merger([id1, id2], output)
        
        lastFileNo = int(request.POST.get('lastFileNo'))
        allIds = []
        for i in range(1, lastFileNo+1):
            fileId = 'file'+str(i)
            if(fileId in request.FILES.keys()):
                file = request.FILES[fileId]
                id = shortuuid.uuid() + ".pdf"
                handle_uploaded_file(file, id)
                allIds.append(id)
        output = shortuuid.uuid() + ".pdf"        
        out = merger(allIds, output)
        return render(request, "merger/index.html", {"out": out.name})
    else:
        # pdf = PDF()
        out = ""
        return render(request, "merger/index.html", { "out": out})
