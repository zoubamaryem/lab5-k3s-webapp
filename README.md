# 🚀 Lab 5: Deploying a Web Application with Database on K3s

![Kubernetes](https.io/badge/Kubernetes-K3s-blue?logo=kubernetes
https://img.shields.io/badge/Docker-Containerization-blue?logo=docker
![tps://img.shields.io/badge/Status-Completed-success

---

## 📌 Overview
This project demonstrates deploying a **two-tier application** on a **K3s Kubernetes cluster**.  
The architecture includes:
- **Frontend:** A Flask web application that allows users to insert and view data.
- **Backend:** A PostgreSQL database for storing submitted data.

The goal is to:
✅ Containerize the web app  
✅ Deploy both tiers using Kubernetes manifests  
✅ Expose the frontend externally while keeping the database internal  

---

## 🏗 Architecture Diagram
docs/architecture.png

**Components:**
- **Web App (NodePort Service)** → Accessible from outside the cluster.
- **Database (ClusterIP Service)** → Internal-only for security.

---

## 📂 Project Structure
lab5-k3s-webapp/
├── app/                # Web application source code
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── k8s/                # Kubernetes manifests
│   ├── web-deployment.yaml
│   ├── web-service.yaml
│   ├── db-deployment.yaml
│   └── db-service.yaml
├── scripts/            # Automation scripts
│   └── deploy.sh
├── docs/               # Documentation and screenshots
│   ├── architecture.png
│   └── screenshots/
│       ├── pods-running.png
│       └── app-working.png
└── README.md
## ⚙️ Technologies Used
- **K3s** – Lightweight Kubernetes
- **Flask** – Python Web Framework
- **PostgreSQL** – Database
- **Docker** – Containerization
- **kubectl** – Kubernetes CLI

---

## 🚀 Deployment Steps

### ✅ 1. Install K3s
```bash
curl -sfL https://get.k3s.io | sh -
kubectl get nodes

Access the Application: http://192.168.56.10:30080/
