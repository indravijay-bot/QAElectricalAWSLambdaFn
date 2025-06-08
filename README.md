# Automated Monthly Solar Energy Report Sender

This project helps send monthly solar energy reports to clients automatically. It gets daily data from the iSolarCloud API, creates a CSV file with all the information, and sends it to the client’s email. It’s built using AWS Lambda and Python, and everything runs by itself at the start of each month.

---

## What It Does

- Collects daily solar production data from iSolarCloud for the last 30 days
- Creates a report in CSV format with all the data
- Sends the report to the client’s email address
- Sends a copy of the report to me as well
- If there is an error or missing data, it doesn’t send the report to the client
- Instead, it sends me an email with the error details

---

## Technologies Used

- Python (3.9 or later)
- AWS Lambda (serverless)
- iSolarCloud Open API
- SMTP (for sending emails)
- `requests`, `csv`, `email` libraries

---

## How To Set Up

### 1. Environment Variables (`.env` file)

Create a `.env` file and add the following details:

ISOLAR_BASE_URL 
AUTH_ENDPOINT 
DATA_ENDPOINT 

APPKEY 
X_ACCESS_KEY
USERNAME 
PASSWORD 

EMAIL_FROM 
EMAIL_PASSWORD(16 Digit appkey)
EMAIL_ADMIN 
QA_EMAIL 
CC_EMAIL_1 /2 /3 ...
EMAIL_TO_1 /2 /3 ...
PS_ID_1 /2 /3 ...
PS_KEY_LIST_1 /2 /3 ...

Project for 
QA ELectricals (Airport west, Melbourne)
renewables@qaelectrical.com.au

🧑‍💻 Author
Indravijaysinh Zala
zalaindravijaysinh50@gmail.com
