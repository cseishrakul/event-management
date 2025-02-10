from django.shortcuts import render,redirect
from django.db.models import Q, Count, Max, Min, Avg
from django.contrib import messages
from events.forms import CategoryForm,EventForm,ParticipantForm
from events.models import Category,Event, Participant
from datetime import date
from django.db.models import Count
# Create your views here.

def index(request):
    events = Event.objects.select_related('category').prefetch_related('participants').all()
    context = {
        'events': events
    }
    return render(request, 'index.html', context)

def details(request, id):
    event = Event.objects.prefetch_related('participants').get(id=id)  # Using prefetch_related
    context = {
        'event': event,
    }
    return render(request, 'details.html', context)



def dashboard(request):
    event_data = Event.objects.aggregate(
        total_events=Count('id'),
        today_events=Count('id', filter=Q(date=date.today())),
        category_count=Count('category'),
        participant_count=Count('participants', distinct=True)  # Corrected query
    )
    
    past_events_count = Event.objects.filter(date__lt=date.today()).count()
    upcoming_events_count = Event.objects.filter(date__gt=date.today()).count()
    all_events = Event.objects.all()

    event_type = request.GET.get('type', None)
    
    if event_type == 'past':
        filtered_events = Event.objects.filter(date__lt=date.today())
    elif event_type == 'upcoming':
        filtered_events = Event.objects.filter(date__gt=date.today())
    else:
        filtered_events = all_events

    context = {
        'events': event_data['total_events'],
        'category': event_data['category_count'],
        'participant': event_data['participant_count'],
        'past_events': past_events_count,
        'upcoming_events': upcoming_events_count,
        'base_events': Event.objects.prefetch_related('category').all(),
        'today_event': Event.objects.filter(date=date.today()),
        'total_events': filtered_events
    }

    return render(request, 'dashboard/dashboard.html', context)



def show_category(request):
    categories = Category.objects.all()
    context={
        'categories':categories
    }
    return render(request,'category/all_category.html',context)


def create_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category Added Successfully')
            return redirect('show-category')
    context = {'form':form}
    return render(request,'category/create_category.html',context)


def update_category(request, id):
    category = Category.objects.get(id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category Updated Successfully')
            return redirect('show-category')
    else:
        form = CategoryForm(instance=category)
    context = {
        'form': form,
    }
    return render(request, 'category/create_category.html', context)

def delete_category(request, id):
    if request.method == 'POST':
        category = Category.objects.get(id=id)
        category.delete()
        messages.success(request, 'Category Deleted Successfully')
        return redirect('show-category')
    else:
        messages.error(request, 'Something went wrong')
        return redirect('show-category')


# Event
def show_event(request):
    events = Event.objects.all()
    context={
        'events':events
    }
    return render(request,'event/show_event.html',context)

def create_event(request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            # Save the event object
            event = form.save()

            # Handle participants
            participants_ids = request.POST.getlist('participants')  # Get selected participants
            event.participants.set(participants_ids)  # Link participants to the event
            event.save()

            # To optimize: Fetch the related category and participants in a single query
            # Using `select_related` for foreign key fields like `category`
            # Using `prefetch_related` for many-to-many relationships like `participants`
            event = Event.objects.select_related('category').prefetch_related('participants').get(id=event.id)

            # Now event object will have its related fields already populated
            messages.success(request, 'Event Added Successfully')
            return redirect('show-event')

    context = {'form': form}
    return render(request, 'event/create_event.html', context)

def update_event(request,id):
    form = Event.objects.get(id=id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=form)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event Updated Successfully')
            return redirect('show-event')
    else:
        form = EventForm(instance=form)
    context = {
        'form': form,
    }
    return render(request, 'event/create_event.html', context)

def delete_event(request, id):
    if request.method == 'POST':
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request, 'Event Deleted Successfully')
        return redirect('show-event')
    else:
        messages.error(request, 'Something went wrong')
        return redirect('show-event')
    
    
# Participant
def show_participant(request):
    participants = Participant.objects.all()
    context={
        'participants':participants
    }
    return render(request,'participant/show_participant.html',context)


def create_participant(request):
    form = ParticipantForm()
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'ParticipantForm Added Successfully')
            return redirect('show-participant')
    context={'form':form}
    return render(request,'participant/create_participant.html',context)


def update_participant(request,id):
    form = Participant.objects.get(id=id)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=form)
        if form.is_valid():
            form.save()
            messages.success(request, 'participant Updated Successfully')
            return redirect('show-participant')
    else:
        form = ParticipantForm(instance=form)
    context = {
        'form': form,
    }
    return render(request, 'participant/create_participant.html', context)

def delete_participant(request,id):
    if request.method == 'POST':
        participant = Participant.objects.get(id=id)
        participant.delete()
        messages.success(request, 'Participant Deleted Successfully')
        return redirect('show-participant')
    else:
        messages.error(request, 'Something went wrong')
        return redirect('show-participant')