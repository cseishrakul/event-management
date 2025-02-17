from django.db.models.signals import post_save,m2m_changed,post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from events.models import Participant

<<<<<<< HEAD
@receiver(m2m_changed, sender=Participant.events.through)
def notify_participant_on_event_creation(sender, instance, action, **kwargs):
    if action == 'post_add':
        assigned_emails = [participant.email for participant in instance.participants.all()]
        send_mail(
            'New Event Organized',
            f"You are invited to the event: {instance.name}",
            "ishrak236@gmail.com",
            assigned_emails
        )
=======
# @receiver(m2m_changed, sender=Participant.events.through)
# def notify_participant_on_event_creation(sender, instance, action, **kwargs):
#     if action == 'post_add':
#         assigned_emails = [instance.email]  # Get email from the participant instance
#         event_names = ", ".join(event.name for event in instance.events.all())  # Get event names
#         send_mail(
#             'New Event Organized',
#             f"You are invited to the event(s): {event_names}",
#             "ishrak236@gmail.com",
#             assigned_emails
#         )
>>>>>>> assignment-2


@receiver(post_delete, sender=Participant)
def delete_event(sender, instance, **kwargs):
    participants = Participant.objects.filter(events=instance)
    if participants.exists():
        print(f"Deleting participants for event: {instance.name}")
        participants.delete()
        print("Deleted Successfully!")
