from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm,TaskModelFormPrac,TaskDetailModelForm
from tasks.models import Employee,Task,TaskDetail,Project
from django.db.models import Q,Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required

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
def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def is_employee(user):
    return user.groups.filter(name='Employee').exists()

def dash_board(request):
    type = request.GET.get('type','all')
    #GETTING TASK COUNT
    # total_task = tasks.count()
    # completed_task = Task.objects.filter(status='COMPLETED').count()
    # in_progress = Task.objects.filter(status='IN_PROGRESS').count()
    # pending_task = Task.objects.filter(status="PENDING").count()
    # tasks = Task.objects.select_related('details').prefetch_related('assign_to')
    
    counts = Task.objects.aggregate(
        total_task = Count('id'),
        completed_task = Count('id',filter=Q(status='COMPLETED')),
        in_progress = Count('id',filter=Q(status='IN_PROGRESS')),
        pending_task = Count('id',filter=Q(status='PENDING'))
    )
    
    #------------RETRIVING DATA-----------
   
    base_query = Task.objects.select_related('details').prefetch_related('assign_to')
    
    if type=='completed':
        tasks = base_query.filter(status='COMPLETED')
    elif type =='pending':
        tasks = base_query.filter(status='PENDING')
    elif type =='in_progress':
        tasks = base_query.filter(status='IN_PROGRESS')
    elif type =='all':
        tasks = base_query.all()
    
    context = {
        'tasks':tasks,
        'Count':counts
        # 'total_task':total_task,
        # 'completed_task':completed_task,
        # 'pending_task':pending_task,
        # 'in_progress':in_progress
    }
    
    return render(request,"dashboard/manager_dashboard.html",context)

def test(request):
    context = {
        "names":["Mahmud"]
    }
    return render(request,"test.html",context)

@login_required(login_url='signIn')
@permission_required('tasks.add_task', login_url='signIn')
def create_task(request):
    task_form = TaskModelForm()
    task_detail_form = TaskDetailModelForm()
    if(request.method == 'POST'):
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST)
        if task_form.is_valid() and task_detail_form.is_valid():
            """ For Model Form Data"""
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            
            messages.success(request,"TASK CREATED SUCCESSFULLY")
            return redirect("create-task")
                
    context = {"task_form": task_form,"task_Detail":task_detail_form}
    return render(request,"task_form.html",context)


@login_required
@permission_required('tasks.add_task', login_url='no-permission')
def update_task(request,id):
    task = Task.objects.get(id=id)
    task_form = TaskModelForm(instance= task)
    
    if task.details:   
        task_detail_form = TaskDetailModelForm(instance=task.details)
        
    if(request.method == 'POST'):
        task_form = TaskModelForm(request.POST,instance = task)
        task_detail_form = TaskDetailModelForm(request.POST,instance=task.details)
        if task_form.is_valid() and task_detail_form.is_valid():
            """ For Model Form Data"""
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            
            messages.success(request,"TASK UPDATED SUCCESSFULLY")
            return redirect("update-task",id)
                
    context = {"task_form": task_form,"task_Detail":task_detail_form}
    return render(request,"task_form.html",context)

@login_required
@permission_required('tasks.add_task', login_url='no-permission')
def delete_task(request,id):
    if request.method=='POST':
        task = Task.objects.get(id=id)
        task.delete()
    
        messages.success(request,"TASK DELETE SUCCESSFUL")
        return redirect("manager-dashboard")
    else:
        messages.error(request,"Something Wrong")
        return redirect("manager-dashboard")

@login_required
@permission_required('tasks.add_task', login_url='no-permission')
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