# Server Monitoring + AI Log Analyzer with Ollama 🤖📊

> **Project:** Automated server monitoring + AI-powered log and metrics analysis using [Ollama](https://ollama.com/) 

This project combines traditional infrastructure monitoring (via Prometheus) with AI-based insights powered by local LLMs (Large Language Models), providing not just raw metrics, but also **intelligent analysis**, **problem detection**, and **actionable recommendations**.

Perfect for DevOps engineers, SRE teams, and anyone looking to bring AIOps capabilities into their infrastructure stack.

---

## 🧠 How It Works

1. The system collects CPU and RAM usage from Prometheus.
2. These metrics are sent to a local LLM via the Ollama API.
3. The model returns:
   - A criticality score (0–100)
   - List of potential issues
   - Recommended actions
4. Results are exposed as Prometheus metrics and logs for alerting and visualization.

---

## ✅ Key Features

- 🔍 Real-time CPU & RAM metric collection via Prometheus  
- 💡 AI-driven system health analysis using Ollama models (`gemma`, `llama3`, `phi`, etc.)  
- 📊 Exported Prometheus metrics for integration with Grafana or Alertmanager  
- 📦 Containerized with Docker & ready for Kubernetes  
- 🚀 Lightweight and easy to extend  

---

## 🧩 Architecture Overvie

|  Servers / Node  | ----> |   Prometheus   | ----> |   AI Analyzer (Ollama API)  | ----> |   Grafana Dashboard     |




---

## 🛠️ Technologies Used

- **AI Analysis**: Python + FastAPI + Ollama
- **Monitoring**: Prometheus
- **Visualization**: Grafana
- **Orchestration**: Kubernetes
- **Containerization**: Docker

---

## 🚀 Quick Start (Kubernetes)

### 1. Deploy on Kubernetes

```bash
kubectl apply -f k8s/
```
Includes: 

    ai-analyzer.yaml – main AI analysis service
    ollama-deployment.yaml – Ollama backend
    stress-deployment.yaml – optional stress test pod
    alert-rules.yaml – Prometheus alert rules
     

2. Import Grafana Dashboard 

Open Grafana at:   
http://grafana-url/dashboard/import

Import the dashboard file:  
dashboards/ai-server-monitoring.json


🧪 Example AI Output
{
  "score": 75,
  "problems": ["High CPU load", "RAM near critical usage"],
  "solutions": [
    "Consider scaling infrastructure",
    "Check background processes",
    "Increase container resources"
  ]
}

📈 Exported Metrics 

    ai_analysis_score – Overall criticality score (0–100)
    ai_reported_cpu_usage – CPU usage (%)
    ai_reported_ram_usage – RAM usage (%)
    ai_service_state – Service state enum: ok/warning/critical
     

🧰 Extensibility 

You can: 

    Add your own LLMs via Ollama
    Extend Prometheus queries
    Integrate with Slack/Telegram for alerts
    Customize prompts for domain-specific scenarios
     

🔐 Security 

    All connections run securely within the Kubernetes cluster
    Supports environment variables for secure configuration
    Can be extended with RBAC and TLS for production use
     

📎 License 

MIT License – free to use and modify. 
📬 Contact 

If you have questions, suggestions, or want to contribute, feel free to open an issue or reach out directly: 

📧 dmitrij.plastun@gmail.com 
 
🚧 Roadmap 

    Telegram/Slack notification bot  
    OpenTelemetry support  
    Predictive failure detection module  
    Web UI for prompt/model management  
    Loki-based log analysis extension
 

If you like this project, please give it a ⭐️ on GitHub. It helps attract contributors and users. 

💡 Tip:  Try different Ollama models (llama3, mistral, phi, dolphin-mixtral) for better results. You can fine-tune prompts in ai-analyzer/app.py. 
