import datetime
import os
import csv
import shutil

todays_date = datetime.datetime.today()
city_names = ['bangalore', 'mumbai']
# Functions
# Get product master data
try:
    with open('product_master.csv', 'r') as prd_master:
        prd_master_csv_obj = csv.reader(prd_master)
        prd_master_header = next(prd_master_csv_obj)
        product_master_dict = {}
        for row in prd_master_csv_obj:
            product_master_dict[row[0]] = int(row[2])
except Exception as e:
    print(e)


def empty_field_validation(content):
    for val in content:
        if val == '':
            return False
    return True


def product_id_validation(order_id, product_master_ids):
    if order_id not in product_master_ids:
        return False
    return True


def order_date_validation(order_date):
    content_date = datetime.datetime.strptime(order_date, '%m/%d/%Y')
    if content_date > todays_date:
        return False
    return True


def city_validation(city_name):
    if city_name not in city_names:
        return False
    return True


def total_sales_validation(content):
    product_id = content[2]
    product_quantity = int(content[3])
    total_price_actual = int(content[4])
    product_master_price = product_master_dict[product_id]
    total_price_expected = product_master_price * product_quantity
    if total_price_expected != total_price_actual:
        return False
    return True


def create_rejected_folder():
    error_file_folder = 'rejected_files'
    error_file_path = os.path.join(error_file_folder, folder_name)
    if not os.path.exists(error_file_path):
        os.mkdir(error_file_path)
    return True


def generate_rejection_file(is_file_contains_error):
    if is_file_contains_error:
        if create_rejected_folder():
            files_full_path = f'rejected_files/{folder_name}'
            error_file_header = ['order_id', 'order_date', 'product_id', 'quantity', 'sales', 'city', 'errors']
            error_file_name = f'error_{file.replace(".csv", "")}'
            with open(f'{files_full_path}/{error_file_name}.csv', 'w', newline="") as e_file:
                writer = csv.DictWriter(e_file, fieldnames=error_file_header)
                writer.writeheader()
                for key, val in final_dict.items():
                    if val.get('errors'):
                        writer.writerow(val)


def create_success_folder():
    error_file_folder = 'successful_files'
    error_file_path = os.path.join(error_file_folder, folder_name)
    if not os.path.exists(error_file_path):
        os.mkdir(error_file_path)
    return True

try:
    today_date = todays_date.strftime("%d")
    today_month = todays_date.strftime("%m")
    today_year = todays_date.strftime("%Y")
    folder_name = f"{today_year}{today_month}{today_date}"
    files_full_path = f'incoming_files/{folder_name}'
    files_list = os.listdir(files_full_path)
    for file in files_list:
        is_file_contains_error = False
        final_dict = {}
        with open(f'{files_full_path}/{file}', 'r') as f1:
            print(f"File is opned ------> {file}")
            csvreader_obj = csv.reader(f1)
            file_header = next(csvreader_obj)
            cnt = 0
            for row in csvreader_obj:
                rows_validation = []
                row_dict ={
                    'order_id': row[0],
                    'order_date': row[1],
                    'product_id': row[2],
                    'quantity': row[3],
                    'sales': row[4],
                    'city': row[5]
                }
                if not empty_field_validation(row):
                    is_file_contains_error = True
                    rows_validation.append('found blank field')
                if not product_id_validation(row[2], list(product_master_dict.keys())):
                    is_file_contains_error = True
                    rows_validation.append('product id does not exists in product master data')
                if not order_date_validation(row[1]):
                    is_file_contains_error = True
                    rows_validation.append('order date contains future date')
                if not city_validation(row[5].lower()):
                    is_file_contains_error = True
                    rows_validation.append('city name not found')
                if not total_sales_validation(row):
                    is_file_contains_error = True
                    rows_validation.append('total sales issue')
                if len(rows_validation) > 0:
                    is_file_contains_error = True
                    row_dict['errors'] = rows_validation

                final_dict[cnt] = row_dict
                cnt += 1
            print(final_dict)
        if is_file_contains_error:
            print('Issue exists in file - hence moving to reject file')
            generate_rejection_file(is_file_contains_error)
        else:
            print('No issues observed')
            create_success_folder()
            destination_file_path = f'successful_files/{folder_name}'
            shutil.copy(f'{files_full_path}/{file}', destination_file_path)

except Exception as e:
    print('This is exception block : ', e)
