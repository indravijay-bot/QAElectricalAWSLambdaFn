import json
import requests
from datetime import datetime, timedelta
import calendar
import traceback
import csv
import io
import smtplib
from email.message import EmailMessage

import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Don't fail in Lambda
# def validate_env_vars():
#     required_vars = [
#         "ISOLAR_BASE_URL", "AUTH_ENDPOINT", "DATA_ENDPOINT",
#         "USERNAME", "PASSWORD", "APPKEY", "X_ACCESS_KEY",
#         "EMAIL_FROM", "EMAIL_PASSWORD", "EMAIL_TO_1",
#         "PS_ID_1", "PS_KEY_LIST_1"
#     ]
#     missing = [var for var in required_vars if not os.getenv(var)]
#     if missing:
#         raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

ISOLAR_BASE_URL = os.getenv("ISOLAR_BASE_URL")
AUTH_ENDPOINT =  os.getenv("AUTH_ENDPOINT")
DATA_ENDPOINT = os.getenv("DATA_ENDPOINT")

APPKEY = os.getenv("APPKEY")
X_ACCESS_KEY = os.getenv("X_ACCESS_KEY")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_ADMIN = os.getenv("EMAIL_ADMIN")
QA_EMAIL = os.getenv("QA_EMAIL")
CC_EMAIL_1 = os.getenv("CC_EMAIL_1")
CC_EMAIL_2 = os.getenv("CC_EMAIL_2")
# ISOLAR_BASE_URL = "https://augateway.isolarcloud.com"
# AUTH_ENDPOINT = "/openapi/login"
# DATA_ENDPOINT = "/openapi/getDevicePointsDayMonthYearDataList"

# APPKEY = "63E336200B3A815601344F6DCD1CF555"
# X_ACCESS_KEY = "3238haae1wd2yz445m2gv4tfkqe4icq1"
# USERNAME = "renewables@qaelectrical.com.au"
# PASSWORD = "27Halseyrd"



# EMAIL_FROM = "abhidrive50@gmail.com"
# EMAIL_PASSWORD = "dkhcmysoqhgbeosk"
# EMAIL_ADMIN = "zalaabhi882@gmail.com"

COMMON_HEADERS = {
    'Content-Type': 'application/json;charset=UTF-8',
    'sys_code': '901',
    'x-access-key': X_ACCESS_KEY
}

