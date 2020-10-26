import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import datetime

def plotNumberOfScans(column,target):
	hist = pd.read_csv('../files/history.csv',parse_dates =['date'])
	res = hist[hist[column] == target]
	data = res.groupby("response")["reference"].count()
	pie, ax = plt.subplots(figsize=[5,3])
	labels = list(data.keys())
	for i in range(len(labels)):
		labels[i] = str(data[labels[i]].item()) + ', '+ labels[i]
	plt.pie(x=data, autopct="%.1f%%", explode=[0.05]*len(labels), labels=labels, pctdistance=0.5)
	if column == "username":
		plt.title("Number of successful/failed scans by "+target, fontsize=14)
	else:
		plt.title("Number of successful/failed scans of "+target, fontsize=14)
	plt.savefig('../assets/'+column+'.png')


def plotDate(date_type,user=None):
	hist = pd.read_csv('../files/history.csv',parse_dates =['date'])
	if user is not None:
		hist = hist[hist['username'] == user]
	hist['date'] = pd.to_datetime(hist['date'])
	if date_type == "day":
		hist['date'] = hist['date'].dt.day
	elif date_type == "week":
		hist['date'] = hist['date'].dt.week
	elif date_type == "month":
		hist['date'] = hist['date'].dt.month
	elif date_type == "year":
		hist['date'] = hist['date'].dt.year
	hist = hist.groupby(['date','response']).size().to_frame()
	hist[0].unstack(level=-1).plot(kind='bar', figsize = (5,3),rot = 0)
	plt.xlabel("")
	if user is not None:
		plt.savefig('../assets/userdate.png')
	else:
		plt.savefig('../assets/date.png')

if __name__ == '__main__':
	plotDate('day')