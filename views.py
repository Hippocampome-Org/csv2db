from django.shortcuts import render
from .forms import UploadFileForm
from .lib.map import Map

def index(request):
    return render(request, 'csv2db/index.html')

def import_all(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                Map(request).all_to_all()
                return render(request, 'csv2db/done.html')
            except KeyError:
                return render(request, 'csv2db/error.html')
        else:
            form = UploadFileForm()
    else:
        form = UploadFileForm()
    return render(request, 'csv2db/import_all.html', {'form': form})

def import_article(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                Map(request).article_to_article() # and article_to_author
                return render(request, 'csv2db/done.html')
            except KeyError:
                return render(request, 'csv2db/error.html')
        else:
            form = UploadFileForm()
    else:
        form = UploadFileForm()
    return render(request, 'csv2db/import_article.html', {'form': form})

def import_attachment(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                Map(request).attachment_to_attachment()
                return render(request, 'csv2db/done.html')
            except KeyError:
                return render(request, 'csv2db/error.html')
        else:
            form = UploadFileForm()
    else:
        form = UploadFileForm()
    return render(request, 'csv2db/import_attachment.html', {'form': form})

def import_connection(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                Map(request).connection_to_connection()
                return render(request, 'csv2db/done.html')
            except KeyError:
                return render(request, 'csv2db/error.html')
        else:
            form = UploadFileForm()
    else:
        form = UploadFileForm()
    return render(request, 'csv2db/import_connection.html', {'form': form})

def import_epdata(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                Map(request).epdata_to_epdata()
                return render(request, 'csv2db/done.html')
            except KeyError:
                return render(request, 'csv2db/error.html')
        else:
            form = UploadFileForm()
    else:
        form = UploadFileForm()
    return render(request, 'csv2db/import_epdata.html', {'form': form})

def import_fragment(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                Map(request).fragment_to_fragment()
                return render(request, 'csv2db/done.html')
            except KeyError:
                return render(request, 'csv2db/error.html')
        else:
            form = UploadFileForm()
    else:
        form = UploadFileForm()
    return render(request, 'csv2db/import_fragment.html', {'form': form})

def import_markerdata(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                Map(request).markerdata_to_markerdata()
                return render(request, 'csv2db/done.html')
            except KeyError:
                return render(request, 'csv2db/error.html')
        else:
            form = UploadFileForm()
    else:
        form = UploadFileForm()
    return render(request, 'csv2db/import_markerdata.html', {'form': form})

def import_morphdata(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                Map(request).morphdata_to_morphdata()
                return render(request, 'csv2db/done.html')
            except KeyError:
                return render(request, 'csv2db/error.html')
        else:
            form = UploadFileForm()
    else:
        form = UploadFileForm()
    return render(request, 'csv2db/import_morphdata.html', {'form': form})

def import_notes(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                Map(request).notes_to_type()
                return render(request, 'csv2db/done.html')
            except KeyError:
                return render(request, 'csv2db/error.html')
        else:
            form = UploadFileForm()
    else:
        form = UploadFileForm()
    return render(request, 'csv2db/import_notes.html', {'form': form})

def import_synonym(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                Map(request).synonym_to_synonym()
                return render(request, 'csv2db/done.html')
            except KeyError:
                return render(request, 'csv2db/error.html')
        else:
            form = UploadFileForm()
    else:
        form = UploadFileForm()
    return render(request, 'csv2db/import_synonym.html', {'form': form})

def import_term(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                Map(request).term_to_term()
                return render(request, 'csv2db/done.html')
            except KeyError:
                return render(request, 'csv2db/error.html')
        else:
            form = UploadFileForm()
    else:
        form = UploadFileForm()
    return render(request, 'csv2db/import_term.html', {'form': form})

def import_type(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                dev = 'false'
                Map(request).type_to_type(dev)
                return render(request, 'csv2db/done.html')
            except KeyError:
                return render(request, 'csv2db/error.html')
        else:
            form = UploadFileForm()
    else:
        form = UploadFileForm()
    return render(request, 'csv2db/import_type.html', {'form': form})

def import_type_dev(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                dev = 'true'
                Map(request).type_to_type(dev)
                return render(request, 'csv2db/done.html')
            except KeyError:
                return render(request, 'csv2db/error.html')
        else:
            form = UploadFileForm()
    else:
        form = UploadFileForm()
    return render(request, 'csv2db/import_type_dev.html', {'form': form})
