from django.db import models


# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=250)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='event_tasks',blank=True,null=True,default='event_tasks/default.jpg')
    
    def __str__(self):
        return self.name

    def get_participants(self):
        return self.participants.all()


class Participant(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField()
    events = models.ManyToManyField(Event, related_name='participants')
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    def __str__(self):
        return self.name
    


