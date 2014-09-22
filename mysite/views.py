from django.shortcuts import render

def my_custom_404_view(request):
	return render(request,'errorpages/error_404.html')
