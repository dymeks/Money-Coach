# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
import plotly.plotly as py
from plotly.graph_objs import Scatter, Layout
import plotly.graph_objs as go
import plotly
import plotly.tools as tls
from datetime import datetime
import pandas as pd

# Create your views here.
def home(request):

	response = "THis will display the success page/home page after login/registration is successful"
	df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv")
	trace_high = go.Scatter(
		x=df.Date,
		y=df['AAPL.High'],
		name = "AAPL High",
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

	trace1 = go.Bar(
		x=['car', 'house', 'trip to Europe'],
		y=[20.5, 14.0, 23.99],
		name='amount I have saved'
	)
	trace2 = go.Bar(
		x=['car', 'house', 'trip to Europe'],
		y=[12.4, 18.2, 29],
		name='Amount I have left to save'
	)

	data = [trace1, trace2]
	layout = go.Layout(
	    barmode='stack'
	)

	fig = go.Figure(data=data, layout=layout)
	py.plot(fig, filename='goals',auto_open=False,link=False)
	context = {
		'graph': tls.get_embed('https://plot.ly/~dymeks/29'),
		'response':response,
		'goals':tls.get_embed('https://plot.ly/~dymeks/31'),

	}
	return render(request,'expense_tracker_app/index.html',context)