from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Task(models.Model):
    STATUS_CHOICES=[
        ('PENDING','Pending'),
        ('IN_PROGRESS','In Progress'),
        ('COMPLETED','Completed')
    ]
    project = models.ForeignKey("Project",on_delete=models.CASCADE,default=1)
    
    # assign_to = models.ManyToManyField(Employee,related_name="tasks")
    assign_to = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name="tasks")
    
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
    # assign_to = models.CharField(max_length=100)
    image = models.ImageField(upload_to='task_details', blank=True, null=True, default='task_details/download.png') #the name should be task_asset
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
    
   
   
