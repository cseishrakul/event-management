from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User,Group
from users.forms import CustomRegistrationForm,LoginForm,AssignRoleForm,CreateGroupForm
from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import Prefetch
from events.models import Event,Category


# Test for users
def is_admin(user):
    return user.groups.filter(name = 'Admin').exists()
def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()
def is_participant(user):
    return user.groups.filter(name='Participant').exists()


# Create your views here.
def sign_up(request):
    form = CustomRegistrationForm()
    if request.method == 'POST':
        form=CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.is_active = False
            user.save()
            messages.success(request, 'A confirmation mail sent. Please check your email!')
            return redirect('sign-in')
        else:
            print("Form is not valid")
    return render(request,'registrations/register.html',{'form':form})

def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('home')
    return render(request,'registrations/login.html',{'form':form})
    
@login_required
def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')
    
def activate_user(request,user_id,token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user,token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid ID or Token!')
    except User.DoesNotExist:
        return HttpResponse('User not Found!')

@user_passes_test(is_admin,login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.prefetch_related(
            Prefetch('groups',queryset=Group.objects.all(),to_attr='all_groups')
        ).all()
    for user in users:
        if user.all_groups:
            user.groups_name = user.all_groups[0].name
        else:
            user.groups_name = 'No Group Assigned!'
    return render(request,'admin/dashboard.html',{'users':users})

@user_passes_test(is_admin,login_url='no-permission')
def assign_role(request,user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()
    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request,f'User {user.username} has been assigned to the {role.name} role')
            return redirect('admin-dashboard')
        
    return render(request,'admin/assign_role.html',{'form':form})

@user_passes_test(is_admin,login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request,f"Group {group.name} has been created successfully!")
            return redirect('create-group')
    return render(request,'admin/create-group.html',{'form':form})

@user_passes_test(is_admin,login_url='no-permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request,'admin/group_list.html',{'groups':groups})

@login_required
def dashboard(request):
    if is_organizer(request.user):
        return redirect('organizer-dashboard')
    elif is_participant(request.user):
        return redirect('participant-dashboard')
    elif is_admin(request.user):
        return redirect('admin-dashboard')
    
    return redirect('no-permission')


@login_required
@user_passes_test(is_organizer,login_url='no-permission')
def organizer_dashboard(request):
    events = Event.objects.all()
    categories = Category.objects.all()
    context={
        'events':events,
        'categories':categories
    }
    return render(request,'admin/organizer_dashboard.html',context)

@login_required
@user_passes_test(is_participant,login_url='no-permission')
def participant_dashboard(request):
    events = Event.objects.all()
    context={
        'events':events
    }
    return render(request,'admin/participant_dashboard.html',context)