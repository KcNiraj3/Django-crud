from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, ExcelFile
from .forms import StudentForms
import pandas as pd
from django.http import JsonResponse
from django.conf import settings

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

def export_data_to_excel(request):
    objs = Student.objects.all()
    
    data= []
    for obj in objs:
        data.append({"name" : obj.name, 
                  "age"  : obj.age})
        pd.DataFrame(data).to_excel('students.xlsx')
        
    return JsonResponse({
        "status": 200,
    })
    
def import_data_to_excel(request):
    if request.method == 'POST':
        file = request.FILES['files']
        obj = ExcelFile.objects.create(
            file = file
        )
        path = str(obj.file)
        print(f'{settings.BASE_DIR}/{path}')
        df = pd.read_excel(path)
        #print(df)
        for index, row in df.iterrows():
            Student.objects.create(
            name = row['name'],
            age = row['age']
            ) 
        return JsonResponse({
        "status": 200,
    })     
    
    return render(request, 'excel.html')  