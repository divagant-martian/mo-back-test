from django.urls import path
from . import views
urlpatterns = [
    path('search/<str:name>', views.search, name='search'),
]
