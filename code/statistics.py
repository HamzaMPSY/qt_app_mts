import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plotNumberOfScans(column,target):
	hist = pd.read_csv('../files/history.csv',parse_dates =['date'])
	res = hist[hist[column] == target]
	ax  = sns.catplot(x=column, hue="response", kind="count" , data=res)
	plt.show()

if __name__ == '__main__':
	plotNumberOfScans('reference','ref2')

