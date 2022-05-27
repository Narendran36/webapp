import argparse
import requests
from datetime import datetime

#usage: python3 upload-results.py --host $ --api_key $ --engagement_name $ --scanner $ --product_name $ --file_path $ 

parser = argparse.ArgumentParser(description='CI/CD integration for DefectDojo')
parser.add_argument('--host', help="DefectDojo Hostname", required=True)
parser.add_argument('--api_key', help="API Key", required=True)
parser.add_argument('--engagement_name', help="Engagement ID (optional)", required=True)
parser.add_argument('--scanner', help="Type of scanner", required=True)
parser.add_argument('--product_name', help="DefectDojo Product ID", required=False)
parser.add_argument('--file_path', help="Path to the file to be uploaded including the file name inside the jenkins ", required=True)
#parser.add_argument('--file_name', help="name of the file to be uploaded", required=True)



args = vars(parser.parse_args())
host = args["host"]
api_key = args["api_key"]
product_name = args["product_name"]
scanner = args["scanner"]
engagement_id = args["engagement_name"]
path = args["file_path"]
#name = args["file_name"]

url = "http://"+host+"/api/v2/import-scan/"



payload={'verified': 'true',
'tags': 'test',
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
