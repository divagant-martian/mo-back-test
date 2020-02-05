from django.http import HttpResponse

def index(request):
    return HttpResponse("I'm index")
    # TODO

def search(request):
    return HttpResponse("I'm search")
    # TODO

def view(request):
    return HttpResponse("I'm view")
    # TODO

# Create your views here.
