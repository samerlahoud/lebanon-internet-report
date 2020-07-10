import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

plt.rcParams['font.family'] = 'sans'
plt.rcParams['font.serif'] = 'Open Sans'

base_folder = '../data/'
selected_countries = ['AE','BH','IQ','IR','JO','KW','LB','OM','PS','QA','SA','SY','TR','YE']

global_as_stats_df = pd.read_csv(base_folder+'country-as-stats.csv', sep=',',index_col=0)
global_as_stats_df.sort_index(inplace=True)

global_ip_stats_dict = {}
for cc in selected_countries:
    country_asn_ip_stats_df = pd.read_csv(base_folder+'{}-asn-ip-stats.csv'.format(cc), sep=',',index_col=0)
    global_ip_stats_dict[cc] = [sum(country_asn_ip_stats_df['prefix_v4']),sum(country_asn_ip_stats_df['ips_v4']),sum(country_asn_ip_stats_df['prefix_v6']), sum(country_asn_ip_stats_df['48s_v6'])]

global_ip_stats_df = pd.DataFrame.from_dict(global_ip_stats_dict,orient='index',columns=['prefix_v4', 'ips_v4', 'prefix_v6', '48s_v6'])

plt.figure()
global_as_stats_df.plot.bar()
plt.legend(['Registered ASes', 'Routed ASes'])
plt.ylabel('Number of ASes (in log scale)')
plt.yscale('log')
plt.savefig('../output/as-stat.pdf', format='pdf', bbox_inches='tight')

plt.figure()
global_ip_stats_df['prefix_v4'].plot.bar()
plt.ylabel('Number of announced IPv4 prefixes')
plt.savefig('../output/prefix-v4.pdf', format='pdf', bbox_inches='tight')

plt.figure()
global_ip_stats_df['ips_v4'].plot.bar()
plt.yscale('log')
plt.ylabel('Total amount of announced IPv4 address space \n(in terms of unique IP addresses)')
plt.savefig('../output/ips-v4.pdf', format='pdf', bbox_inches='tight')

plt.figure()
global_ip_stats_df['prefix_v6'].plot.bar()
plt.ylabel('Number of announced IPv6 prefixes')
plt.savefig('../output/prefix-v6.pdf', format='pdf', bbox_inches='tight')

plt.figure()
ax = global_ip_stats_df['ips_v4'].plot.bar()

# for p in ax.patches:
#     ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))

plt.yscale('log')
plt.ylabel('Total amount of announced IPv6 address space \n(in terms of unique /48 subnets)')
plt.savefig('../output/48s-v6.pdf', format='pdf', bbox_inches='tight')


