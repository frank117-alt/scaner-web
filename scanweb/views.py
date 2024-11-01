from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.views import View
from .form import IPDomainForm
from django.shortcuts import render 
from celery.result import AsyncResult
from django.urls import reverse
import json
from django.contrib.gis.geoip2 import GeoIP2
from .tasks import perform_scan,resolverdns




from celery.result import AsyncResult


def ip_location_view(request, ip):
    g = GeoIP2()
    try:
        # Obtener información geográfica de la IP
        location = g.city(ip)
        lat = location['latitude']
        lon = location['longitude']
        city = location['city']
        country = location['country_name']
        region = location['country_code']
        print(lat)
        print(lon)

        context = {
            'ip': ip,
            'lat': lat,
            'lon': lon,
            'city': city,
            'country': country,
            'region':region,
        }
        return render(request, 'location_map.html', context)
    except Exception as e:
        return render(request, 'location_map.html', {'error': str(e)})



def resultView(request):
    # Get task IDs from the session
    task_ids = request.session.get('task_ids')

    if not task_ids:
        # Handle the case where task IDs are missing
        return render(request, 'result.html', {'error': 'No tasks found'})

    # Use task IDs to get the results
    results = {
        'task_one': AsyncResult(task_ids['task_one']),
        'task_two': AsyncResult(task_ids['task_two']),
    }

    # Pass the results to the template
    context = {
        'results': results,
    }

    return render(request, 'result.html', context)
class indexView(TemplateView):
     template_name=('index.html')

def infoView(request):
        if request.method =="POST":
            form = IPDomainForm(request.POST)
            if  form.is_valid():
                 host = form.cleaned_data['host']
                 print(f"IP/Dominio enviado: {host}")

                # Lanza la tarea de escaneo en segundo plano
                 task_one= perform_scan.delay(host)
                 task_two =resolverdns.delay(host) 
                 print(f"Task Two ID: {task_two.id}")
                 
                 request.session['task_ids'] ={
                    'task_one':task_one.id,
                    'task_two':task_two.id
                 }
                
                 return redirect('result')

            else:
                error_message = "la ip o dominio no son correctos"
                return render (request,'index.html',{'form':form,'error_message':error_message})
        else:
            form = IPDomainForm()
        return render(request, 'index.html', {'form': form})

def scan_status_view(request, task_id):
    task = AsyncResult(task_id)  # Obtiene el estado de la tarea

    if task.state == 'SUCCESS':
        # Si el escaneo está completo, muestra los resultados
        result = task.result
        return render(request, 'scan_result.html', {'result': result})
    elif task.state == 'PENDING':
        # Si la tarea está pendiente o en progreso
        return render(request, 'scan_status.html', {'status': 'En progreso...'})

    # Si la tarea ha fallado
    return render(request, 'scan_status.html', {'status': 'Error en el escaneo.'})