from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import User
import hashlib
from time import sleep
# from django.db import *


# Create your views here.
def reg_view(request):
    if request.method == "GET":
        return render(request,"user/register.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        password_1 = request.POST.get("password_1")
        password_2 = request.POST.get("password_2")

        if not username or not password_1 or not password_2:
            response_user ="Please give me username"
            return render(request, "user/register.html", locals())
        for ch in username:
        #     if 0x4e00 <= ch <= 0x9fff:
            if ord(ch) > 255:
                response_user = "The username contains chinese"
                return render(request, "user/register.html", locals())

        older_users = User.objects.filter(username=username)
        if older_users:
            response_user = "The username is already existed"
            return render(request,"user/register.html",locals())
        if password_1 !=password_2:
            response_pwd = "两次密码不一致"
            return render(request, "user/register.html", locals())

        #密码处理：hash算法
        m = hashlib.md5()
        m.update(password_1.encode())
        password_h = m.hexdigest()
        try:
            user = User.objects.create(username=username,password=password_h)
        except Exception as e:
            print(e)
            response_user="The username is aleady existed"
            return render(request, "user/register.html", locals())

    return HttpResponseRedirect("/index")

def login_view(request):
    if request.method == "GET":
        if "username" in request.session and "uid" in request.session:

            # return HttpResponse("---您已登录---")
            return HttpResponseRedirect("/index")
        username = request.COOKIES.get("username",None)
        uid = request.COOKIES.get("uid",None)
        if username and uid:
            request.session["uid"] = uid
            request.session["username"] = username
            # return HttpResponse("---您已登录---")
            return HttpResponseRedirect("/index")

        return render(request,"user/login.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        remember = request.POST.get("remember")
        try:
            older_user = User.objects.get(username=username)
        except Exception as e:
            response_log = "用户名或密码错误"
            return render(request,"user/login.html",locals())
        m= hashlib.md5()
        m.update(password.encode())
        password_h = m.hexdigest()
        if password_h != older_user.password:
            response_log = "用户名或密码错误"
            return render(request, "user/login.html", locals())
        request.session["uid"] = older_user.id
        request.session["username"] = older_user.username

        # print("-----------------------------------")
        # print(remember)

        resp = HttpResponseRedirect("/index")
        if remember:
            resp.set_cookie("username",username,3600*24*15)
            resp.set_cookie("uid",older_user.id,3600*24*15)

        return resp


def logout_view(request):
    # username = request.COOKIES.get("username", None)
    # uid = request.COOKIES.get("uid", None)

    # try:
    #     del request.session["username"]
    #     del request.session["uid"]
    # except:
    #     pass
    request.session.flush()

    resp = HttpResponseRedirect("/index")
    resp.delete_cookie("username")
    resp.delete_cookie("uid")

    # return HttpResponseRedirect("/index")
    # return HttpResponseRedirect("/user/login")
    return resp