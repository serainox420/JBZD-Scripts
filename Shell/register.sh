#!/bin/bash

# Example: ./register.sh config.txt "email@gmail.com" "username" "password123" "recaptcha_token"

# Check if the correct number of arguments are passed
if [ "$#" -ne 5 ]; then
    echo "Usage: $0 path-to-config email login password recaptcha"
    exit 1
fi

# Assign the command line arguments to variables
CONFIG_FILE=$1
EMAIL=$2
LOGIN=$3
PASSWORD=$4
RECAPTCHA=$5

# Check if the specified config file exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Config file not found at $CONFIG_FILE!"
    exit 1
fi

# Source the config file to get COOKIE, X_CSRF_TOKEN, and X_XSRF_TOKEN
source "$CONFIG_FILE"

# Check if the required variables are loaded from the config file
if [ -z "$COOKIE" ] || [ -z "$X_CSRF_TOKEN" ] || [ -z "$X_XSRF_TOKEN" ]; then
    echo "Missing values in the config file! Ensure COOKIE, X_CSRF_TOKEN, and X_XSRF_TOKEN are set."
    exit 1
fi

# Execute the curl command and capture the output
response=$(curl -s 'https://jbzd.com.pl/auth/register' \
  -X 'POST' \
  -H 'accept: application/json' \
  -H 'accept-language: en-US,en;q=0.9,pl-PL;q=0.8,pl;q=0.7' \
  -H 'cache-control: no-cache' \
  -H "cookie: ${COOKIE}" \
  -H 'dnt: 1' \
  -H 'origin: https://jbzd.com.pl' \
  -H 'pragma: no-cache' \
  -H 'priority: u=1, i' \
  -H 'referer: https://jbzd.com.pl/' \
  -H 'sec-ch-ua: "Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36' \
  -H "x-csrf-token: ${X_CSRF_TOKEN}" \
  -H "x-xsrf-token: ${X_XSRF_TOKEN}" \
  -H 'content-type: application/json;charset=UTF-8' \
  --data-raw '{
      "email": "'"${EMAIL}"'",
      "login": "'"${LOGIN}"'",
      "password": "'"${PASSWORD}"'",
      "password_confirmation": "'"${PASSWORD}"'",
      "recaptcha": "'"${RECAPTCHA}"'",
      "rules": 1
  }')

# Check if the response contains success status
if echo "$response" | grep -q '"status":"success"'; then
    echo "Registration successful!"
else
    # Print the entire response if not successful
    echo "Request failed: $response"
fi
