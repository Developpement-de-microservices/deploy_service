import os, uuid
from datetime import datetime, timezone
from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient(os.getenv("MONGO_URI", "mongodb://db:27017/"))
db = client.deployer_db
deployments_col = db.deployments

@app.route('/deployments', methods=['GET'])
def list_deployments():
    deploy = deployments_col.find({}, {"_id": 0}).sort("createdAt", -1)
    list_deploy = list(deploy)
    return jsonify(list_deploy), 200

@app.route('/deployments', methods=['POST'])
def create_deployment():
    data = request.json
    
    if not all(k in data for k in ("applicationId", "versionId", "environmentId")):
        return jsonify({"message": "Champs obligatoires manquants"}), 400

    new_deployment = {
        "id": str(uuid.uuid4()),
        "applicationId": data['applicationId'],
        "versionId": data['versionId'],
        "environmentId": data['environmentId'],
        "status": "PENDING",
        "initiatedBy": data.get('initiatedBy', str(uuid.uuid4())),
        "notes": data.get('notes', ""),
        "startedAt": None,
        "finishedAt": None,
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "updatedAt": datetime.now(timezone.utc).isoformat()
    }
    
    deployments_col.insert_one(new_deployment.copy())
    
    if "_id" in new_deployment: del new_deployment["_id"] # NOus ne voulons pas d'id en plus donc il faut retirer l'id mis automatiquement par mongodb
    return jsonify(new_deployment), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)