import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plotNumberOfScans(column,target):
	hist = pd.read_csv('../files/history.csv',parse_dates =['date'])
	res = hist[hist[column] == target]
	dim = (5,3)
	sns.catplot(x=column, hue="response", kind="count" ,data=res,height = dim[1],aspect = dim[0]/dim[1])
	plt.savefig('../assets/'+column+'.png')
