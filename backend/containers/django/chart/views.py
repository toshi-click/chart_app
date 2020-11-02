from django.shortcuts import render
from django.views import generic, View

# Create your views here.
# class IndexView(generic.TemplateView):
#     template_name = 'index.html'

class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')
index_page = IndexView.as_view()
