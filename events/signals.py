from django.db.models.signals import post_save,m2m_changed,post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from events.models import Participant

@receiver(m2m_changed,sender=Participant.events.through)
def notify_participant_on_event_creation(sender,instance,action,**kwargs):
    if action == 'post_add':
        assigned_emails = [part.email for part in instance.participants.all()]
        send_mail(
            'New Event Organized',
            f"You are invited to the event: {instance.name}",
            "ishrak236@gmail.com",
            assigned_emails
        )

@receiver(post_delete, sender=Participant)
def delete_event(sender, instance, **kwargs):
    participants = Participant.objects.filter(events=instance)
    if participants.exists():
        print(f"Deleting participants for event: {instance.name}")
        participants.delete()
        print("Deleted Successfully!")