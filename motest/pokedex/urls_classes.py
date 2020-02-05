from django.urls import path
from . import view_classes

urlpatterns = [
    path('', view_classes.Index.as_view(), name='index'),
    path('search', view_classes.Search.as_view(), name='search'),
    path('view', view_classes.View.as_view(), name='view'),
]
