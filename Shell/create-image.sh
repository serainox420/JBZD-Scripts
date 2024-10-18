#!/bin/bash

# Prosty skrypt dodający mema obrazkowego.
# Użycie: <plik config> <tytuł> <ścieżka do pliku>
# Gdzie plik config to ciastka i tokeny danego użytkownika, każdy użytkownik ma własny config. (config musi zawierać wartości COOKIE, X-XSRF-TOKEN oraz X-CSRF-TOKEN)
# Tytuł to tytuł wrzuty (tagi są takie jak tytuł)
# Ścieżka do pliku to miejsce i nazwa obrazka do wrzucenia
# Np `bash create-image.sh config/username.txt dupa obrazki/dupa.png`

# Check if the user has provided a config file and a file to upload
if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <config_file> <title> <path_to_file>"
  exit 1
fi

CONFIG_FILE=$1
TITLE=$2
FILE_PATH=$3

# Load the config file
if [ -f "$CONFIG_FILE" ]; then
  source "$CONFIG_FILE"
else
  echo "Config file not found!"
  exit 1
fi

# Ensure all tokens are set
if [ -z "$COOKIE" ] || [ -z "$X-CSRF-TOKEN" ] || [ -z "$X-XSRF-TOKEN" ]; then
  echo "Missing token(s) in the config file!"
  exit 1
fi

# Execute the curl request with the variables from the config file
curl 'https://jbzd.com.pl/content/create/image' \
  -H 'accept: application/json' \
  -H 'accept-language: en-US,en;q=0.9,pl-PL;q=0.8,pl;q=0.7' \
  -H 'cache-control: no-cache' \
  -H 'content-type: multipart/form-data' \
  -H "cookie: $COOKIE" \
  -H 'dnt: 1' \
  -H 'origin: https://jbzd.com.pl' \
  -H 'pragma: no-cache' \
  -H 'priority: u=1, i' \
  -H 'referer: https://jbzd.com.pl/oczekujace' \
  -H 'sec-ch-ua: "Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36' \
  -H "x-csrf-token: $X_CSRF_TOKEN" \
  -H "x-xsrf-token: $X_XSRF_TOKEN" \
  -F "title=$TITLE" \
  -F 'description=' \
  -F 'state=humor-memy' \
  -F 'mca=false' \
  -F 'mero=false' \
  -F 'mature=false' \
  -F 'search=' \
  -F "tags[0]=$TITLE" \
  -F 'age_group=0' \
  -F 'agreements[0]=1' \
  -F "file[7gTAAEwX2KzloMhj]=@$FILE_PATH"
