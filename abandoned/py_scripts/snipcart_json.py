import os,sys

apikey = os.environ.get("TD_API_KEY")
apiserver = os.environ.get("TD_API_SERVER")
snipcart_apikey = os.environ.get("SNIPCART_API_KEY")
snipcart_pass = os.environ.get("SNIPCART_PASSWD")

def write_abandoned_to_table_by_json(url, database, table):
    os.system(f"{sys.executable} -m pip install requests")
    os.system(f"{sys.executable} -m pip install --upgrade pytd")

    import requests
    import pytd
    import pandas as pd
    import json
    from pandas.io.json import json_normalize

    r = requests.get(url,headers={"Accept":"application/json"},auth=requests.auth.HTTPBasicAuth(snipcart_apikey, snipcart_pass))

    print(f"statusCode: {r.status_code}")
    items = []
    if (r.status_code == 200):
      json_dict = json.loads(r.text)
      df_json = json_normalize(json_dict['items'])

      ## Debug
      print(df_json)

      client = pytd.Client(apikey=apikey, endpoint=apiserver, database=database)
      client.create_database_if_not_exists(database)
      client.load_table_from_dataframe(df_json, table, if_exists="append")