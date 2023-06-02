pip install -r requirements.txt

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
  "private_key_id": "ad36e9ca9b56ac470eb552884cc4bab8c8a06596",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDBFHit9j9H2zy3\nr5D1hh4+osI/Y8eLWMrzKMhnbauC6TqluZGR1xnXuxhrvHAmKRezY9eWQbsPLnjD\nNe1NVVOJkMhUsmoA4buSgI88d6vbfv62wu8advObgAL1LayUR27e/sU94rEEySUx\nRFQQzfnWInaHWqvUTXSyWDC1dRrdm60owhHjfu8G35KlhGsTFsS+usMO05sW3jXH\n/ZYW/Sc6UHzdqbBtL6zJaMqbhhLc9+/m8xIwY/otieIo/nByn3oeQg5o98JfABPL\nhEOBKHAcx8XQzETd6U/JLWt3XkiF4I4C5gQjXztSZd3QzvfiB614+H0kZeFB77Up\ndAl3BH5ZAgMBAAECggEAMt1iwWl62EJAZ5+fz56qfxO/mpV9rw8QQCjBSsYQhedN\nZPVTDRmenD+UumUlIlh2/vJRjCr6zZAPjlW5k0LkQ/xZWj66QEs3b+vgUCyyoJt/\nHMST2uP1X0TFArQqn9GFusdhTOFYgws+ehEnGFo69BeWJChV1hMlqAolotgb4L85\n01yeD3RsFymmFo5hbic2J4/eTBl6fGHU4jqtttm7PcP4AX8wmQ4do95xGf+tANwv\n+dwDETeQI0KU1QgP0INqUuNd9FUdn5hKGQBXra/cvsGwoAAJitIEfOZwNa367efM\ntOq8dpgz1Ud39+BU4c3a5+428Ba/IRMfT+3Q3SO7ZQKBgQDvdUCSULGbJr+UI8V6\nCP+ILDa4zYJGBPSJU8cw9raH8ssoN3OOPT23SNa9DYLCzkeFh05Oo180teV24yK6\n/y2PxmYW6PCISAQX2sIX4UKpE0kCPWyCKCRFs3dLgnA+3ntEjMYzVxltckp/6u1e\ncYhjbOL6pBUYjPwvbIc935ksOwKBgQDOawlQTTz8orKfFm5S2YkQbwSZIpzmfLY/\nTnPuRjpnHput63vHHKxkWq8/xQMa6DGRLU3FWz9hQ7R9qjp5jav33I6J+PJsoHfI\n+TBcFL8dhI761Acc1bcNZIHAdvdAYnNwNdrB5/IzCZ607m6wOkLuFs16lCjhJUCe\n4o5FmCbaewKBgBP0DEZk7PfFuc8JUApEN67MKF8r2MAm542N6po85KbdZ2pZfIqM\ntdjQ+/vS5WOANtt8k9zfpi5JPe6zLJCydMR3PsiH7oscnSKzutqsjZZzIfFK1wDd\ngXBBbR5gpyPF/DWRGW7rwhWpoWWZWOA2y6ulRiCmjY93KAh3naldOXFDAoGBAIKC\nMlVPQGwLAhyLth0z5PE7ABFCTSl9WE0WcT4JsQtZ0txXst7lRin9HCiZi6kLfato\nlW9ejegVQpzhcC9CX6RLEuQxPjVoD9RFmUne5CbplO0J+aVFioMxNMhXb2SJ2qrr\nofBPklaqkmmbBujtLTwTtr71xhLz1rOeUo218XrZAoGBAIqJv/v0Hg0MMF86UdL5\ntGihqR8atDA0pxg5Q0MWw7e8bqxyF8U7JUl0cJcMFINehkDCv5yu4ZONfkKHnAbQ\nNdVMY/TNr92M89iumUOZwRUojH2k/E+oZaDLxKaRp+GzKiE6sSOvQs5oGqRCh5p6\nO7XBdFWEwq2cO1FigN0uPaHk\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-e83r3@jaka-id.iam.gserviceaccount.com",
  "client_id": "105991201552807563925",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-e83r3%40jaka-id.iam.gserviceaccount.com"
}
' > ~/firebase/serviceAccountKey.json

DOCKER_BUILDKIT=1 docker build ./scraping/ -t scraping
