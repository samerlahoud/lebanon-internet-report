import json
import requests
import time
import pandas as pd

api_url_base = 'https://stat.ripe.net/data/'

def get_country_asn(country_code):
    api_url = '{}country-asns/data.json?resource={}&lod=1'.format(api_url_base, country_code)
    response = requests.get(api_url)
    if response.status_code == 200:
        country_asn_json = json.loads(response.content.decode('utf-8'))
        country_asn_list = country_asn_json["data"]["countries"][0]["routed"]
        country_asn_stats = country_asn_json["data"]["countries"][0]["stats"]
        return country_asn_list, country_asn_stats
    else:
        return None

def get_asn_prefix(asn):
    api_url = '{}routing-status/data.json?resource={}'.format(api_url_base, asn)
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

def get_country_stats(country_code):
    asn_results = {}
    country_asn_list, country_asn_stats = get_country_asn(country_code)
    for asn in country_asn_list:
        temp_result = get_asn_prefix(asn)
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

if __name__ == "__main__":
    selected_countries = ['AE','BH','EG','IQ','IR','JO','KW','LB','OM','PS','QA','SA','SY','TR','YE']
    
    get_global_stats(selected_countries)
    #get_country_stats('PS')