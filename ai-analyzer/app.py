import os
import requests
import time
from prometheus_api_client import PrometheusConnect
from prometheus_client import start_http_server, Gauge, Enum
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PROMETHEUS_URL = os.getenv('PROMETHEUS_URL', 'http://prometheus-operated.monitoring.svc:9090')
OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://ollama.monitoring.svc.cluster.local:11434')
METRICS_PORT = int(os.getenv('METRICS_PORT', '8000'))

analysis_score = Gauge('ai_analysis_score', 'Общий балл критичности (0-100)')
cpu_usage = Gauge('ai_reported_cpu_usage', 'Загрузка CPU по данным AI')
ram_usage = Gauge('ai_reported_ram_usage', 'Загрузка RAM по данным AI')
service_status = Enum('ai_service_state', 'Состояние сервиса', states=['ok', 'warning', 'critical'])

def get_metrics():
    try:
        prom = PrometheusConnect(url=PROMETHEUS_URL, disable_ssl=True)

        cpu_query = '100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)'
        ram_query = '(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100'

        logger.info(f"Выполняется запрос CPU: {cpu_query}")
        logger.info(f"Выполняется запрос RAM: {ram_query}")

        cpu_result = prom.custom_query(cpu_query)
        ram_result = prom.custom_query(ram_query)

        if not cpu_result or not ram_result:
            raise ValueError("Пустой результат запроса Prometheus")

        cpu = float(cpu_result[0]["value"][1])
        ram = float(ram_result[0]["value"][1])

        logger.info(f"Получены метрики CPU: {cpu:.2f}%, RAM: {ram:.2f}%")
        return cpu, ram
    except Exception as e:
        logger.error(f"Ошибка получения метрик: {str(e)}")
        raise

def analyze_with_ai(cpu, ram):
    prompt = f"""
Системные метрики:
- CPU: {cpu:.2f}%
- RAM: {ram:.2f}%
Проанализируй и верни JSON:
{{
    "score": "0-100",
    "problems": ["список проблем"],
    "solutions": ["список решений"]
}}
"""
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",  # Исправлено: убран /api, используется /generate для Ollama 0.7.1+
            json={
                "model": "gemma:2b-instruct",
                "prompt": prompt,
                "stream": False,
                "format": "json"
            },
            timeout=60
        )
        response.raise_for_status()
        data = response.json()

        # В новых версиях Ollama ответ в data["response"] или data["text"] — может быть строкой JSON
        text_response = data.get("response") or data.get("text") or json.dumps(data)

        try:
            parsed = json.loads(text_response)
            return parsed
        except json.JSONDecodeError:
            # Если не JSON, возвращаем как есть в словаре
            return {"raw_response": text_response}

    except Exception as e:
        logger.error(f"Ошибка AI: {str(e)}")
        raise

def calculate_status(score):
    if score > 80:
        return 'critical'
    elif score > 60:
        return 'warning'
    return 'ok'

if __name__ == "__main__":
    start_http_server(METRICS_PORT)
    logger.info(f"Метрик-сервер запущен на порту {METRICS_PORT}")

    while True:
        try:
            current_cpu, current_ram = get_metrics()
            ai_report = analyze_with_ai(current_cpu, current_ram)

            # Ожидаем, что ai_report — это dict с ключом "score"
            score = 0
            if isinstance(ai_report, dict):
                score_raw = ai_report.get("score", 0)
                try:
                    score = float(score_raw)
                except (ValueError, TypeError):
                    score = 0

            analysis_score.set(score)
            cpu_usage.set(current_cpu)
            ram_usage.set(current_ram)
            service_status.state(calculate_status(score))

            logger.info(f"Отчет AI:\n{json.dumps(ai_report, ensure_ascii=False, indent=2)}")

        except Exception as e:
            logger.error(f"Критическая ошибка: {str(e)}")
            service_status.state('critical')

        time.sleep( int(os.getenv('ANALYSIS_INTERVAL', '300')) )
