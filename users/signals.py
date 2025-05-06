from django.db.models.signals import post_save,pre_save,post_delete,pre_delete
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.contrib.auth.models import User,Group
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save,sender=User)
def user_activation_email(sender,instance,created,**kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}"
        
        subject = 'Activate Your Account'
        message = f'Click This Link To Activate The Account : {activation_url}'
        recipent_list = [instance.email]
        
        try:
             send_mail(subject,message,settings.EMAIL_HOST_USER,recipent_list)
        except Exception as e :
            print(f'Fail to send the email to {instance.email}:{str(e)}')
            
@receiver(post_save,sender=User)
def assign_task(sender,instance,created,**kwargs):
    if created:
        user_group,created = Group.objects.get_or_create(name="User Group")
        instance.groups.add(user_group)
        instance.save()
        