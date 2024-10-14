# En urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),  # Ruta principal
    path('upload/', views.upload_file, name='upload_file'),
    path('resumen_ventas/', views.resumen_ventas, name='resumen_ventas'),
    path('grafico/', views.grafico, name='grafico'),
    path('datos_estudiante/', views.datos_estudiante, name='datos_estudiante'),
]
