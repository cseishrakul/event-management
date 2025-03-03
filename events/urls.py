from django.urls import path
from events.views import  update_category,delete_category,update_event,delete_event,create_participant,show_participant,update_participant,delete_participant,CategoryListView,CreateCategoryView,ShowEventView,CreateEventView

urlpatterns = [
    # Category
    path('show-category/',CategoryListView.as_view(),name='show-category'),
    path('create-category/',CreateCategoryView.as_view(),name='create-category'),
    path('update-category/<int:id>/', update_category, name='update-category'),
    path('delete-category/<int:id>/', delete_category, name='delete-category'),
    
    # Event
    # path('create-event/', create_event, name='create-event'),
    path('create-event/', CreateEventView.as_view(), name='create-event'),
    path('show-event/', ShowEventView.as_view(), name='show-event'),
    path('update-event/<int:id>/', update_event, name='update-event'),
    path('delete-event/<int:id>/', delete_event, name='delete-event'),
    
    # Participant
    path('create-participant/', create_participant, name='create-participant'),
    path('show-participant/', show_participant, name='show-participant'),
    path('update-participant/<int:id>/', update_participant, name='update-participant'),
    path('delete-participant/<int:id>/', delete_participant, name='delete-participant'),
]
