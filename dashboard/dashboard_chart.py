	#!/usr/bin/env python
	# coding: utf-8

	# In[57]:


	# version 0.1
	# notes: based on TailCell v0.4
	# function: Accessibility, Retainability with different thresholds

	# version 0.2
	# function: Box Annotations, Band Annotations

	# version 0.3
	# function: create combined_KPI_plot function
	# function: create tabs for 3 show cases

	# version 0.4
	# create double line chart for throughput

	# version 0.5
	# create function of KPI_Dashborad(filename) 


	# In[58]:


def KPI_Dashboard(filename='Detail KPI.csv'):


	# In[59]:


	# bokeh toolkits https://bokeh.pydata.org/en/latest/docs/user_guide/tools.html
	from bokeh.io import output_file, show, curdoc
	from bokeh.plotting import figure
	from bokeh.models import ColumnDataSource, HoverTool, CategoricalColorMapper, DatetimeTickFormatter,Slider,Select,CustomJS,LinearAxis, Range1d,BoxAnnotation,Band
	from bokeh.layouts import column, row, gridplot,widgetbox,layout
	from bokeh.models.widgets import Tabs, Panel, RangeSlider, Button, DataTable, TableColumn, NumberFormatter, DateFormatter


	#import other libraries
	import pandas as pd
	import numpy as np
	import matplotlib.pyplot as plt
	import seaborn as sns

	import os
	from os.path import dirname, join


	# In[60]:


	DetailKPI = pd.read_csv(join(dirname("__file__"), filename))
	#print(DetailKPI.shape)
	#DetailKPI.head()
	#print(DetailKPI.dtypes)


	# In[61]:


	#To work with time series data in pandas, your date columns needs to be of the datetime64 type.
	DetailKPI['Date'] = pd.to_datetime(DetailKPI['Date'])
	DetailKPI['Year'] = DetailKPI.Date.apply(lambda x: x.year)
	DetailKPI['Month'] = DetailKPI.Date.apply(lambda x: x.month)
	DetailKPI['Day'] = DetailKPI.Date.apply(lambda x: x.day)
	#DetailKPI.head()
	#print(DetailKPI.dtypes)


	# In[62]:


	# define format of time series
	formatter_hours=["%d %B %Y"]
	formatter_days=["%m/%d/%Y"]
	formatter_days_new=['%m/%d', '%a%d']
	formatter_months=["%d %B %Y"]
	formatter_years=["%d %B %Y"]


	# In[63]:


	#DetailKPI['TPG_Intra-frequency Handover Out Success Rate(%)'].describe()


	# In[64]:


	#Nominate Data Source for Accessibility Plot
	#Issue: Link Plot does not work upon adding extra y axis
	source_KPI = ColumnDataSource(DetailKPI)
	hover_KPI = HoverTool(tooltips=[("Date", "@Date{%F}"),
											 ('TPG_RRC Setup Success Rate(%)', "@{TPG_RRC Setup Success Rate(%)}{0.00}"),
										  ('TPG_RRC Setup Attempt', "@{TPG_RRC Setup Attempt}{0.00}"),
											('TPG_E-RAB Setup Success Rate(%)', "@{TPG_E-RAB Setup Success Rate(%)}{0.00}"),
											('TPG_E-RAB Setup Attempt', "@{TPG_E-RAB Setup Attempt}{0.00}"),], 
					  formatters = { "Date": "datetime"},mode='mouse')

	toolkit = ['pan','reset','box_zoom','crosshair','box_select, lasso_select','save',hover_KPI]

	#Color sets
	lineColor = 'green'
	HoverColor = 'red'


	# In[65]:


	#show case1: Box Annotation, upper and lower threshold to be defined

	def box_annotations (Upper_Threshold, Lower_Threshold, plotname):
		low_box = BoxAnnotation(top=Lower_Threshold, fill_alpha=0.1, fill_color= None)
		mid_box = BoxAnnotation(bottom=Lower_Threshold, top=Upper_Threshold, fill_alpha=0.1, fill_color='red')
		high_box = BoxAnnotation(bottom=Upper_Threshold, fill_alpha=0.1, fill_color= None)
		plotname.add_layout(low_box)
		plotname.add_layout(mid_box)
		plotname.add_layout(high_box)


	# In[66]:


	#show case2: band Annotation, 68–95–99.7 rule https://en.wikipedia.org/wiki/68%E2%80%9395%E2%80%9399.7_rule
	#Pr(mean-std <= X <= mean+std) = 0.6827
	#Pr(mean-2std <= X <= mean+2std) = 0.9545
	#Pr(mean-3std <= X <= mean+3std) = 0.9973

	def band_annotations (counter, plotname):
		lower = DetailKPI[counter].mean() - DetailKPI[counter].std()
		upper = DetailKPI[counter].mean() + DetailKPI[counter].std()
		band = Band(base='Date', lower=lower, upper=upper, source=source_KPI, level='underlay',
				fill_alpha=1.0, line_width=1, line_color='black')
		plotname.add_layout(band)


	# In[67]:


	#show case3: apply band Annotation, replace mean by KPI baseline

	def baseline_annotations (counter, plotname,KPI_Baseline):
		lower = KPI_Baseline - DetailKPI[counter].std()
		upper = KPI_Baseline + DetailKPI[counter].std()
		band = Band(base='Date', lower=lower, upper=upper, source=source_KPI, level='underlay',
				fill_alpha=1.0, line_width=1, line_color='black')
		plotname.add_layout(band)


	# In[68]:


	# Write a function to create combined line + bar plot with 2 y-axis
	# issue: cannnot put all three plots into one tab. The issue is fixed by define 'return plot_name'

	def combined_KPI_plot(line_name, bar_name, plot_name):
		source_KPI = ColumnDataSource(DetailKPI)
		ymin_1st = DetailKPI[line_name].min()
		ymax_1st = DetailKPI[line_name].max()
		ymin_2nd = DetailKPI[bar_name].min()
		ymax_2nd = DetailKPI[bar_name].max()    

		# pass plot_name (string) to file_name that to be used for saveing as. 
		file_name =  plot_name

		# the typ of plot_name is now converted to figure, other than string.
		plot_name = figure(x_axis_label='Date', y_axis_label=line_name,
						y_range=(ymin_1st, ymax_1st), tools=toolkit)
		plot_name.line('Date', line_name,source=source_KPI, color=lineColor, hover_color=HoverColor)
		plot_name.circle('Date', line_name, source=source_KPI, color=lineColor,hover_color=HoverColor)
		plot_name.extra_y_ranges = {bar_name: Range1d(start=ymin_2nd, end=ymax_2nd)}
		plot_name.vbar(x='Date', top=bar_name, width = 0.5,  source=source_KPI,y_range_name=bar_name,hover_color=HoverColor)
		plot_name.add_layout(LinearAxis(y_range_name=bar_name,axis_label= bar_name), 'right')
		plot_name.title.text = line_name
		plot_name.xaxis.formatter=DatetimeTickFormatter(days = formatter_days) 

		#output_file(file_name + '.html')
		#show(plot_name)
		return plot_name


	# In[69]:


	# Write a function to create combined double lines plot with 2 y-axis
	# issue: cannnot put all three plots into one tab. The issue is fixed by define 'return plot_name'

	def doubleline_KPI_plot(line_name1, line_name2, plot_name):
		source_KPI = ColumnDataSource(DetailKPI)
		ymin_1st = DetailKPI[line_name1].min()
		ymax_1st = DetailKPI[line_name1].max()
		ymin_2nd = DetailKPI[line_name2].min()
		ymax_2nd = DetailKPI[line_name2].max()    

		# pass plot_name (string) to file_name that to be used for saveing as. 
		file_name =  plot_name

		# the typ of plot_name is now converted to figure, other than string.
		plot_name = figure(x_axis_label='Date', y_axis_label=line_name1,
						y_range=(ymin_1st, ymax_1st), tools=toolkit)
		plot_name.line('Date', line_name1,source=source_KPI, color=lineColor, hover_color=HoverColor)
		plot_name.circle('Date', line_name1, source=source_KPI, color=lineColor,hover_color=HoverColor)


		# Setting the second y axis range name and range
		plot_name.extra_y_ranges = {line_name2: Range1d(start=ymin_2nd, end=ymax_2nd)}

		# Adding the second axis to the plot.
		plot_name.add_layout(LinearAxis(y_range_name=line_name2,axis_label= line_name2), 'right')

		plot_name.line('Date', line_name2, source=source_KPI, y_range_name=line_name2,hover_color=HoverColor)
		plot_name.circle('Date', line_name2, source=source_KPI,y_range_name=line_name2,hover_color=HoverColor)
		#plot_name.title.text = line_name
		plot_name.xaxis.formatter=DatetimeTickFormatter(days = formatter_days) 

		#show(plot_name)
		return plot_name


	# In[70]:


	#show case1: Box Annotation, upper and lower threshold to be defined


	RRC_Detail = combined_KPI_plot('TPG_RRC Setup Success Rate(%)', 'TPG_RRC Setup Attempt', "RRC_Detail")
	RAB_Detail = combined_KPI_plot('TPG_E-RAB Setup Success Rate(%)', 'TPG_E-RAB Setup Attempt', "RAB_Detail")
	Service_Drop = combined_KPI_plot('TPG_Service Drop Rate(%)', 'TPG_E-RAB Abnormal Release', "Service_Drop")

	Intra_HO = combined_KPI_plot('TPG_Intra-frequency Handover Out Success Rate(%)', 'TPG_Intra-frequency HO Out Attempt', "Intra_HO")
	Inter_FddTdd_HO = combined_KPI_plot('TPG_Inter-FddTdd Handover Out Success Rate(%)', 'TPG_Inter-FddTdd HO Out Attempt', "Inter_FddTdd_HO")


	User_throughput = doubleline_KPI_plot('TPG_User Downlink Average Throughput(Mbps)', 'TPG_User Uplink Average Throughput(Mbps)',
										  'User_throughput')
	Cell_throughput = doubleline_KPI_plot('TPG_Cell Downlink Average Throughput(Mbps)', 'TPG_Cell Uplink Average Throughput(Mbps)',
										  'Cell_throughput')

	#Add box annotations
	box_annotations (99.6, 99.4, RRC_Detail)
	box_annotations (99.75, 99.69, RAB_Detail)
	box_annotations (0.6, 0.5, Service_Drop)
	box_annotations (99.99, 99.89, Intra_HO)
	box_annotations (99.4, 99.3, Inter_FddTdd_HO)


	layout_show_case_1 = gridplot([[RRC_Detail,RAB_Detail], [Service_Drop,None],
								   [Intra_HO,Inter_FddTdd_HO],[User_throughput,Cell_throughput]],toolbar_location='right')


	#show(layout_show_case_1)


	# In[71]:


	#show case2: band Annotation, 68–95–99.7 rule https://en.wikipedia.org/wiki/68%E2%80%9395%E2%80%9399.7_rule
	RRC_Detail = combined_KPI_plot('TPG_RRC Setup Success Rate(%)', 'TPG_RRC Setup Attempt', "RRC_Detail")
	RAB_Detail = combined_KPI_plot('TPG_E-RAB Setup Success Rate(%)', 'TPG_E-RAB Setup Attempt', "RAB_Detail")
	Service_Drop = combined_KPI_plot('TPG_Service Drop Rate(%)', 'TPG_E-RAB Abnormal Release', "Service_Drop")

	Intra_HO = combined_KPI_plot('TPG_Intra-frequency Handover Out Success Rate(%)', 'TPG_Intra-frequency HO Out Attempt', "Intra_HO")
	Inter_FddTdd_HO = combined_KPI_plot('TPG_Inter-FddTdd Handover Out Success Rate(%)', 'TPG_Inter-FddTdd HO Out Attempt', "Inter_FddTdd_HO")

	User_throughput = doubleline_KPI_plot('TPG_User Downlink Average Throughput(Mbps)', 'TPG_User Uplink Average Throughput(Mbps)',
										  'User_throughput')
	Cell_throughput = doubleline_KPI_plot('TPG_Cell Downlink Average Throughput(Mbps)', 'TPG_Cell Uplink Average Throughput(Mbps)',
										  'Cell_throughput')

	# Add band annotations
	band_annotations ('TPG_RRC Setup Success Rate(%)', RRC_Detail)
	band_annotations ('TPG_E-RAB Setup Success Rate(%)', RAB_Detail)
	band_annotations ('TPG_Service Drop Rate(%)', Service_Drop)
	band_annotations ('TPG_Intra-frequency Handover Out Success Rate(%)', Intra_HO)
	band_annotations ('TPG_Inter-FddTdd Handover Out Success Rate(%)', Inter_FddTdd_HO)

	layout_show_case_2 = gridplot([[RRC_Detail,RAB_Detail], [Service_Drop,None],
								   [Intra_HO,Inter_FddTdd_HO],[User_throughput,Cell_throughput]],toolbar_location='right')
	#show(layout_show_case_2)


	# In[72]:


	#show case3: apply band Annotation, replace mean by KPI baseline
	RRC_Detail = combined_KPI_plot('TPG_RRC Setup Success Rate(%)', 'TPG_RRC Setup Attempt', "RRC_Detail")
	RAB_Detail = combined_KPI_plot('TPG_E-RAB Setup Success Rate(%)', 'TPG_E-RAB Setup Attempt', "RAB_Detail")
	Service_Drop = combined_KPI_plot('TPG_Service Drop Rate(%)', 'TPG_E-RAB Abnormal Release', "Service_Drop")

	Intra_HO = combined_KPI_plot('TPG_Intra-frequency Handover Out Success Rate(%)', 'TPG_Intra-frequency HO Out Attempt', "Intra_HO")
	Inter_FddTdd_HO = combined_KPI_plot('TPG_Inter-FddTdd Handover Out Success Rate(%)', 'TPG_Inter-FddTdd HO Out Attempt', "Inter_FddTdd_HO")

	User_throughput = doubleline_KPI_plot('TPG_User Downlink Average Throughput(Mbps)', 'TPG_User Uplink Average Throughput(Mbps)',
										  'User_throughput')
	Cell_throughput = doubleline_KPI_plot('TPG_Cell Downlink Average Throughput(Mbps)', 'TPG_Cell Uplink Average Throughput(Mbps)',
										  'Cell_throughput')

	# Add band annotations
	baseline_annotations('TPG_RRC Setup Success Rate(%)', RRC_Detail, 99.4)
	baseline_annotations('TPG_E-RAB Setup Success Rate(%)', RAB_Detail, 99.8)
	baseline_annotations('TPG_Service Drop Rate(%)', Service_Drop, 0.5)
	baseline_annotations('TPG_Intra-frequency Handover Out Success Rate(%)', Intra_HO, 99.8)
	baseline_annotations('TPG_Inter-FddTdd Handover Out Success Rate(%)', Inter_FddTdd_HO, 99.4)


	layout_show_case_3 = gridplot([[RRC_Detail,RAB_Detail], [Service_Drop,None],
								   [Intra_HO,Inter_FddTdd_HO],[User_throughput,Cell_throughput]],toolbar_location='right')
	#show(layout_show_case_3)


	# In[73]:


	# define tabs
	show_case_1 = Panel(child=layout_show_case_1, title='box annotations')
	show_case_2 = Panel(child=layout_show_case_2, title='band annotations')
	show_case_3 = Panel(child=layout_show_case_3, title='baseline annotations')

	# Put the Panels in a Tabs object
	layout_tabs = Tabs(tabs=[show_case_1, show_case_2, show_case_3])

	# Due to the dejango constraint, comment out the display of Sample.html which has multiple tabs.
	#output_file('Sample.html')
	#show(layout_tabs)

	return layout_show_case_2
