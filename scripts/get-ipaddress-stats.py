import json
import requests
import time
import pandas as pd
import re
from time import gmtime, strftime
from datetime import date, timedelta

api_url_base = 'https://stat.ripe.net/data/'

def get_country_asn(country_code):
    api_url = '{}country-asns/data.json?resource={}&lod=1'.format(api_url_base, country_code)
    response = requests.get(api_url)
    if response.status_code == 200:
        country_asn_json = json.loads(response.content.decode('utf-8'))
        country_asn_list = country_asn_json["data"]["countries"][0]["routed"]
        country_asn_list = re.findall(r'\((.*?)\)', country_asn_list)
        country_asn_stats = country_asn_json["data"]["countries"][0]["stats"]
        return country_asn_list, country_asn_stats
    else:
        return None

def get_asn_prefix(asn, timestamp):
    api_url = '{}routing-status/data.json?resource={}&timestamp={}'.format(api_url_base, asn, timestamp)
    time.sleep(3)
    response = requests.get(api_url)
    if response.status_code == 200:
        asn_prefix_json = json.loads(response.content.decode('utf-8'))
        asn_prefix_v4 = asn_prefix_json["data"]["announced_space"]["v4"]["prefixes"]
        asn_ips_v4 = asn_prefix_json["data"]["announced_space"]["v4"]["ips"]
        asn_prefix_v6 = asn_prefix_json["data"]["announced_space"]["v6"]["prefixes"]
        asn_48s_v6 = asn_prefix_json["data"]["announced_space"]["v6"]["48s"]
        return [asn_prefix_v4, asn_ips_v4, asn_prefix_v6, asn_48s_v6]
    else:
        return None

def get_detailed_country_stats(country_code):
    asn_results = {}
    current_time = date.today()+timedelta(hours=-2)
    timestamp = current_time.strftime("%Y-%m-%dT12:00")
    country_asn_list, country_asn_stats = get_country_asn(country_code)
    for asn in country_asn_list:
        temp_result = get_asn_prefix(asn, timestamp)
        if(temp_result):
            asn_results[asn] = temp_result
    asn_results_df=pd.DataFrame.from_dict(asn_results, orient='index',columns=['prefix_v4', 'ips_v4', 'prefix_v6', '48s_v6'])
    asn_results_df.to_csv('../data/{}-asn-ip-stats.csv'.format(country_code))

def get_global_stats(country_list):
    country_results = {}
    for country_code in selected_countries:
        country_asn_list, country_asn_stats = get_country_asn(country_code)
        country_results[country_code] = [country_asn_stats['registered'],country_asn_stats['routed']]
    country_results_df=pd.DataFrame.from_dict(country_results,orient='index',columns=['registered_as','routed_as'])
    country_results_df.to_csv('../data/country-as-stats.csv')

def get_aggregate_country_stats(cc):
    # IP space is allocated or assigned according to RIRs but not necessarly announced
    api_url = '{}country-resource-list/data.json?resource={}'.format(api_url_base, cc)
    response = requests.get(api_url)
    if response.status_code == 200:
        aggregate_country_json = json.loads(response.content.decode('utf-8'))
        country_asn_list = aggregate_country_json["data"]["resources"]["asn"]
        country_ipv4_list = aggregate_country_json["data"]["resources"]["ipv4"]
        country_ipv6_list = aggregate_country_json["data"]["resources"]["ipv6"]
        nb_asn = len(country_asn_list)
        nb_ipv4_addr = sum([pow(2,32-(int(pref.split('/')[1]))) for pref in country_ipv4_list])
        nb_ipv6_s48 = sum([pow(2,48-(int(pref.split('/')[1]))) for pref in country_ipv6_list])
        return [nb_asn, nb_ipv4_addr, nb_ipv6_s48]
    else:
        return None

def get_detailed_evolution_country_stats(country_code):
    country_asn_list, country_asn_stats = get_country_asn(country_code)
    back_years = 10
    for time_leap in range(back_years,-1,-1):
        asn_results = {}
        timestamp = date.today()+timedelta(days=-time_leap*365)
        timestr = timestamp.strftime("%Y-%m-%dT12:00")
        for asn in country_asn_list:
            temp_result = get_asn_prefix(asn,timestr)
            if(temp_result):
                asn_results[asn] = temp_result
        asn_results_df=pd.DataFrame.from_dict(asn_results, orient='index',columns=['prefix_v4', 'ips_v4', 'prefix_v6', '48s_v6'])
        asn_results_df.to_csv('../data/{}-asn-ip-stats-{}.csv'.format(country_code,timestamp.strftime("%Y")))

if __name__ == "__main__":
    selected_countries = ['AE','BH','EG','IQ','IR','JO','KW','LB','OM','PS','QA','SA','SY','TR','YE']
    
    '''Get global stats for countries'''
    # get_global_stats(selected_countries)

    '''Get detailed country stats per asn'''
    # get_detailed_country_stats('YE')

    '''Get detailed country evolution per asn'''
    get_detailed_evolution_country_stats('LB')