# Import forms Class from django
from django import forms
# Import Stock Class into models or django database
from .models import Stock

# Create a new class
class StockForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ["ticker"]