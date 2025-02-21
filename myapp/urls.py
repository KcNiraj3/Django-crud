from django.contrib import admin
from django.urls import path, include
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('update/<int:id>', views.home, name="update_student"),
    # path('export_data_to_excel/', views.export_data_to_excel, name="export_data_to_excel"),
    # path('import_data_to_excel/', views.import_data_to_excel, name="import_data_to_excel"),
    path('export_data/', views.export_data, name="export_data"),
]
