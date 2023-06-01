mkdir -p ~/.streamlit
echo "
[server]
headless = true
port = $PORT
enableCORS = true

[theme]
base = 'light'
primaryColor = '#f72585'
backgroundColor = '#f8f8f8'
secondaryBackgroundColor = '#ffffff'
textColor = '#3a0ca3'
font = 'sans serif'
" > ~/.streamlit/config.toml

mkdir -p ~/firebase
echo '
{
  "type": "service_account",
  "project_id": "jaka-id",
  "private_key_id": "3ffa94ea6f43c1be7b2aaf222c655c94b2ae89a9",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDODM01yaRGaojb\nAccFnbuCiHMndvLGSxYFcdl6hunDAx7jux/Rn93kmSEVIIcgK5eoDhyjxjcaRNWi\nSany72gYquRZ5SRf3o5jW8b6/TDvkT6SC/3nC274uTKPudcq1OF4KmoEs5c9wifV\n4OziXEJxITS5wk6/1mby/9amYkjBhc9ZIydt73PllHzywI9AoBbZLF7dvamlgiUJ\nAs5NK1cSOBnN8cJsPTpXJRAbKH67B9tDK6WuL3nuPR85TrmGeoO2LkRiJhUoLuxh\nnZWrNOetVeeGk9d4v0Oet6QGE2zMHZxtLaE451MjcKNxG9nvcC2gLHGxRdzQtlEZ\n7Raac9B/AgMBAAECggEACF6Qv0yPdaTCJlMuKFY91ZGBS+sS9Wb7YAE92jI8sIUh\n7hIdusAJnU1zAI6vrmjW4iagly5n8pM1MkBXvNxomAfo+pXKInLBydtie7NpF3II\n3pnKGGZofYXYPepIiR7Yga8HW2WIESQfxho6xP8GW94DbEAuPrCQwfIOX/fCCMo5\n3HVw4C7cA7PisleplA76L6gar4bcPK3N6nrE88fzD6Ib0J2EvOlPiN73eyL81YUO\n5k24yQQdO8G0OqSWPMPu7MM7gH3oLmIC7N8LdQwuApyeaRSK0DoB/wZOEfr8dwxC\nDbnx021b6F6d5f9m2W0BIqWGps3gZtGTqLZwwM0oAQKBgQD/aPVhzmdKcreIDADV\nUKUWs0aMF6prVuhc+Wyq30TuPtiuo2n1mcUHLxnyXVpYv0xQ5fGPfA7fba1t3oaR\nuVDPhqBvwAccnLXf1X4bYnFfOd9a+2wzYDvn+7TnKpVsN5FTbkwcjJLyw4qYR0q1\neLTz5cHYJNNveJuMqQHhtUsCfwKBgQDOhqczSotpopJ75lRo/ZU7ImhjD8ijtnVf\nZwiiIE06gz+LN3srBpaLzl3JfPFZSdTjejXAJoAruo6KRuSJYNxqEboK5hKYu7sW\nRYnO50i4dYSvADI60E7UIeyDg34m2hqzW/jVg9Mws4O73JCg03OfUMKQq1zE+5e9\nfTgAE1QyAQKBgQD5/DAYT953VrreFOmH4AwFoOjO26b4srJxtcuvnyInkimhHN7r\n/VqEQozB1K9GJ865a6a4SrN/6iiSXfgWj2xSArHrTudnENdOwvZQNVVD4DAGLAnm\nay2XTJzumZZwuh6qq00hsFFv/QYdL8ImxoNOKTZGqRytgT22OgFWeox1XwKBgDNX\nPhF+IpIsHAY5CBrhj0uYDiMyNUqdfSguUPMc3JYDMrTFIhVcGei/cIk6SjVMKWQz\naVFPQOWeBvlRDlcogSLNLVawQ0c8xBGRT+Tjkixo6ocmoVYFmtMZa9Z1xdKavbCA\n2KcbklC1D7aP6lRQvJmKVhPoxbMiaGJu0pESPQgBAoGAUTJ224idLgafg0kKuYff\nKxe7XISDRvR90Ab5TEn3E582Rl+u6Osx3W/PPV1FhmYt6srfOQhX2DpScFr/pPUP\nU8V4YWzBK+adbfHW0Mhv3vvO2NgcSbibwUE3e9saV73++rSPSXN4W4IhfFw/7555\nwl/DuLZv63Esa6gytDXgkh0=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-e83r3@jaka-id.iam.gserviceaccount.com",
  "client_id": "105991201552807563925",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-e83r3%40jaka-id.iam.gserviceaccount.com"
}
' > ~/firebase/serviceAccountKey.json
