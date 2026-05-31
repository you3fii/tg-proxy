from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)
TELEGRAM_API = "https://api.telegram.org"

@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    url = f"{TELEGRAM_API}/{path}"
    
    # کپی کردن هدرها به جز هدر Host
    req_headers = {k: v for k, v in request.headers if k.lower() != 'host'}
    
    # ارسال درخواست به تلگرام با اصلاح پارامتر params
    resp = requests.request(
        method=request.method,
        url=url,
        headers=req_headers,
        data=request.get_data(),
        params=request.args,  # ⚡ اصلاح شد
        stream=False
    )
    
    # فیلتر کردن هدرهای پاسخ برای جلوگیری از تداخل کدگذاری
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    res_headers = {k: v for k, v in resp.headers.items() if k.lower() not in excluded_headers}
    
    return Response(resp.content, status=resp.status_code, headers=res_headers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
