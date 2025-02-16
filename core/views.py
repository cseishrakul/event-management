from django.shortcuts import render
from events.models import Event

# Create your views here.
def index(request):
    events = Event.objects.select_related('category').prefetch_related('participants').all()
    context = {
        'events': events
    }
    return render(request, 'index.html', context)

def no_permission(request):
    return render(request,'no_permission.html')