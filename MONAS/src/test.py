import requests

r = requests.get('https://www.giffgaff.com/free-sim-cards', headers={
"authority": "www.giffgaff.com",
"method": "GET",
"path": "/free-sim-cards",
"scheme": "https",
"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"accept-encoding": "gzip, deflate, br",
"accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
"cache-control": "max-age=0",
"referer": "https://www.giffgaff.com/",
"sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
"sec-ch-ua-mobile": "?0",
"sec-ch-ua-platform": '"macOS"',
"sec-fetch-dest": "document",
"sec-fetch-mode": "navigate",
"sec-fetch-site": "same-origin",
"sec-fetch-user": "?1",
"upgrade-insecure-requests": "1",
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 Edg/80.0.361.62"
})

simorder_security_token = r.text.split('name="simorder_security_token" value="')
simorder_security_token = simorder_security_token[1]
simorder_security_token.split(' "id="simorder_security_token" />')
simorder_security_token = simorder_security_token[0]
print(simorder_security_token)
                