# 🚀 Deploy Service

[![Status](https://img.shields.io/badge/status-en--développement-orange)](https://github.com/Developpement-de-microservices/deploy_service/tree/main)
[![Docker](https://img.shields.io/badge/Docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3670A0?style=flat&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-%23000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)

> **Deploy Service** est un microservice conçu pour servir de passerelle (gateway) simplifiée entre les utilisateurs et l'orchestration de conteneurs Docker.

---

## 📝 Présentation
L'objectif est d'abstraire la complexité technique de l'API Docker en proposant une interface REST intuitive pour gérer des environnements isolés.



---

## 🛠️ API Endpoints (Roadmap)

Le service expose les routes suivantes pour la gestion complète du cycle de vie des environnements :

| Méthode | Point de terminaison | Action | État |
| :--- | :--- | :--- | :---: |
| `POST` | `/envs` | Créer un nouvel environnement | ⏳ |
| `GET` | `/envs` | Lister tous les environnements | ⏳ |
| `GET` | `/envs/{envId}` | Récupérer les détails d'un environnement | ⏳ |
| `PUT` | `/envs/{envId}` | Modifier la configuration d'un environnement | ⏳ |
| `DELETE` | `/envs/{envId}` | Supprimer un environnement | ⏳ |
