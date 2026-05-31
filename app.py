from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)
TELEGRAM_API = "https://api.telegram.org"

@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    url = f"{TELEGRAM_API}/{path}"
    headers = {k: v for k, v in request.headers if k.lower() != 'host'}
    resp = requests.request(
        method=request.method,
        url=url,
        headers=headers,
        data=request.get_data(),
        query_string=request.query_string,
        stream=True
    )
    return Response(resp.iter_content(chunk_size=1024), status=resp.status_code, headers=dict(resp.headers))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
