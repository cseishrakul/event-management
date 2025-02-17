from django.db.models.signals import post_save,m2m_changed,post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from events.models import Participant

@receiver(post_delete, sender=Participant)
def delete_event(sender, instance, **kwargs):
    participants = Participant.objects.filter(events=instance)
    if participants.exists():
        print(f"Deleting participants for event: {instance.name}")
        participants.delete()
        print("Deleted Successfully!")
