from django.urls import path
from events.views import create_category, update_category,show_category,delete_category,create_event,show_event,update_event,delete_event,create_participant,show_participant,update_participant,delete_participant

urlpatterns = [
    # Category
    path('show-category/',show_category,name='show-category'),
    path('create-category/',create_category,name='create-category'),
    path('update-category/<int:id>/', update_category, name='update-category'),
    path('delete-category/<int:id>/', delete_category, name='delete-category'),
    
    # Event
    path('create-event/', create_event, name='create-event'),
    path('show-event/', show_event, name='show-event'),
    path('update-event/<int:id>/', update_event, name='update-event'),
    path('delete-event/<int:id>/', delete_event, name='delete-event'),
    
    # Participant
    path('create-participant/', create_participant, name='create-participant'),
    path('show-participant/', show_participant, name='show-participant'),
    path('update-participant/<int:id>/', update_participant, name='update-participant'),
    path('delete-participant/<int:id>/', delete_participant, name='delete-participant'),
]
