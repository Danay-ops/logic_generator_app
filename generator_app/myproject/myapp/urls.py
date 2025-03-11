from django.urls import path
from .views import editor_view, process_file

urlpatterns = [
    path('', editor_view, name="editor"),  # Страница с Monaco Editor
    path('process/', process_file, name="process_file"),  # Обработка файла
]
