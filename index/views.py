from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def index_view(request):
    login=True
    username = request.session.get("username", None)
    uid = request.session.get("uid", None)
    if (not username) and (not uid):
        username = request.COOKIES.get("username", None)
        uid = request.COOKIES.get("uid", None)
        if (not username) and (not uid):
            login=False

    return render(request,"index/index.html",locals())