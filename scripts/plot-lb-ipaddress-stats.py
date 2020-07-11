import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

plt.rcParams['font.family'] = 'sans'
plt.rcParams['font.serif'] = 'Open Sans'

base_folder = '../data/'

country_ip_stats_dict = {}
country_code = 'LB'
min_year = 2010
max_year = 2020
top_ips_v4_perc_df = pd.DataFrame()
for year in range(min_year,max_year+1):
    country_ip_stats_df = pd.read_csv(base_folder+'{}-asn-ip-stats-{}.csv'.format(country_code,year), sep=',',index_col=0)
    country_ip_stats_df['ips_v4_perc'] = 100*country_ip_stats_df['ips_v4']/sum(country_ip_stats_df['ips_v4'])
    top_ips_v4_perc  = country_ip_stats_df.nlargest(8,'ips_v4_perc')['ips_v4_perc']
    
    df0 = pd.DataFrame(top_ips_v4_perc.rename(year))
    top_ips_v4_perc_df = pd.concat([top_ips_v4_perc_df, df0], axis=1)
    country_ip_stats_dict[year] = [sum(country_ip_stats_df['prefix_v4']),sum(country_ip_stats_df['ips_v4']),sum(country_ip_stats_df['prefix_v6']), sum(country_ip_stats_df['48s_v6'])]

country_ip_evolution_stats_df = pd.DataFrame.from_dict(country_ip_stats_dict,orient='index',columns=['prefix_v4', 'ips_v4', 'prefix_v6', '48s_v6'])
top_ips_v4_perc_df.fillna(0,inplace=True)
top_ips_v4_perc_df.sort_values(min_year,ascending=0,inplace=True)

plt.figure()
ax = top_ips_v4_perc_df.transpose().plot.bar(stacked=True)
plt.ylabel('Percentage of announced IPv4 address space \n(in terms of unique IP addresses)')
ax.legend(bbox_to_anchor=(1.3, 1.0), loc='upper right')
plt.savefig('../output/{}-top-ips-v4.pdf'.format(country_code), format='pdf', bbox_inches='tight')

plt.figure()
country_ip_evolution_stats_df['prefix_v4'].plot.line(marker='o')
plt.xlim(min_year-1, max_year+1)
plt.ylabel('Number of announced IPv4 prefixes')
plt.savefig('../output/{}-prefix-v4.pdf'.format(country_code), format='pdf', bbox_inches='tight')

plt.figure()
country_ip_evolution_stats_df['ips_v4'].plot.line(marker='o')
plt.xlim(min_year-1, max_year+1)
plt.ylabel('Total amount of announced IPv4 address space \n(in terms of unique IP addresses)')
plt.savefig('../output/{}-ips-v4.pdf'.format(country_code), format='pdf', bbox_inches='tight')

plt.figure()
country_ip_evolution_stats_df['prefix_v6'].plot.line(marker='o')
plt.xlim(min_year-1, max_year+1)
plt.ylabel('Number of announced IPv6 prefixes')
plt.savefig('../output/{}-prefix-v6.pdf'.format(country_code), format='pdf', bbox_inches='tight')

plt.figure()
country_ip_evolution_stats_df['48s_v6'].plot.line(marker='o')
plt.xlim(min_year-1, max_year+1)
plt.ylabel('Total amount of announced IPv6 address space \n(in terms of unique /48 subnets)')
plt.savefig('../output/{}-48s-v6.pdf'.format(country_code), format='pdf', bbox_inches='tight')
