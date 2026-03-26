import os, uuid
from datetime import datetime, timezone
from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient(os.getenv("MONGO_URI", "mongodb://db:27017/"))
db = client.deployer_db
deployments_col = db.deployments

@app.route('/deployments', methods=['GET', 'POST'])
def deployments():
    match request.method:
        case "GET":
            deploy = deployments_col.find({}, {"_id": 0}).sort("createdAt", -1)
            list_deploy = list(deploy)
            return jsonify(list_deploy), 200
        
        case "POST":
                data = request.json

                if not all(k in data for k in ("applicationId", "versionId", "environmentId")):
                    return jsonify({"message": "Champs obligatoires manquants"}), 400

                new_deployment = {
                    "id": str(uuid.uuid4()),
                    "applicationId": data['applicationId'],
                    "versionId": data['versionId'],
                    "environmentId": data['environmentId'],
                    "status": "PENDING",
                    "initiatedBy": data.get('initiatedBy', str(uuid.uuid4())), # Return a random user until the user's feature is available
                    "notes": data.get('notes', ""),
                    "startedAt": None,
                    "finishedAt": None,
                    "createdAt": datetime.now(timezone.utc).isoformat(),
                    "updatedAt": datetime.now(timezone.utc).isoformat()
                }

                deployments_col.insert_one(new_deployment.copy())

                if "_id" in new_deployment: del new_deployment["_id"] # NOus ne voulons pas d'id en plus donc il faut retirer l'id mis automatiquement par mongodb
                return jsonify(new_deployment), 201

@app.route('/deployments/<deploymentId>', methods=['GET'])
def get_deployment(deploymentId):
    match request.method:
        case "GET":
            dep = deployments_col.find_one({"id": deploymentId}, {"_id": 0})
            if not dep:
                return jsonify({"message": "Déploiement non trouvé"}), 404
            return jsonify(dep), 200
        
        case "PATCH":
            data = request.json
            update_fields = {"updatedAt": datetime.now(timezone.utc).isoformat()}

            if 'status' in data:
                status = data['status']
                update_fields['status'] = status
                if status == "RUNNING":
                    update_fields['startedAt'] = datetime.now(timezone.utc).isoformat()
                elif status in ["DEPLOYED", "FAILED"]:
                    update_fields['finishedAt'] = datetime.now(timezone.utc).isoformat()

            if 'notes' in data:
                update_fields['notes'] = data['notes']

            result = deployments_col.update_one({"id": deploymentId}, {"$set": update_fields})

            if result.matched_count == 0:
                return jsonify({"message": "Déploiement non trouvé"}), 404

            updated_doc = deployments_col.find_one({"id": deploymentId}, {"_id": 0})
            return jsonify(updated_doc), 200
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)