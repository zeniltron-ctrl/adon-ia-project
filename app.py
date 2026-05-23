import os, json, urllib.request
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
OLLAMA = os.environ.get('OLLAMA_HOST', 'http://127.0.0.1:11434')
MODEL = 'adon-ia'

def _req(method, path, data=None):
    url = f'{OLLAMA}{path}'
    body = json.dumps(data).encode() if data else None
    r = urllib.request.Request(url, data=body, method=method)
    r.add_header('Content-Type', 'application/json')
    resp = urllib.request.urlopen(r, timeout=180 if path == '/api/chat' else 5)
    return json.loads(resp.read().decode())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    msg = request.get_json().get('message', '')
    try:
        data = _req('POST', '/api/chat', {
            'model': MODEL,
            'messages': [
                {'role': 'system', 'content': 'Seu nome é Adon-ia. Você é um assistente de IA baseado no Qwen3. Responda sempre em português de forma útil e educada.'},
                {'role': 'user', 'content': msg}
            ],
            'stream': False
        })
        td = data.get('total_duration', 0) / 1e9
        ec = data.get('eval_count', 0)
        ed = data.get('eval_duration', 0) / 1e9
        tps = round(ec / ed, 1) if ed > 0 else 0
        return jsonify(
            response=data['message']['content'],
            time=f'{td:.1f}s',
            tokens=ec,
            tps=tps
        )
    except Exception as e:
        return jsonify(error=str(e)), 502

@app.route('/api/status')
def status():
    try:
        data = _req('GET', '/api/tags')
        models = [m['name'] for m in data.get('models', [])]
        return jsonify(ok=True, active=any(MODEL in m for m in models))
    except:
        return jsonify(ok=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12800, debug=False)
