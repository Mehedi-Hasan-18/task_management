from django.db.models.signals import post_save,pre_save,post_delete,pre_delete
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.core.mail import send_mail
from tasks.models import Task


# SIGNALS 
@receiver(post_save,sender=Task)
def notify(sender,instance,created,**kwargs):
    if created:
        instance.is_complete = True
        instance.save()
        
@receiver(pre_save,sender=Task)
def notify(sender,instance,**kwargs):
    print(sender)
    print(instance)
    print(kwargs)
    instance.is_complete = True

@receiver(m2m_changed,sender=Task.assign_to.through)
def notify_employee(sender,instance,action,**kwargs):
    if action == 'post_add':
        assigned_email = [emp.email for emp in instance.assign_to.all()]
        print(assigned_email)
        
        send_mail(
        "New Task Assign",
        "You are Added to a new Task ",
        "mdmehedihasanroby@gmail.com",
        assigned_email,
    )
        
@receiver(pre_delete,sender=Task)
def delete_task(sender,instance,**kwargs):
    if instance.details:
        instance.details.delete()
        print("Delete Successful")