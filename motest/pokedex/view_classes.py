from django.shortcuts import redirect
from django.views import generic
from .models import Pokemon
from .forms import SearchForm


class Index(generic.ListView):
    """"""
    # FIXME add docstring
    template_name = 'index.html'
    # TODO do stuff


class Search(generic.CreateView):
    """"""
    # FIXME add docstring
    form_class = SearchForm
    template_name = 'search.html'
    # TODO do stuff. Create Show view

class View(generic.CreateView):
    """"""
    # FIXME add docstring
    form_class = SearchForm
    template_name = 'view.html'
    # TODO do stuff. Create Show view
