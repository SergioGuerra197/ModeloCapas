from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def my_view(request):
   return render(
    request,
    "mi_app/index.html",
    {
        "foo": "bar",
    })
