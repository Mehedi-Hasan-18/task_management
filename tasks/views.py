from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm,TaskModelFormPrac
from tasks.models import Employee,Task,TaskDetail,Project
from django.db.models import Q,Count

# Create your views here.
    #Work with database
    # Transform data
    # Data pass
    # Http response / Json response
# def home(request):
#     return HttpResponse("Welcome to the task management")
    
# def contact(recquest):
#     return HttpResponse("This is Contact page")

# def show_details(request):
#     return HttpResponse("This is Show Details section")

# def show_specific_task(request,id):
#     return HttpResponse("This is Show Specific Task section")

# ----------------------------------------------------RIGHT WAY TO WRITE THE CODE-----------------------------------------
def dash_board(request):
    return render(request,"dashboard/manager_dashboard.html")

def test(request):
    context = {
        "names":["Mahmud"]
    }
    return render(request,"test.html",context)

def create_task(request):
    form = TaskModelForm()
    if(request.method == 'POST'):
        form = TaskModelForm(request.POST)
        if form.is_valid():
            """ For Model Form Data"""
            form.save()
            
            return render(request,'task_form.html',{'form':form,"message":"Text Added Successfull"})
                
    context = {"form": form}
    return render(request,"task_form.html",context)

def view_task(request):
    #RETRIVE ALL DATA
    # tasks = Task.objects.all()
    
    #RETRIVE A SPECIFIC DATA
    # task_1 = Task.objects.get(id=1)
    
    #----------FILTER----------#
    # tasks = Task.objects.filter(status='PENDING')
    # tasks = Task.objects.exclude(status = 'DONE')
    
    #-----SHOW THE TASK THAT CONTAIN "Paper"
    # tasks = Task.objects.filter(title__icontains='c',status='PENDING')
    
    #--------------SHOW TASK WITH OR ------------
    # tasks = Task.objects.filter(Q(status="PENDING") | Q(status = 'IN_PROGRESS'))
    
    # ----------------Select_related(Foreignkey,OneToOneField)---------
    # tasks = Task.objects.select_related('details').all()
    # tasks = TaskDetail.objects.select_related('task').all()
    tasks = Task.objects.select_related("project").all()
    
    
    # ------------prefetch_related(reverse Forigkey, manyTomany)------------
    # tasks = Project.objects.prefetch_related('task_set').all()
    # tasks = Task.objects.prefetch_related("assign_to").all()
    
    # ----------AGGREGATE----------
    # task_count = Task.objects.aggregate(num_task=Count('id'))
    
    projects = Project.objects.annotate(num_task=Count('task')).order_by('num_task')
    return render(request,'show_task.html',{'projects':projects})
    # return render(request,'show_task.html',{'tasks':tasks})






#PRACTICE
# def create_task_prac(request):
#     form = TaskModelFormPrac()
#     if(request.method=='POST'):
#         form = TaskModelFormPrac(request.POST)
#         if form.is_valid():
#             form.save()
            
#             return render(request,'task_form_prac.html',{'form':form,'message':'Task Added Succefully'})
            
#     return render(request,'task_form_prac.html',{'form':form})