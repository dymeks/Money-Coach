# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from ..log_reg_app.models import User
import plotly.plotly as py
from plotly.graph_objs import Scatter, Layout
import plotly.graph_objs as go
import plotly
import plotly.tools as tls
from datetime import datetime
import pandas as pd

from django.conf import settings
from django.core.files.storage import FileSystemStorage
import xlrd
import pandas as pd
from pandas import ExcelFile
from pandas import ExcelWriter

from django import forms
import django_excel as excel
from .models import Transaction, Document
from ..log_reg_app.models import User

class UploadFileForm(forms.Form):
    file = forms.FileField()

# Create your views here.
def home(request):

	response = "THis will display the success page/home page after login/registration is successful"
	
	df = pd.read_csv("media/documents/goals/susan/susan_goals.csv")

	context = {
		'user_name': User.objects.get(id=request.session['user_id']).first_name,
		'response':response,
		'goals':df['goal'],

	}
	return render(request,'expense_tracker_app/index.html',context)
def pie_chart(request):

	labels = ['Rent','Food','Entertainment','Car']
	values = [135.90,25.6,100.30,200.74]
	trace = go.Pie(labels=labels, values=values)
	py.plot([trace], filename='basic_pie_chart',auto_open=False)
	pie_chart = tls.get_embed('https://plot.ly/~dymeks/0')

	return render(request,'expense_tracker_app/history.html',{'graph':pie_chart})
def history(request):
	df = pd.read_csv("media/documents/2018/03/sample_transaction2.csv")
	
	trace_high = go.Scatter(
		x=df.date,
		y=df['price'],
		name = "Price",
		line = dict(color = '#17BECF'),
		opacity = 0.8)
	data = [trace_high]

	layout = dict(
		title='Monthly Finances',
		xaxis=dict(
			rangeselector=dict(
				buttons=list([
					dict(count=1,
						label='1m',
						step='month',
						stepmode='backward'),
					dict(count=6,
						label='6m',
						step='month',
						stepmode='backward'),
					dict(step='all')
				])
			),
			rangeslider=dict(),
			type='date'
		)
	)

	fig = dict(data=data,layout=layout)
	py.plot(fig, filename='history_chart',auto_open=False,link=False)
	
	context = {
		'graph': tls.get_embed('https://plot.ly/~dymeks/29')
	}

	return render(request,'expense_tracker_app/history.html',context)

def graph(request):
	df = pd.read_csv("media/documents/goals/susan/susan_goals.csv")
	print "The entire csv file: "+ str(df)
	for goal in df:
		print goal
		# trace1 = go.Bar(
		# 	x=goal.goal,
		# 	y=df.current_amount,
		# 	name='amount I have saved'
		# )

		# trace2 = go.Bar(
		# 	x=df.goal,
		# 	y=df.total_amount,
		# 	name='Amount I have left to save'
		# )

	# data = [trace1, trace2]
	# layout = go.Layout(
	#     barmode='stack'
	# )

	# fig = go.Figure(data=data, layout=layout)
	# py.plot(fig, filename='goals',auto_open=False,link=False)

	# tls.get_embed('https://plot.ly/~dymeks/31')
def import_sheet(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)
        if form.is_valid():
			user = User.objects.get(id=request.session['user_id'])
			instance = Document.objects.create(document=request.FILES['file'], user=User.objects.get(id=request.session['user_id']))			
            
			request.FILES['file'].save_to_database(
                model=Transaction,
                mapdict=['date_of_purchase', 'company', 'category', 'price',]
				)
			t = Transaction.objects.last().company
			print t
			return HttpResponse("OK")

        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
        return render(
            request,
            'expense_tracker_app/upload_form.html',
            {'form': form
			})
		
def display_docs(request):
	documents = Document.objects.all()
	return render(
		request,
		'expense_tracker_app/docs.html',
		{'documents': documents
		})
