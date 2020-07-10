import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

plt.rcParams['font.family'] = 'sans'
plt.rcParams['font.serif'] = 'Open Sans'

base_folder = '../data/'
selected_countries = ['AE','BH','IQ','IR','JO','KW','LB','OM','PS','QA','SA','SY','TR','YE']
selected_years = ['2017','2018','2019']

global_lir_stats_df = pd.DataFrame(index=selected_countries, columns=selected_years)

for y in selected_years:
    lir_stats_df = pd.read_csv(base_folder+'menog-{}-lirs.csv'.format(y), sep=';',index_col=0)
    global_lir_stats_df[y] = lir_stats_df['LIRs']

plt.figure()
global_lir_stats_df.plot.bar()
plt.ylabel("Number of LIRs")
plt.savefig('../output/lir.pdf', format='pdf', bbox_inches='tight')
