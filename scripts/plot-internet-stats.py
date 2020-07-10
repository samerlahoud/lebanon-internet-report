import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

plt.rcParams['font.family'] = 'sans'
plt.rcParams['font.serif'] = 'Open Sans'
#plt.rcParams['axes.labelsize'] = 14
#plt.rcParams.update({'font.size': 12})

# data from https://databank.worldbank.org/
base_folder = '../data/Data_Extract_From_World_Development_Indicators/'
#selected_countries = ['YEM','SYR','MEA','LBN','QAT','KWT']
selected_countries = ['LBN','MEA','QAT','YEM']

stat_df = pd.read_csv(base_folder+'42da6ae7-a256-443d-ab20-466f2cbbba13_Data.csv', sep=',', index_col='Country Code')

total_population_df = stat_df.loc[stat_df['Series Code'] == 'SP.POP.TOTL']
internet_users_df = stat_df.loc[stat_df['Series Code'] == 'IT.NET.USER.ZS']
mobile_users_df = stat_df.loc[stat_df['Series Code'] == 'IT.CEL.SETS.P2']
bbnd_fixed_users_df = stat_df.loc[stat_df['Series Code'] == 'IT.NET.BBND.P2']

# Total population
total_population_df = total_population_df.drop(columns=['Series Name', 'Series Code', 'Country Name']).transpose()
total_population_df.index = total_population_df.index.str.split(" ").str[0]
total_population_df = total_population_df.drop(['2018', '2019'])
total_population_df = total_population_df.replace('..','0')
total_population_df = total_population_df.astype('float64')
subset_total_population_df = total_population_df[selected_countries]

# Internet users
internet_users_df = internet_users_df.drop(columns=['Series Name', 'Series Code', 'Country Name']).transpose()
internet_users_df.index = internet_users_df.index.str.split(" ").str[0]
internet_users_df = internet_users_df.drop(['2018', '2019'])
internet_users_df = internet_users_df.replace('..','0')
internet_users_df = internet_users_df.astype('float64')
#internet_users_df = internet_users_df.sort_values(by=['2017 [YR2017]'], axis=1, ascending=True, inplace=False, kind='quicksort', na_position='last')
#subset_internet_users_df = internet_users_df[['YEM','SYR','MEA','LBN','QAT','KWT']]
subset_internet_users_df = internet_users_df[selected_countries]

# Mobile users
mobile_users_df = mobile_users_df.drop(columns=['Series Name', 'Series Code', 'Country Name']).transpose()
mobile_users_df.index = mobile_users_df.index.str.split(" ").str[0]
mobile_users_df = mobile_users_df.drop(['2019'])
mobile_users_df = mobile_users_df.replace('..','0')
mobile_users_df = mobile_users_df.astype('float64')
subset_mobile_users_df = mobile_users_df[selected_countries]

# Fixed broadband users
bbnd_fixed_users_df = bbnd_fixed_users_df.drop(columns=['Series Name', 'Series Code', 'Country Name']).transpose()
bbnd_fixed_users_df.index = bbnd_fixed_users_df.index.str.split(" ").str[0]
bbnd_fixed_users_df = bbnd_fixed_users_df.drop(['2019'])
bbnd_fixed_users_df = bbnd_fixed_users_df.replace('..','0')
bbnd_fixed_users_df = bbnd_fixed_users_df.astype('float64')
subset_bbnd_fixed_users_df = bbnd_fixed_users_df[selected_countries]

plt.figure()
subset_internet_users_df.plot.line(marker='o')
plt.ylabel("Individuals using the Internet \n(% of population)")
plt.savefig('../output/internet-users.pdf', format='pdf', bbox_inches='tight')

plt.figure()
subset_mobile_users_df.plot.line(marker='o')
plt.ylabel("Mobile cellular subscriptions \n(per 100 people)")
plt.savefig('../output/mobile-users.pdf', format='pdf', bbox_inches='tight')

plt.figure()
subset_bbnd_fixed_users_df.plot.line(marker='o')
plt.ylabel("Fixed broadband subscriptions \n(per 100 people)")
plt.savefig('../output/fixed-bbnd-users.pdf', format='pdf', bbox_inches='tight')

abs_internet_users_lbn = subset_internet_users_df["LBN"]/100 * subset_total_population_df["LBN"]/1e6
total_population_lbn = subset_total_population_df["LBN"]/1e6
plt.figure()
abs_internet_users_lbn.plot.line(marker='o')
plt.legend(["Individuals using the Internet"])
total_population_lbn.plot.area(alpha=0.1)
plt.ylabel("Total population (millions)")
plt.savefig('../output/population-internet-lbn.pdf', format='pdf', bbox_inches='tight')

aggregate_lbn_users = pd.DataFrame({"Fixed broadband subscriptions":subset_bbnd_fixed_users_df["LBN"],"Mobile cellular subscriptions":subset_mobile_users_df["LBN"]})
plt.figure()
aggregate_lbn_users.plot.bar()
plt.ylim(0, 100) 
plt.ylabel("Percentage of population")
plt.savefig('../output/aggregate-lbs-users.pdf', format='pdf', bbox_inches='tight')