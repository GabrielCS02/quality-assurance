from flask import Flask, request, Response
from prometheus_client import Counter, Histogram, generate_latest
import time
import random

app = Flask(__name__)

# Definindo as métricas que o Prometheus vai ler
REQUEST_COUNT = Counter('http_requests_total', 'Total de requisições HTTP', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'Latência das requisições HTTP', ['method', 'endpoint'])

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype="text/plain")

@app.route('/')
def home():
    start_time = time.time()
    time.sleep(random.uniform(0.05, 0.15)) # Simula um tempo de resposta normal rápido
    
    REQUEST_COUNT.labels('GET', '/', 200).inc()
    REQUEST_LATENCY.labels('GET', '/').observe(time.time() - start_time)
    return "Bem-vindo à E-Fecaf Global!"

@app.route('/checkout')
def checkout():
    start_time = time.time()
    chance = random.random()
    status_code = 200
    
    # Simula um gargalo de performance (15% de chance de falhar ou ficar muito lento)
    if chance < 0.15:
        time.sleep(random.uniform(2.0, 4.0)) # Lentidão severa que queremos detetar
        status_code = 500
        response_text = "Erro 500: Falha no servidor de pagamentos."
    else:
        time.sleep(random.uniform(0.2, 0.5)) # Tempo normal de checkout
        response_text = "Compra realizada com sucesso!"
        
    REQUEST_COUNT.labels('GET', '/checkout', status_code).inc()
    REQUEST_LATENCY.labels('GET', '/checkout').observe(time.time() - start_time)
    
    return response_text, status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)