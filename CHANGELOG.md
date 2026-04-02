# 📓 Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

---

## [1.0] - 2026-03-31 (Initial Release)

### ✨ Ajouts (Added)
- **Gestion des déploiements** : 
    - Création d'un déploiement via `POST /deployments` avec génération d'UUID.
    - Récupération de la liste complète via `GET /deployments` (triée par date).
    - Consultation d'un déploiement spécifique par ID.
- **Cycle de vie** : Mise à jour dynamique des statuts (`PENDING`, `RUNNING`, `DEPLOYED`, `FAILED`) via `PATCH`.
- **Horodatage automatique** : Gestion des champs `createdAt`, `updatedAt`, `startedAt` et `finishedAt` selon l'état du déploiement.
- **Sécurité** : 
    - Middleware d'authentification (`Bearer Token`) vérifié auprès du proxy.
    - Validation de l'existence de l'application et de l'environnement avant création.
- **Base de données** : Intégration avec **MongoDB** pour la persistance des données.
- **Santé du service** : Endpoint `/deployments/health` pour le monitoring.

### ⚙️ Technique
- Initialisation du projet avec **Flask 3.0.2**.
- Support de **CORS**

---

## [1.1] - 2026-04-02

### Modification
- **Modification de l'authentification vers les autres service**
    - Utilisation du token de l'utilisateur au lieux d'un token fixe.

---

## [Prochainement]

### 🚀 À venir
- Implémentation de la fonction `rollback`.

---
*Dernière mise à jour : 31 mars 2026*
