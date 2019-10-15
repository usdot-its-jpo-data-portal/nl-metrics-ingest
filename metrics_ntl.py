import csv
import pandas as pd
import json
import requests
import yaml
from argparse import ArgumentParser
from googleapiclient.http import MediaFileUpload
from googleapiclient import discovery
from google.oauth2 import service_account

XLS_FILE_PATH = 'data.xlsx'
CSV_VIEWS_FILE_PATH = 'views.csv'
CSV_DOWNLOADS_FILE_PATH = 'downloads.csv'
CONFIG_FILE_PATH = 'config.yml'


def main():
    argparser = ArgumentParser()
    group = argparser.add_mutually_exclusive_group(required=True)
    group.add_argument('--csv', action='store_true')
    group.add_argument('--xls', action='store_true')
    args = argparser.parse_args()

    value_range_body = {'values': []}

    if args.csv:
        views_list = parse_csv(CSV_VIEWS_FILE_PATH)
        downloads_list = parse_csv(CSV_DOWNLOADS_FILE_PATH)
        assert len(views_list) == len(downloads_list), "Failed to match CSV files, mismatched data lengths. Found %d entries in views file but %d entries in downloads file." % (len(views_list), len(downloads_list))

        value_range_values = []
        for index in range(len(views_list)):
            views_ds_name = views_list[index]['dataset_name']
            downloads_ds_name = downloads_list[index]['dataset_name']
            assert views_ds_name == downloads_ds_name, "Failed to match CSV files, mismatched dataset names: '%s' in views file but '%s' in downloads file." % (views_ds_name, downloads_ds_name)
            value_range_values.append([str(views_ds_name), str(views_list[index]['count']), str(downloads_list[index]['count']), str(views_list[index]['total']), str(downloads_list[index]['total'])])

    elif args.xls:
        value_range_values = parse_xls(XLS_FILE_PATH)

    value_range_body['values'] = value_range_values

    with open(CONFIG_FILE_PATH, 'r') as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)
    credentials = get_credentials(config)
    service = discovery.build('sheets', 'v4', credentials=credentials)
    spreadsheet_id = config["spreadsheet_id_ntl"]
    spreadsheetRange = "A2:E" + str(len(value_range_body['values']) + 1)
    value_input_option = 'USER_ENTERED'

    print(json.dumps(value_range_body, indent=4, sort_keys=True))
    request = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=spreadsheetRange, valueInputOption=value_input_option, body=value_range_body)
    response = request.execute()
    print(response)

def get_credentials(config):
    service_account_info = json.loads(config["google_api_credentials"])
    credentials = service_account.Credentials.from_service_account_info(service_account_info)
    return credentials

def parse_csv(filepath):
    csv_iter = pd.read_csv(filepath, encoding='utf-8').iterrows()
    headers = next(csv_iter)

    data_list = []
    for index, row in csv_iter:
        if pd.notna(row.iloc[0]) and row.iloc[2] == 'Dataset':
            dataset_name = row.iloc[0]
            count = row.iloc[-1]
            total = sum(row.iloc[6:])
            data_list.append({
                'dataset_name': dataset_name,
                'count': count,
                'total': total})
    return data_list

def parse_xls(filepath):
    xls = pd.ExcelFile(filepath)

    downloads_df = pd.read_excel(xls, 'downloads')
    views_df = pd.read_excel(xls, 'views')

    value_range_values = []

    for index, row in downloads_df.iterrows():
        dataset = views_df.iloc[index, 0]
        if pd.notna(dataset) and views_df.iloc[index, 2] == 'Dataset':
            lm_views = views_df.iloc[index, -3]
            total_views = views_df.iloc[index, -2]
            lm_downloads = downloads_df.iloc[index, -3]
            total_downloads = downloads_df.iloc[index, -2]
            value_range_values.append([str(dataset), str(lm_views), str(lm_downloads), str(total_views), str(total_downloads)])

    return value_range_values


if __name__ == "__main__":
    main()
