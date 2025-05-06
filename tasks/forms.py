from django import forms
from tasks.models import Task,TaskDetail

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
    """ Mixing to apply style to form field"""

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_style_widget()

    default_classes = "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"

    def apply_style_widget(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder':  f"Enter {field.label.lower()}",
                    'rows': 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                # print("Inside Date")
                field.widget.attrs.update({
                    "class": "border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                # print("Inside checkbox")
                field.widget.attrs.update({
                    'class': "space-y-2"
                })
            else:
                # print("Inside else")
                field.widget.attrs.update({
                    'class': self.default_classes
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
        
        
    """WIDGET APPLY NIXIN"""
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.apply_style_widget()
  
  
class TaskDetailModelForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model = TaskDetail
        fields = ['priority','notes','image']
        
    