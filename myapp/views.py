from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, ExcelFile
from .forms import StudentForms
import pandas as pd
from django.http import JsonResponse, HttpResponse
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

# def export_data_to_excel(request):
#     objs = Student.objects.all()
    
#     data= []
#     for obj in objs:
#         data.append({"name" : obj.name, 
#                   "age"  : obj.age})
#         pd.DataFrame(data).to_excel('students.xlsx')
        
#     return JsonResponse({
#         "status": 200,
#     })
    
# def import_data_to_excel(request):
#     if request.method == 'POST':
#         file = request.FILES['files']
#         obj = ExcelFile.objects.create(
#             file = file
#         )
#         path = str(obj.file)
#         print(f'{settings.BASE_DIR}/{path}')
#         df = pd.read_excel(path)
#         #print(df)
#         for index, row in df.iterrows():
#             Student.objects.create(
#             name = row['name'],
#             age = row['age']
#             ) 
#         return JsonResponse({
#         "status": 200,
#     })     
    
#     return render(request, 'excel.html')  

from tablib import Dataset  # Import Dataset class to handle data export formats
from .resources import StudentResource  # Import the resource class that defines how data should be exported
from .models import Student  # Import Employee model (though it's not directly used here, it's implied)


def export_data(request):
    if request.method=="POST":
        file_format = request.POST["file-format"]
        student_resource = StudentResource() # calling Studentresource class
        dataset = student_resource.export() # this class helps to export file to download
        
        if file_format == "CSV":
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
            return response
        
        elif file_format == "JSON":
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="exported_data.json"' # prompt the browser to download the file with the specified name
            return response
        
        elif file_format == 'Excel':  # Ensure this matches the value in your HTML dropdown
            # Prepare an Excel response (XLSX format)
            response = HttpResponse(dataset.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="exported_data.xlsx"'
            return response
    return render(request, 'export.html')  

def import_data(request):
    if request.method=="POST":
        file_format = request.POST["file-format"]
        student_resource = StudentResource() # calling Studentresource class
        #dataset = student_resource.export() # this class helps to export file to download
        dataset = Dataset() #Dataset is a tabular data structure provided by the tablib
        new_employees = request.FILES['importData'] #retrieves the uploaded file from the request. The file is accessed via request.FILES, and 'importData' is the name of the file input field in the form.

        
        if file_format == 'CSV':
            dataset.load(new_employees.read().decode('utf-8'), format='csv') #If the file format is CSV, this block reads the uploaded file, decodes it from bytes to a string using utf-8 encoding, and loads it into the dataset object using the csv format.
        
        elif file_format == 'JSON':
            dataset.load(new_employees.read().decode('utf-8'), format='json')
            # Testing data import
        result = student_resource.import_data(dataset, dry_run=True) # A dry run validates the data and checks for errors (e.g., missing fields, invalid data types) without actually saving the data to the database.
                                                                            # The result object contains information about the import process, including any errors.

        if not result.has_errors(): # If there are no errors, 
            # Import now
            student_resource.import_data(dataset, dry_run=False)  # this line performs the actual import by setting dry_run=False
        
    return render(request, 'import.html')  
    