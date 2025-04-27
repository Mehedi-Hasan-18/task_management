from django import forms
from tasks.models import Task

#Django Form NO NEED THIS IS BASIC           
class TaskForm(forms.Form):
    title = forms.CharField(max_length=250)
    discription = forms.CharField(widget=forms.Textarea,label="Description")
    due_date = forms.DateField(widget=forms.SelectDateWidget,label="Due Date")
    assign_to = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,label="Assign To",choices=[])
    
    def __init__(self,*args,**kwargs):
        employees = kwargs.pop("employees",[])
        super().__init__(*args,**kwargs) 
        self.fields["assign_to"].choices = [(emp.id,emp.name) for emp in employees]           
 
# MIXIN           
class StyleFormMixin:
    
    default_classes = "border-2 border-gray-300 w-full rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500"
    
    def apply_style_widget(self):
        for fieldName,field in self.fields.items():
            if isinstance(field.widget,forms.TextInput):
                field.widget.attrs.update({
                    'class':self.default_classes,
                    'placeholder':f'Enter {field.label.lower()}'
                })
            elif isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    'class':self.default_classes,
                    'placeholder':f'Enter {field.label.lower()}'
                })
            elif isinstance(field.widget,forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class':self.default_classes
                })
            elif isinstance(field.widget,forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class':'space-y-2'
                })
            
                
            
    
 
            
#DJANGO MODEL FORM
class TaskModelForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','discription','due_date','assign_to']
        widgets = {
            'due_date':forms.SelectDateWidget,
            'assign_to':forms.CheckboxSelectMultiple
        }
        
        
        '''MANUAL WIDGET NO NEED THIS IS BASIC'''
        # widgets = {
        #     'title':forms.TextInput(attrs={
        #         'class':"border-2 border-gray-300 w-full rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500",
        #         'placeholder':'Enter Details' 
        #     }),
        #     'discription':forms.Textarea(attrs={
        #         'class':"border-2 border-gray-300 w-full rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500",
        #         'placeholder':'Enter Task Title' 
        #     }),
        #     'due_date':forms.SelectDateWidget(attrs={
        #         'class':"border-2 border-gray-300 w-full rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500",
        #     }),
        #     'assign_to':forms.CheckboxSelectMultiple(attrs={
        #         'class':"border-2 border-gray-300 w-full rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500"
        #     })
        # }
        
    """WIDGET APPLY NIXIN"""
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.apply_style_widget()
  
  
#MIXIN PRSCTICE
class styleMixin:
    
    default_classess = "border-2 border-gray-300 w-full rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500"
    def add_style(self):
        for fieldname,field in self.fields.items():
            if isinstance(field.widget,forms.TextInput):
                field.widget.attrs.update({
                    'class':self.default_classess,
                    'placeholder':f'Enter {field.label.lower()}'
                })
            elif isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    'class':self.default_classess,
                    'placeholder':f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget,forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class':self.default_classess
                })
            elif isinstance(field.widget,forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class':self.default_classess
                })
        
              
        
#TASK MODEL FORM PRACTICE
class TaskModelFormPrac(styleMixin,forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','discription','due_date','assign_to']
        widgets={
            'due_date':forms.SelectDateWidget,
            'assign_to':forms.CheckboxSelectMultiple
        }
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.add_style()