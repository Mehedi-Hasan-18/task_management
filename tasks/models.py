from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
# Create your models here.
class Task(models.Model):
    project = models.ForeignKey("Project",on_delete=models.CASCADE,default=1)
    
    assign_to = models.ManyToManyField(Employee,related_name="tasks")
    
    title = models.CharField(max_length=250)
    discription = models.TextField()
    due_date = models.DateField()
    is_complete = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    

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
    priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS, default=LOW)
    
class Project(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField()