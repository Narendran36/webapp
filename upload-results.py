import argparse
import requests
from datetime import datetime

#usage: python3 upload-results.py --host $ --api_key $ --engagement_name $ --scanner $ --product_name $ --result_file $ --tag $

parser = argparse.ArgumentParser(description='CI/CD integration for DefectDojo')
parser.add_argument('--host', help="DefectDojo Hostname", required=True)
parser.add_argument('--api_key', help="API Key", required=True)
parser.add_argument('--engagement_name', help="Engagement ID (optional)", required=True)
parser.add_argument('--scanner', help="Type of scanner", required=True)
parser.add_argument('--product_name', help="DefectDojo Product ID", required=False)
parser.add_argument('--result_file', help="Path to the file to be uploaded including the file name inside the jenkins ", required=True)
parser.add_argument('--tag', help="name of the file to be uploaded", required=False)



args = vars(parser.parse_args())
host = args["host"]
api_key = args["api_key"]
product_name = args["product_name"]
scanner = args["scanner"]
engagement_id = args["engagement_name"]
path = args["result_file"]
tag = args["tag"]

url = "http://"+host+"/api/v2/import-scan/"



payload={'verified': 'true',
'tags': tag,
'scan_date' : datetime.now().strftime("%Y-%m-%d"),
'scan_type': scanner,
'minimum_severity': 'Info',
'skip_duplicates': 'true',
'close_old_findings': 'false',
'product_name': product_name,
'engagement_name': engagement_id }
files=[
  ('file ',(path,open(path,'rb'),'application/octet-stream'))
]
headers = {
  'Authorization': 'Token '+ api_key
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)
