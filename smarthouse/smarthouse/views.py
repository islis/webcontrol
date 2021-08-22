from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from groups.models import Room


@login_required
def index(request):
    rooms = Room.objects.filter(owner=request.user)
    context = {'rooms': rooms}
    return render(request, 'base/base.html', context)
