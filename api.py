from flask import Flask, request
import hashlib
import os

app = Flask(__name__)
TOKEN = os.environ.get('WECHAT_TOKEN', 'openclaw123')
ENCODING_AES_KEY = os.environ.get('WECHAT_ENCODING_AES_KEY', 'kRo3sWXMFDIHibzp6JHDNRm1cB7cC8Tdkdb59K8q7jx')
def verify_signature(token, timestamp, nonce, echostr):
    data = sorted([token, timestamp, nonce, echostr])
    return hashlib.sha1(''.join(data).encode()).hexdigest()

@app.route('/api/v1/channels/wecom', methods=['GET', 'POST'])
def callback():
    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    
    if request.method == 'GET':
        echostr = request.args.get('echostr', '')
        computed = verify_signature(TOKEN, timestamp, nonce, echostr)
        return echostr if computed == signature else 'Invalid', 403
    
    return 'success'

@app.route('/')
def home():
    return 'WeChat Callback Server OK'
