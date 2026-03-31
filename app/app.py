import os, uuid
from datetime import datetime, timezone
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS 
import requests

app = Flask(__name__)
CORS(app)

client = MongoClient(os.getenv("MONGO_URI", "mongodb://db_deploy_service:27017/"))
db = client.deployer_db
deployments_col = db.deployments

def authentification():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post("http://proxy/auth/verify", headers=headers)
        if response.status_code != 200:
            return jsonify({"error": "Not authorized"}), 401
    except requests.RequestException:
        return jsonify({"error": "Unable to check token, check /auth API"}), 401

@app.route("/deployments/health", methods=["GET"])
def get_health_events():
    response = {
        "status": "ok",
        "service": "Deployments",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    return jsonify(response), 200

@app.route('/deployments', methods=['GET', 'POST'])
def deployments():
    match request.method:
        case "GET":
            auth_check = authentification()
            if auth_check: 
                return auth_check
            
            deploy = deployments_col.find({}, {"_id": 0}).sort("createdAt", -1)
            list_deploy = list(deploy)
            return jsonify(list_deploy), 200
        
        case "POST":
                auth_check = authentification()
                if auth_check: 
                    return auth_check
                
                data = request.json
                token = "tokene1f93ed8-9778-4721-b06a-311f6a7dc415" 
                headers = {
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json'
                }


                response_app = requests.get(f'http://proxy:8080/apps/{data["applicationId"]}', headers=headers)
                if response_app.status_code == 404:
                    return jsonify({"message": "The app doesn't exist!"}), 404
                
                response_env = requests.get(f'http://proxy:8080/environments/{data["environmentId"]}', headers=headers)
                if response_env.status_code == 404:
                    return jsonify({"message": "The environment doesn't exist!"}), 404

                if not all(k in data for k in ("applicationId", "versionId", "environmentId")):
                    return jsonify({"message": "Missing required field!"}), 400

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

@app.route('/deployments/<deploymentId>', methods=['GET', 'PATCH'])
def get_deployment(deploymentId):
    match request.method:
        case "GET":
            auth_check = authentification()
            if auth_check: 
                return auth_check

            dep = deployments_col.find_one({"id": deploymentId}, {"_id": 0})
            if not dep:
                return jsonify({"message": "Deploy not found!"}), 404
            return jsonify(dep), 200
        
        case "PATCH":
            auth_check = authentification()
            if auth_check: 
                return auth_check
                
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
                return jsonify({"message": "Deploy not found!"}), 404

            updated_doc = deployments_col.find_one({"id": deploymentId}, {"_id": 0})
            return jsonify(updated_doc), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
