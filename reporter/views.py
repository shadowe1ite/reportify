from django.shortcuts import render
from .forms import ReportForm

# Create your views here.
def index(request):
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            # Handle the valid form data here
            # For example, save the form or process it further
            return render(request, 'reporter/thank_you.html', {'form': form})
    else:
        form = ReportForm()
    return render(request, 'reporter/index.html', {'form': form})