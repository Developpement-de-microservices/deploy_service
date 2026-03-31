# 🚀 Deploy Service

[![Status](https://img.shields.io/badge/status-en--développement-orange)](https://github.com/Developpement-de-microservices/deploy_service/tree/main)
[![Docker](https://img.shields.io/badge/Docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3670A0?style=flat&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-%23000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=flat&logo=mongodb&logoColor=white)](https://www.mongodb.com/)

> **Deploy Service** est un microservice conçu pour servir de passerelle (gateway) simplifiée entre les utilisateurs et l'orchestration de conteneurs Docker.

---

## 📝 Présentation
L'objectif est d'abstraire la complexité technique de l'API Docker en proposant une interface REST intuitive pour gérer des déploiements. Le service assure la persistance des états de déploiement et communique avec les services d'inventaire (`apps` et `environments`) via un proxy.

## 🛠️ API Endpoints

Le service expose les routes suivantes. Toutes les routes (hors health) nécessitent une authentification via un **Bearer Token**.

| Méthode | Point de terminaison | Description | État |
| :--- | :--- | :--- | :--- |
| `GET` | `/deployments/health` | Vérifier l'état du service | ✅ Implémenté |
| `GET` | `/deployments` | Lister les déploiements (triés par date) | ✅ Implémenté |
| `POST` | `/deployments` | Déclencher un nouveau déploiement | ✅ Implémenté |
| `GET` | `/deployments/{id}` | Consulter le détail d'un déploiement | ✅ Implémenté |
| `PATCH` | `/deployments/{id}` | Mettre à jour l'état ou les notes | ✅ Implémenté |
| `POST` | `/deployments/{id}/rollback` | Lancer un rollback | 📅 Prevu |
