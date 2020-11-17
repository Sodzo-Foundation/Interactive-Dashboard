from django.shortcuts import render
import datetime

def index(request):
    today = datetime.datetime.now()
    now = today.strftime("%m/%d/%Y, %H:%M %p")
    return render(request, 'index.html', {'now': now })
