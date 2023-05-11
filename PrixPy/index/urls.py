from django.urls import path, re_path
from index import views





urlpatterns = [
    path('', views.index, name='index'),
    
    path('input', views.input, name='input'),
    path('Import_excel', views.Import_excel, name='Import_excel'),
  
    path('ind_elem', views.ind_elem, name ="ind_elem"),
    #path('',views.Table, name='archive'),
    re_path(r'^.*\.*', views.pages, name='pages'),
    #path('Import_excel', views.Import_excel, name='Import_excel'),
    
]



