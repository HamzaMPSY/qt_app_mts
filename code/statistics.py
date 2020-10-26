import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

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

if __name__ == '__main__':
	plotNumberOfScans('reference','ref1')