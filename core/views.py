from django.shortcuts import render
from events.models import Event

# Create your views here.
def index(request):
    all_events = Event.objects.select_related('category').prefetch_related('participants').order_by('-date')
    latest_events = all_events[:3]
    show_all_button = all_events.count() > 3

    context = {
        'events': latest_events,
        'show_all_button': show_all_button,
    }
    return render(request, 'index.html', context)

def aboutPage(request):
    return render(request,'about.html')

def blogPage(request):
    return render(request,'blog.html')
def contactPage(request):
    return render(request,'contact.html')

def no_permission(request):
    return render(request,'no_permission.html')