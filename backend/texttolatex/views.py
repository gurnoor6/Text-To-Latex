from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from .ocr import getImageText
from .src.predict import predictions

class Conversion(viewsets.ModelViewSet):
	queryset = Convert.objects.all()
	serializer_class = ConvertSerializer

	def post(self,request,*args,**kwargs):
		identifier = request.data['identifier']
		pic = request.data['picture']
		Convert.objects.create(identifier = identifier, picture = pic)


@csrf_exempt
def getText(request):
	if request.method=="POST":
		images = Convert.objects.all()
		identifier = request.POST['identifier']
		images = images.filter(identifier=identifier)
		# print(type(images[0].picture.name))
		# print(t)
		convert_serializer = ConvertSerializer(images,many=True)
		if(len(images)==1):
			# text = getImageText("media/"+images[0].picture.name)
			text = predictions("media/"+images[0].picture.name)
			print(text)
			return JsonResponse({"response":text})
		else:
			return JsonResponse({"response":"fail"})