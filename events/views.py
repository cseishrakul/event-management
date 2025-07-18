from django.shortcuts import render,redirect
from django.db.models import Q, Count
from django.contrib import messages
from events.forms import CategoryForm,EventForm,ParticipantForm
from events.models import Category,Event, Participant
from datetime import date
from django.db.models import Count
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from users.views import is_admin
from django.views.generic import ListView,CreateView
from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

# Organizer test
def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()
def is_participant(user):
    return user.groups.filter(name='Participant').exists()
def is_admin_or_organizer(user):
    return user.is_superuser or user.groups.filter(name='Organizer').exists()


# Create your views here.
def details(request, id):
    event = get_object_or_404(Event, id=id)
    related_events = Event.objects.filter(category=event.category).exclude(id=event.id)

    return render(request, 'details.html', {
        'event': event,
        'related_events': related_events,
    })
    
def all_events(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})


@user_passes_test(is_admin,login_url='no-permission')
def admin_dashboard(request):
    event_data = Event.objects.aggregate(
        total_events=Count('id'),
        today_events=Count('id', filter=Q(date=date.today())),
        category_count=Count('category'),
        participant_count=Count('participants', distinct=True)
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

# Class based view of show category

@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(user_passes_test(is_admin_or_organizer, login_url='no-permission'), name='dispatch')
class CategoryListView(ListView):
    model = Category
    template_name = 'category/all_category.html'
    context_object_name = 'categories'

@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(user_passes_test(is_admin_or_organizer, login_url='no-permission'), name='dispatch')
class CreateCategoryView(LoginRequiredMixin,CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/create_category.html'
    success_url = reverse_lazy('show-category')
    
    def form_valid(self, form):
        messages.success(self.request,'Category Added Successfully!')
        return super().form_valid(form)





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


# Event class based view

class ShowEventView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    model = Event
    template_name = 'event/show_event.html'
    context_object_name = 'events'
    permission_required = 'events.view_event'
    login_url = 'no-permission'

class CreateEventView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = Event
    form_class = EventForm
    template_name = 'event/create_event.html'
    permission_required = 'events.add_event'
    login_url = 'no-permission'
    success_url = reverse_lazy('show-event')
    
    def form_valid(self,form):
        event = form.save()
        participants_ids = self.request.POST.getlist('participants')
        event.participants.set(participants_ids)
        event.save()
        event = Event.objects.select_related('category').prefetch_related('participants').get(id=event.id)
        messages.success(self.request,'Event Added Successfully!')
        
        return super().form_valid(form)


@login_required
@permission_required('events.change_event',login_url='no-permission')
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

@login_required
@permission_required('events.delete_event',login_url='no-permission')
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
@login_required
@permission_required('events.view_participant',login_url='no-permission')
def show_participant(request):
    participants = Participant.objects.all()
    context={
        'participants':participants
    }
    return render(request,'participant/show_participant.html',context)

@login_required
@permission_required('events.add_participant',login_url='no-permission')
def create_participant(request):
    form = ParticipantForm()
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'ParticipantForm Added Successfully')
            return redirect('create-participant')
    context={'form':form}
    return render(request,'participant/create_participant.html',context)


@login_required
@permission_required('events.change_participant',login_url='no-permission')
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

@login_required
@permission_required('events.delete_participant', login_url='no-permission')
def delete_participant(request, id):
    try:
        participant = Participant.objects.get(id=id)
        participant.events.clear()
        participant.delete()
        messages.success(request, 'Participant Deleted Successfully')
        return redirect('show-participant')
    except Participant.DoesNotExist:
        messages.error(request, 'Participant not found')
        return redirect('show-participant')
    except Exception as e:
        messages.error(request, f"Something went wrong: {e}")
        return redirect('show-participant')
    
@login_required
def dashboard(request):
    if is_organizer(request.user):
        return redirect('organizer-dashboard')
    elif is_participant(request.user):
        return redirect('participant-dashboard')
    elif is_admin(request.user):
        return redirect('admin-dashboard')
    
    return redirect('no-permission')