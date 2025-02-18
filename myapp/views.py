from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForms

# Create your views here.

def home(request, id=None): # default arguments
    if id:
        student_update = get_object_or_404(Student, id=id) 
        form = StudentForms(request.POST or None,instance=student_update) 
    else:
        form = StudentForms(request.POST or None)    

    form = StudentForms()
    if request.method == 'POST':
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
