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
from django.db.models import Sum
from django import forms
import django_excel as excel
from .models import Transaction, Document, Goal
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
	
def options(request):
	return render(request, 'expense_tracker_app/options.html')

def pie_chart(request):
	categories = []
	prices = []
	user = User.objects.get(id=request.session['user_id'])
	user_history = Transaction.objects.filter(user=user)

	for transaction in user_history:
		if transaction.category not in categories:
			categories.append(transaction.category)

	for category in categories:
		print "Category: " + str(category)
		sum_category = Transaction.objects.filter(category=category).aggregate(Sum('price'))
		prices.append(sum_category['price__sum'])

	print prices
	print categories
	labels = categories
	values = prices
	trace = go.Pie(labels=labels, values=values)
	py.plot([trace], filename='basic_pie_chart',auto_open=False)
	pie_chart = tls.get_embed('https://plot.ly/~dymeks/0')
	request.session['graph'] = pie_chart
	return render(request,'expense_tracker_app/history.html',{'user_name':user.first_name})

def history(request):
	# df = pd.read_csv("media/documents/2018/03/sample_transaction2.csv")
	user = User.objects.get(id=request.session['user_id'])
	user_history = Transaction.objects.filter(user=user)
	print user_history
	prices = []
	dates = []
	for transaction in user_history:
		prices.append(transaction.price)
		dates.append(transaction.date_of_purchase)

	print prices
	print dates
	trace_high = go.Scatter(
		x=dates,
		y=prices,
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
	
	# context = {
	# 	'graph': tls.get_embed('https://plot.ly/~dymeks/29')
	# }
	request.session['graph'] = tls.get_embed('https://plot.ly/~dymeks/29')
	return render(request,'expense_tracker_app/history.html',{'user_name':user.first_name})

def graph(request):
	return render(request,'expense_tracker_app/history.html')
	
def display_goals(request):
	# df = pd.read_csv("media/documents/goals/susan/susan_goals.csv")
	user = User.objects.get(id=request.session['user_id'])
	user_goals = Goal.objects.filter(user=user)
	# print "The entire csv file: "+ str(df)
	goal_titles = []
	current_amount = []
	total_amount = []
	print "Goals: "+ str(user_goals)
	for goal in user_goals:
		goal_titles.append(goal.title)
		current_amount.append(goal.current_amount)
		total_amount.append(goal.total_amount)

	trace1 = go.Bar(
		x=goal_titles,
		y=current_amount,
		name='amount I have saved'
	)

	trace2 = go.Bar(
		x=goal_titles,
		y=total_amount,
		name='Amount I have left to save'
	)

	data = [trace1, trace2]
	layout = go.Layout(
	    barmode='stack'
	)

	fig = go.Figure(data=data, layout=layout)
	py.plot(fig, filename='goals',auto_open=False,link=False)
	user = User.objects.get(id=request.session['user_id'])
	context = {
		'goals':tls.get_embed('https://plot.ly/~dymeks/31'),
		'user_name': User.objects.get(id=request.session['user_id']).first_name,
		'goallist' : Goal.objects.filter(user=user),
	}

	return render(request,'expense_tracker_app/goals.html', context)

def import_sheet(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)
        if form.is_valid():
			user = User.objects.get(id=request.session['user_id'])
			instance = Document.objects.create(document=request.FILES['file'], user=User.objects.get(id=request.session['user_id']))
			request.session['doc_id'] = instance.id
			request.FILES['file'].save_to_database(
                model=Transaction,
                mapdict=['date_of_purchase', 'company', 'category', 'price',]
				)
			added_t = Transaction.objects.filter(document__isnull=True)
			for t in added_t:
				t.document = instance
				t.user = user
				t.save()			
			return redirect('/track/display')

        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
        return render(
            request,
            'expense_tracker_app/upload_form.html',
            {'form': form,
            	'user_name':User.objects.get(id=request.session['user_id']).first_name
			})
		
def display_docs(request):
	user = User.objects.get(id=request.session['user_id'])
	transactions = Document.objects.get(id=request.session['doc_id']).transactions_of.all()
	context = {
		'user': user,
		'transactions': transactions
	}
	return render(
		request,
		'expense_tracker_app/docs.html',
		context)

def edit(request, t_id):
	transaction = Transaction.objects.get(id=t_id)
	user = User.objects.get(id=request.session['user_id'])
	context = {
		'transaction': transaction,
		'user_name':user.name
	}
	return render(request, 'expense_tracker_app/edit.html', context)

def modify(request, t_id):
	t = Transaction.objects.get(id=t_id)
	t.date_of_purchase = request.POST['date']
	t.company = request.POST['company']
	t.category = request.POST['category']
	t.price = request.POST['price']
	t.save()
	return redirect('/track/display')

def add_manual(request):
	user = User.objects.get(id=request.session['user_id'])
	t = Transaction.objects.create(date_of_purchase=request.POST['date'], company=request.POST['company'], category=request.POST['category'], price=request.POST['price'])
	t.user = user
	t.save()
	return redirect('/track/graph')

def delete(request, t_id):
	t = Transaction.objects.get(id=t_id)
	t.delete()
	return redirect('/track/display')

def add_goal(request):
	user = User.objects.get(id=request.session['user_id'])
	g = Goal.objects.create(title=request.POST['title'], total_amount=request.POST['total'], current_amount=request.POST['saved'], user=user)
	g.save()
	return redirect('/track/goals')

def modify_goal(request):
	g = Goal.objects.get(title=request.POST['title'])
	g.current_amount = request.POST['saved']
	g.save()
	return redirect('/track/goals')

def delete_goal(request, g_id):
	g = Goal.objects.get(id=g_id)
	g.delete()
	return redirect('/track/goals')