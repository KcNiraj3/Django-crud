from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForms

# Create your views here.

def home(request, id=None): # default arguments
    if id:
        student_update = get_object_or_404(Student, id=id) 
        form = StudentForms(request.POST or None,instance=student_update) # takes info or empty info and supply to  form as post request
    else:
        form = StudentForms(request.POST or None)    # if no need to update. will take create form

  
    if request.method == 'POST':
        if "delete" in request.POST:
            student_to_delete = get_object_or_404(Student, id=request.POST["delete"])
            student_to_delete.delete()
            return redirect("home")
        
        form = form
        if form.is_valid():
            form.save()
            return redirect('home')
    
    students = Student.objects.all()
    context ={
        'students' : students ,
        'form' : form
    }
    
    return render(request, "home.html", context = context)
