from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Car
import requests

api_url = "https://zyanyatech1-license-plate-recognition-v1.p.rapidapi.com/recognize_url"

headers = {
	"X-RapidAPI-Key": "9ddb0ab3fdmshd38e2a337759cc3p1af9b8jsnde847bad7fa1",
	"X-RapidAPI-Host": "zyanyatech1-license-plate-recognition-v1.p.rapidapi.com"
}

def recognize_license_plate(image_url):
    querystring = {"image_url": image_url}
    return requests.post(api_url, headers=headers, params=querystring).json()

def home(request):
    all_cars = Car.objects.all().order_by('-id')

    if request.method == 'POST':
        image = request.FILES['image']
        car = Car.objects.create(image=image)
        
        image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTr3TvrN5fG5MIS4-YdpKi0TmwPr5OdUdv5tg"
        recognition_result = recognize_license_plate(image_url)
        
        if recognition_result and 'results' in recognition_result:
            license_number = recognition_result['results'][0]['plate']
            car.license_number = license_number
            car.recognition_result = recognition_result  
            car.save()
        
        return HttpResponseRedirect(reverse('home'))

    context = {
        "all_cars": all_cars
    }
    
    return render(request, 'base/home.html', context)