# === CLIENT CONFIGURATION ===
CLIENTS = [
    {
        "email_to": os.getenv("EMAIL_TO_1"),
        "ps_id": os.getenv("PS_ID_1"),
        "ps_key_list": [os.getenv("PS_KEY_LIST_1")],
        "data_point": "p1",
        "plant_name": "CAH Student Acc. Unit 1",
        "supplier_name": "Colac Area Health",
        "mesurement_device": "Colac_Student_Accommodation1_5_Solar",
        "activity_name": "Solar Power"
    },
    {
        "email_to": os.getenv("EMAIL_TO_1"),
        "ps_id": os.getenv("PS_ID_2"),
        "ps_key_list": [os.getenv("PS_KEY_LIST_2")],
        "data_point": "p1",
        "plant_name": "CAH Student Acc. Unit 2",
        "supplier_name": "QAE",
        "mesurement_device": "Colac_Student_Accommodation2_5_Solar",
        "activity_name": "Solar Power"
    },
    {
        "email_to": os.getenv("EMAIL_TO_1"),
        "ps_id": os.getenv("PS_ID_3"),
        "ps_key_list": [os.getenv("PS_KEY_LIST_3")],
        "data_point": "p1",
        "plant_name": "CAH Student Acc. Unit 3",
        "supplier_name": "QAE",
        "mesurement_device": "Colac_Student_Accommodation3_5_Solar",
        "activity_name": "Solar Power"
    },
    {
        "email_to": os.getenv("EMAIL_TO_1"),
        "ps_id": os.getenv("PS_ID_4"),
        "ps_key_list": [os.getenv("PS_KEY_LIST_4")],
        "data_point": "p1",
        "plant_name": "CAH Student Acc. Unit 4",
        "supplier_name": "QAE",
        "mesurement_device": "Colac_Student_Accommodation4_5_Solar",
        "activity_name": "Solar Power"
    },
    {
        "email_to": os.getenv("EMAIL_TO_1"),
        "ps_id": os.getenv("PS_ID_5"),
        "ps_key_list": [os.getenv("PS_KEY_LIST_5")],
        "data_point": "p1",
        "plant_name": "Timboon hospital",
        "supplier_name": "QAE",
        "mesurement_device": "Timboon hospital_5_Solar",
        "activity_name": "Solar Power"
    }
]
#1553526
# CLIENTS = [
#     {
#         "email_to": "zalaindravijaysinh50@gmail.com",
#         "ps_id": "1552434",
#         "ps_key_list": ["1552434_1_1_1"],
#         "data_point": "p1",
#         "plant_name": "CAH Student Acc. Unit 1",
#         "supplier_name": "Colac Area Health",
#         "mesurement_device": "Colac_Student_Accommodation1_5_Solar",
#         "activity_name": "Solar Power"
#     }
#     # {
#     #     "email_to": os.getenv("EMAIL_TO_1"),
#     #     "ps_id": os.getenv("PS_ID_2"),
#     #     "ps_key_list": [os.getenv("PS_KEY_LIST_2")],
#     #     "data_point": "p1",
#     #     "plant_name": "CAH Student Acc. Unit 2",
#     #     "supplier_name": "QAE",
#     #     "mesurement_device": "Colac_Student_Accommodation2_5_Solar",
#     #     "activity_name": "Solar Power"
#     # },
#     # {
#     #     "email_to": os.getenv("EMAIL_TO_1"),
#     #     "ps_id": os.getenv("PS_ID_3"),
#     #     "ps_key_list": [os.getenv("PS_KEY_LIST_3")],
#     #     "data_point": "p1",
#     #     "plant_name": "CAH Student Acc. Unit 3",
#     #     "supplier_name": "QAE",
#     #     "mesurement_device": "Colac_Student_Accommodation3_5_Solar",
#     #     "activity_name": "Solar Power"
#     # },
#     # {
#     #     "email_to": os.getenv("EMAIL_TO_1"),
#     #     "ps_id": os.getenv("PS_ID_4"),
#     #     "ps_key_list": [os.getenv("PS_KEY_LIST_4")],
#     #     "data_point": "p1",
#     #     "plant_name": "CAH Student Acc. Unit 4",
#     #     "supplier_name": "QAE",
#     #     "mesurement_device": "Colac_Student_Accommodation4_5_Solar",
#     #     "activity_name": "Solar Power"
#     # }
# ]

# === UTILITIES ===

def create_csv_in_memory(data_rows):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerows(data_rows)
    return output.getvalue()

def send_email_with_csv(csv_content, to_email, plant_name):
    msg = EmailMessage()
    cc_addresses = [QA_EMAIL, CC_EMAIL_1, CC_EMAIL_2]
    #cc_address = QA_EMAIL
    msg['Subject'] = f"Monthly Solar Energy Report-{plant_name}"
    msg['From'] = EMAIL_FROM
    msg["To"] = to_email
    msg['Cc'] = ", ".join(cc_addresses)
    msg.set_content('Please find attached the monthly solar energy report for your plant.\n\nBest regards,\nRaj Zala\nQA Electrical')
    msg.add_attachment(csv_content.encode('utf-8'), maintype='text', subtype='csv', filename = f"{plant_name}_data.csv")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_FROM, EMAIL_PASSWORD)
        smtp.send_message(msg)

def get_previous_month_dates():
    today = datetime.utcnow()
    last_day_prev_month = datetime(today.year, today.month, 1) - timedelta(days=1)
    year = last_day_prev_month.year
    month = last_day_prev_month.month
    num_days = calendar.monthrange(year, month)[1]
    return [datetime(year, month, day).strftime("%Y-%m-%d") for day in range(1, num_days + 1)]

def get_auth_token():
    url = f"{ISOLAR_BASE_URL}{AUTH_ENDPOINT}"
    payload = {
        "user_account": USERNAME,
        "user_password": PASSWORD,
        "appkey": APPKEY
    }

    response = requests.post(url, headers=COMMON_HEADERS, json=payload)
    response.raise_for_status()
    data = response.json()

    if data.get("result_code") == "1":
        return data["result_data"]["token"]
    raise ValueError(f"Auth failed: {data.get('result_msg', 'Unknown error')}")

