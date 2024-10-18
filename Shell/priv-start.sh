#!/bin/bash

# Rozpocznij nowa rozmowe prywatną
# Podajesz: <Config> oraz <UID> + <NICK>, a otrzymujesz <HASH>
# $0 <config> <UID> <NICK>
# Wypluwa Hash: <XYZ> który jest potrzebny do faktycznego wysłania wiadomości.
# Hash rozmowy można wygenerować w ten sposób, lub ręcznie na stronie, wchodząc z kimś w rozmowe, hash znajdziesz na końcu URL

# Check if the correct number of arguments are passed
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 path-to-config UID NICK"
    exit 1
fi

# Assign command line arguments to variables
CONFIG_FILE=$1
USER_ID=$2
NICKNAME=$3

# Check if the specified config file exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Config file not found at $CONFIG_FILE!"
    exit 1
fi

# Source the config file to get COOKIE, X_CSRF_TOKEN, X_XSRF_TOKEN
source "$CONFIG_FILE"

# Check if the required variables are loaded from the config file
if [ -z "$COOKIE" ] || [ -z "$X_CSRF_TOKEN" ] || [ -z "$X_XSRF_TOKEN" ]; then
    echo "Missing values in the config file! Ensure COOKIE, X_CSRF_TOKEN, and X_XSRF_TOKEN are set."
    exit 1
fi

# Execute the curl command and capture the output
response=$(curl -s "https://jbzd.com.pl/private-message/thread/start/${USER_ID}" \
  -X 'POST' \
  -H 'accept: application/json' \
  -H 'accept-language: en-US,en;q=0.9,pl-PL;q=0.8,pl;q=0.7' \
  -H 'cache-control: no-cache' \
  -H 'content-length: 0' \
  -H "cookie: ${COOKIE}" \
  -H 'dnt: 1' \
  -H 'origin: https://jbzd.com.pl' \
  -H 'pragma: no-cache' \
  -H 'priority: u=1, i' \
  -H "referer: https://jbzd.com.pl/uzytkownik/${NICKNAME}" \
  -H 'sec-ch-ua: "Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36' \
  -H "x-csrf-token: ${X_CSRF_TOKEN}" \
  -H "x-xsrf-token: ${X_XSRF_TOKEN}")

# Check if the response contains success status
if echo "$response" | grep -q '"status":"success"'; then
    # Extract the hash value from the response using grep/sed
    hash=$(echo "$response" | grep -o '"hash":"[^"]*' | sed 's/"hash":"//')
    echo "Hash: $hash"
else
    # Print the entire response if not successful
    echo "Request failed: $response"
fi
