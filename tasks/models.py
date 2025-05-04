from django.db import models
from django.db.models.signals import post_save,pre_save,post_delete,pre_delete
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.core.mail import send_mail


class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.name
# Create your models here.
class Task(models.Model):
    STATUS_CHOICES=[
        ('PENDING','Pending'),
        ('IN_PROGRESS','In Progress'),
        ('COMPLETED','Completed')
    ]
    project = models.ForeignKey("Project",on_delete=models.CASCADE,default=1)
    
    assign_to = models.ManyToManyField(Employee,related_name="tasks")
    
    title = models.CharField(max_length=250)
    discription = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=15,choices=STATUS_CHOICES,default="PENDING")
    is_complete = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.title
    

class TaskDetail(models.Model):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    PRIORITY_OPTIONS = (
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low'),
    )
    task = models.OneToOneField(
        Task, 
        on_delete=models.CASCADE,
        related_name='details'
    )
    assign_to = models.CharField(max_length=100)
    priority = models.CharField(
        max_length=1, choices=PRIORITY_OPTIONS, default=LOW)
    notes = models.TextField(blank=True,null=True)
    
    def __str__(self):
        return f'Details For Task {self.task.title}'
    
class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    start_date = models.DateField()
    
    def __str__(self):
        return self.name
    
   
   
#SIGNALS 
# @receiver(post_save,sender=Task)
# def notify(sender,instance,created,**kwargs):
#     print(sender)
#     print(instance)
#     print(kwargs)
#     print(created)
#     if created:
#         instance.is_complete = True
#         instance.save()
        
# @receiver(pre_save,sender=Task)
# def notify(sender,instance,**kwargs):
#     print(sender)
#     print(instance)
#     print(kwargs)
#     instance.is_complete = True

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