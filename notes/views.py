from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from user.models import User
from notes.models import Note
from django.db import models
from django.db.models import *
from time import time

# Create your views here.
def check_login(func):
    def wrapper(request,*args,**kwargs):
        if "username" in request.session and "uid" in request.session:
            return func(request,*args,**kwargs)
        username = request.COOKIES.get("username",None)
        uid = request.COOKIES.get("uid",None)
        if username and uid:
            request.session["uid"] = uid
            request.session["username"] = username
            return func(request,*args,**kwargs)
        return HttpResponseRedirect("/user/login")
    return wrapper

@check_login
def add_view(request):
    username = request.session.get("username")
    if request.method =="GET":
        return render(request,"notes/add_note.html")
    elif request.method == "POST":
        user1 = User.objects.get(username=username)
        title = request.POST.get("title")
        content = request.POST.get("content")
        note = Note.objects.create(title=title,content=content,user=user1)
        # return render(request,"notes/mod_note.html")
        return HttpResponseRedirect("/notes/mod/%s"%(note.id))

@check_login
def list_view(request):
    username = request.session.get("username")
    user = User.objects.get(username=username)
    notes = user.note_set.filter(is_active=True)
    return render(request, "notes/list_note.html", locals())

@check_login
def mod_view(request,id):
    username = request.session.get("username")
    if request.method == "GET":
        try:
            user = User.objects.get(username=username)
            note = Note.objects.get(id=id)
            return render(request, "notes/mod_note.html",locals())
        except:
            return HttpResponseRedirect("/notes/")
    elif request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        # note = Note.objects.filter(id=id)
        note = Note.objects.get(id=id)
        note.title=title
        note.content=content
        note.updated_time=time()
        note.save()
        # note.update(title=title, content=content, updated_time=time())
        # return render(request,"notes/mod_note.html")
        return HttpResponseRedirect("/notes/mod/%s" % (note.id))

@check_login
def del_view(request,id):
    username = request.session.get("username")
    user = User.objects.get(username=username)
    try:
        note = user.note_set.filter(id=id)
        note.update(is_active=False)
        # note.is_active = False
        # note.save()
    except:
        return HttpResponseRedirect("/notes/")

@check_login
def show_view(request,id):
    try:
        note = Note.objects.get(id=id)
        return render(request,"notes/show.html",locals())
    except:
        return HttpResponseRedirect("/notes/")
