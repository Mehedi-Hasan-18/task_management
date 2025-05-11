from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm,TaskDetailModelForm
from tasks.models import Task,TaskDetail,Project
from django.db.models import Q,Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from django.utils.decorators import method_decorator
from users.views import is_admin
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic.base import ContextMixin
from django.views.generic.list import ListView
from django.views.generic import DetailView,UpdateView
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

# @login_required
# @permission_required('tasks.add_task', login_url='signIn')
# def create_task(request):
#     task_form = TaskModelForm()
#     task_detail_form = TaskDetailModelForm()
#     if(request.method == 'POST'):
#         task_form = TaskModelForm(request.POST)
#         task_detail_form = TaskDetailModelForm(request.POST, request.FILES)
#         if task_form.is_valid() and task_detail_form.is_valid():
#             """ For Model Form Data"""
#             task = task_form.save()
#             task_detail = task_detail_form.save(commit=False)
#             task_detail.task = task
#             task_detail.save()
            
#             messages.success(request,"TASK CREATED SUCCESSFULLY")
#             return redirect("create-task")
                
#     context = {"task_form": task_form,"task_Detail":task_detail_form}
#     return render(request,"task_form.html",context)

"""Class Based View
    Used Build In Mixin Of Django
"""
create_decorator = [login_required,permission_required('tasks.add_task', login_url='signIn')]

@method_decorator(create_decorator,name='dispatch')
class CreateTask(ContextMixin,LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = 'task.add_task'
    login_url='signIn'
    template_name = 'task_form.html'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)  
        context['task_form'] =kwargs.get('task_form',TaskModelForm())
        context['task_Detail'] =kwargs.get('task_Detail',TaskDetailModelForm())
        return context
    
    
    def get(self,request,*args,**kwargs):
        
        context = self.get_context_data()
        return render(request,self.template_name,context)
    
    def post(self,request,*args,**kwargs):
        if(request.method == 'POST'):
            task_form = TaskModelForm(request.POST)
            task_detail_form = TaskDetailModelForm(request.POST, request.FILES)
            if task_form.is_valid() and task_detail_form.is_valid():
                """ For Model Form Data"""
                task = task_form.save()
                task_detail = task_detail_form.save(commit=False)
                task_detail.task = task
                task_detail.save()
                messages.success(request,"TASK CREATED SUCCESSFULLY")
                context = self.get_context_data(task_form=task_form,task_Detail=task_detail_form)
                return render(request,self.template_name,context)


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

class UpdateTaskView(UpdateView):
    model = Task
    form_class = TaskModelForm
    template_name = 'task_form.html'
    context_object_name='task'
    pk_url_kwarg = 'id'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['task_form'] = self.get_form()
        
        if hasattr(self.object, 'details') and self.object.details:
            context['task_Detail'] = TaskDetailModelForm(instance = self.object.details)
        else:
            context['task_Detail'] = TaskDetailModelForm()
            
        return context
    
    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        task_form = TaskModelForm(request.POST, instance = self.object)

        task_Detail = TaskDetailModelForm(request.POST,request.FILES, instance=getattr(self.object, 'details' , None))

        if task_form.is_valid() and task_Detail.is_valid():
            task = task_form.save()
            task_detail = task_Detail.save(commit=False)
            task_detail.task = task
            task_detail.save()
            
            messages.success(request,"TASK UPDATED SUCCESSFULLY")
            return redirect("update-task",self.object.id)
        
        return redirect('update-task', self.object.id)
    

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
    tasks = Task.objects.select_related("project").all()
    
    projects = Project.objects.annotate(num_task=Count('task')).order_by('num_task')
    return render(request,'show_task.html',{'projects':projects})

view_project_decorator = [login_required,permission_required('projects.view_project', login_url='signIn')]

@method_decorator(view_project_decorator,name='dispatch')
class ViewProject(ListView):
    model=Project
    context_object_name = 'projects'
    template_name ='show_task.html'
    
    def get_queryset(self):
        queryset = Project.objects.annotate(num_task=Count('task')).order_by('num_task')
        return queryset


@login_required
@permission_required('tasks.add_task', login_url='no-permission')
def task_details(request,task_id):
    task = Task.objects.get(id=task_id)
    status_choice = Task.STATUS_CHOICES
    
    if request.method == 'POST':
        selected_status = request.POST.get('task_status')
        task.status = selected_status
        task.save()
        return redirect('task-details', task_id)
    
    return render(request, 'task_details.html' , {'task':task, 'status_choice':status_choice})

task_details_decorator = [login_required,permission_required('tasks.detail_task', login_url='signIn')]

@method_decorator(task_details_decorator,name='dispatch')  
class TaskDetailView(DetailView):
    model = Task
    context_object_name = 'task' 
    template_name = 'task_details.html'
    pk_url_kwarg = 'task_id'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['status_choice'] = Task.STATUS_CHOICES
        return context
    
    def post(self,request,*args,**kwargs):
        task = self.get_object()
        selected_status = request.POST.get('task_status')
        task.status = selected_status
        task.save()
        return redirect('task-details', task.id)
    
    
    
    
@login_required   
def employee_dashboard(request):
    return render(request,'dashboard/manager_dashboard.html')
    
    
    
@login_required   
def dashboard(request):
    if is_manager(request.user):
        return redirect('manager-dashboard')
    elif is_employee(request.user):
        return redirect('employee_dashboard')
    elif is_admin(request.user):
        return redirect('admin_dashboard')
    else :
        return redirect('no-permission')