def call_daily_data_api(token, date_str, ps_id, ps_key_list, data_point):
    start_date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    end_date_obj = start_date_obj + timedelta(days=1)

    payload = {
        "data_point": data_point,
        "data_type": "2",
        "start_time": start_date_obj.strftime("%Y%m%d"),
        "end_time": end_date_obj.strftime("%Y%m%d"),
        "query_type": "1",
        "order": 0,
        "ps_key_list": ps_key_list,
        "ps_id": ps_id,
        "token": token,
        "appkey": APPKEY,
        "sys_code": 901
    }

    try:
        response = requests.post(f"{ISOLAR_BASE_URL}{DATA_ENDPOINT}", headers=COMMON_HEADERS, json=payload)
        response.raise_for_status()
        if response.status_code != 200:
         raise RuntimeError(f"API call failed for client {ps_id}: HTTP {response.status_code} - {response.text}")
        data = response.json()

        if data.get("result_msg") != "success":
         raise ValueError(f"API response not successful for client {ps_id}: result_msg={data.get('result_msg')}")


        result_data = data.get("result_data", {})
        ps_key = ps_key_list[0]

        if ps_key not in result_data:
            print(f"{date_str} → No data for {ps_key}.")
            return None

        p_data = result_data[ps_key].get(data_point, [])
        if p_data and "2" in p_data[0]:
            return float(p_data[0]["2"])
        return None
    except Exception as e:
        print(f"{date_str} → API error: {e}")
        return None

# === LAMBDA ENTRY POINT ===

def send_error_email_to_admin(subject, body):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_ADMIN
    msg.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_FROM, EMAIL_PASSWORD)
        smtp.send_message(msg)


def lambda_handler(event=None, context=None):
    try:
        token = get_auth_token()
        dates = get_previous_month_dates()

        for client in CLIENTS:
            try:
                email_to = client["email_to"]
                ps_id = client["ps_id"]
                ps_key_list = client["ps_key_list"]
                data_point = client["data_point"]
                plant_name = client["plant_name"]
                supplier_name = client["supplier_name"]
                mesurement_device = client["mesurement_device"]
                activity_name = client['activity_name']

                print(f"📩 Processing for client: {email_to}")
                data_rows = [(
                    "Supplier Name",
                    "Measurement Device",
                    "Start Datetime",
                    "Stop Datetime",
                    "Measured Quantity",
                    "Measurement Unit",
                    "Activity Name"
                )]
                valid_data = True
                for date_str in dates:
                    value = call_daily_data_api(token, date_str, ps_id, ps_key_list, data_point)
                    if value is None:
                        print(f"{date_str}: No data found.")
                        valid_data = False
                        break
                    data_rows.append((
                        supplier_name,
                        mesurement_device,
                        f"{date_str} 00:00",
                        f"{date_str} 23:59",
                        round(value / 1000, 2),
                        "kWh",
                        activity_name
                    ))
                    print(f"{date_str}: {value} Wh")
                if valid_data: 
                  csv_content = create_csv_in_memory(data_rows)
                  send_email_with_csv(csv_content, email_to, plant_name)
                  print(f"✅ Email sent to {email_to}")
                else:
                    send_error_email_to_admin(
                    subject=f"Error for Client {client['email_to']}",
                    body=f"An error occurred while processing data for client {client['email_to']}:\n\n{error_trace}"
                  )


            except Exception as client_error:
                error_trace = traceback.format_exc()
                print(f"❌ Error with client {client['plant_name']}: {client_error}")
                send_error_email_to_admin(
                    subject=f"Error for Client {client['email_to']}",
                    body=f"An error occurred while processing data for client {client['email_to']}:\n\n{error_trace}"
                )

        return {
            'statusCode': 200,
            'body': json.dumps('✅ Data processed for all clients (errors reported to admin).')
        }

    except Exception as e:
        trace = traceback.format_exc()
        print("❌ Fatal error in lambda_handler")
        send_error_email_to_admin("Fatal Error in Lambda", trace)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e), 'trace': trace})
        }
