from django.shortcuts import render, redirect
from . dashboard_chart import KPI_Dashboard
from bokeh.embed import components
# Create your views here.


def home(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, "dashboard/home.html", {})


def dashboard_view(request):

    script, div = components(KPI_Dashboard())

    return render(request, 'dashboard/dashboard_view.html', {'script': script, 'div': div})


def geo_site_based(request):

    return render(request, "dashboard/geo_site_based.html", {})


def geo_grid_based(request):
    return render(request, "dashboard/geo_grid_based.html", {})


def tasks(request):
    return render(request, "dashboard/tasks.html", {})


def geo_grid_coverage(request):
    return render(request, "dashboard/geo_grid_coverage.html",{})