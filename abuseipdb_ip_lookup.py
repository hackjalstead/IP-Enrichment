
import requests
import pandas as pd
import time

API_KEY = 'PUT_UR_API_KEY_HERE'
url = "https://api.abuseipdb.com/api/v2/check"
df = pd.read_csv('ips.csv')
df.columns = ['IP']


######################################################
headers = {
    'Accept': 'application/json',
    'Key': API_KEY
}
def check_ip(ip):
    try:
        params = {
            'ipAddress': ip,
            'maxAgeInDays': 90
        }
        response = requests.get(url, headers=headers, params=params)
        data = response.json()['data']
        return {
            'IP': ip,
            'Abuse Score': data['abuseConfidenceScore'],
            'Country': data.get('countryCode', 'N/A'),
            'ISP': data.get('isp', 'N/A'),
            'Domain': data.get('domain', 'N/A'),
            'Usage Type': data.get('usageType', 'N/A'),
            'Total Reports': data['totalReports'],
            'Last Reported At': data.get('lastReportedAt', 'N/A')
        }
    except Exception as e:
        return {'IP': ip, 'Error': str(e)}
results = []
for ip in df['IP'].dropna().unique():
    results.append(check_ip(ip))
    time.sleep(1.4) #depending on ur abuseIPBD subscription plan, u can adjust this. 

result_df = pd.DataFrame(results)
result_df.to_csv('abuseipdb_results.csv', index=False)
print("Results saved to 'abuseipdb_results.csv'")
