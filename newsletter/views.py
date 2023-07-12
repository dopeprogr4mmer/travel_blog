from django.template.loader import render_to_string
from django.http import HttpResponse
from .models import Signup
import json

def fetch_signup_data(request=None):
	data = Signup.objects.all()
	emails = []
	for row in data:
		emails.append(row.email)
	context = {"emails":emails}
	return HttpResponse(f'<h3>{context}</h3>') 
 
