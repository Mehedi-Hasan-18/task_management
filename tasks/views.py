from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm,TaskModelFormPrac
from tasks.models import Employee,Task

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
    # employees = Employee.objects.all()
    form = TaskModelForm()
    if(request.method == 'POST'):
        form = TaskModelForm(request.POST)
        if form.is_valid():
            """ For Model Form Data"""
            form.save()
            
            return render(request,'task_form.html',{'form':form,"message":"Text Added Successfull"})
            
            """For Django Form Data"""
            # data = form.cleaned_data
            # title = data.get('title')
            # discription = data.get('discription')
            # due_date = data.get('due_date')
            # assign_to = data.get('assign_to')
            
            # task = Task.objects.create(title=title,discription=discription,due_date=due_date)
            
            # # ASSIGN EMPLOYEE TO TASKS
            # for emp_id in assign_to:
            #     employee = Employee.objects.get(id=emp_id)
            #     task.assign_to.add(employee)
                
    context = {"form": form}
    return render(request,"task_form.html",context)

#PRACTICE
def create_task_prac(request):
    form = TaskModelFormPrac()
    if(request.method=='POST'):
        form = TaskModelFormPrac(request.POST)
        if form.is_valid():
            form.save()
            
            return render(request,'task_form_prac.html',{'form':form,'message':'Task Added Succefully'})
            
    return render(request,'task_form_prac.html',{'form':form})