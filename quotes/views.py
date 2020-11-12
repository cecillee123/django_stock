# copyright (C) 2020 Cecil Lee All Rights Reserved

from django.shortcuts import render, redirect
# Add in import for database, models, stockform, messages
from .models import Stock
from .forms import StockForm
from django.contrib import messages

# Create your views here.
# Create a home http GET request function
def home(request):
	import requests 
	import json

	if request.method == 'POST':
		ticker = request.POST['ticker']
		api_requests = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_fd78a6e8bc3e4d99b3f56a9a62648736")

		# load json to variable api
		try:
			api = json.loads(api_requests.content)
		# if error then do this
		except Exception as e:
			api = "Error..."
		# display http GET request of json api variable to home.html page
		return render(request, 'home.html', {'api': api })

	else:
		return render(request, 'home.html', {'ticker': "Enter a Ticker Symbol Above..."})

	
# Create a 'about' http GET request function
def about(request):
	return render(request, 'about.html', {})

# Create the 'add_stock' http GET request function
# StockForm and Message
def add_stock(request):
	import requests
	import json

	if request.method == 'POST':
		# form is a variable
		form = StockForm(request.POST or None)

		# if form is valid then save into database, display message and redirect page to add_stock.html
		if form.is_valid():
			form.save()
			messages.success(request, ("Stock Has Been Added"))
			return redirect('add_stock')

	else:
		ticker = Stock.objects.all()

		# create an array to store api data
		output = []
		for ticker_item in ticker:

			api_requests = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_fd78a6e8bc3e4d99b3f56a9a62648736")

			# load json to variable api
			try:
				api = json.loads(api_requests.content)
				output.append(api)
			# if error then do this
			except Exception as e:
				api = "Error..."



		return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})

# Create a new 'delete stock' function
def delete(request, stock_id):
	# define item as stock.objects variable
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ("Stock Has Been Deleted"))
	return redirect(delete_stock)

# Create a 'delete_stock' http GET request function
def delete_stock(request):
	ticker = Stock.objects.all()
	return render(request, 'delete_stock.html', {'ticker': ticker})