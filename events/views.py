from django.shortcuts import render,redirect
from django.db.models import Q, Count, Max, Min, Avg
from django.contrib import messages
from events.forms import CategoryForm,EventForm,ParticipantForm
from events.models import Category,Event, Participant
from datetime import date

# Create your views here.

def index(request):
    events = Event.objects.all()
    context={
        'events':events
    }
    return render(request,'index.html',context)

def details(request,id):
    events = Event.objects.get(id=id)
    context={
        'events':events
    }
    return render(request,'details.html',context)

def dashboard(request):
    
    base_event = Event.objects.all()
    events = base_event.count()
    today_event = Event.objects.filter(date=date.today())
    category = Category.objects.all().count()
    participant = Participant.objects.all().count()
    context={
        'events':events,
        'category':category,
        'participant':participant,
        'base_events':base_event,
        'today_event':today_event
    }
    return render(request,'dashboard/dashboard.html',context)


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
            form.save()
            messages.success(request, 'Event Added Successfully')
            return redirect('show-event')
    context={'form':form}
    return render(request,'event/create_event.html',context)

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