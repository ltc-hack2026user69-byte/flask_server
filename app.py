from flask import Flask, request, jsonify
from flask_cors import CORS

from create_account import create_ledger_account
from get_account import get_account
from invoke_contract import invoke_kyc
from query_contract import query_contract

import os
app = Flask(__name__)
CORS(app)

ACCOUNT_MANAGER_ID = "1:ACT:GBP:425TpAuzy7KUnmbKTW6VHth8UUFRQ9aSq6YuUr5buqEe1"

ACCOUNT_MANAGER_KMS_KEY = "projects/ltc-hack2026-team14/locations/in/keyRings/ltc-reboot-2026/cryptoKeys/account-manager/cryptoKeyVersions/1"


@app.route("/")
def home():
    return "GCUL Server Running"


@app.route("/ledger/create-account", methods=["POST"])
def create_account():

    try:

        result = create_ledger_account(
            ACCOUNT_MANAGER_ID,
            ACCOUNT_MANAGER_KMS_KEY,
        )

        return jsonify({
            "success": True,
            "ledger": result
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    
@app.route("/ledger/account/<account_id>", methods=["GET"])
def retrieve_account(account_id):
    try:
        response = get_account(account_id)
        account = response.account

        public_key = account.public_key.decode("utf-8")

        return jsonify({
            "success": True,
            "account": {
                "account_id": account_id,
                "public_key": public_key,
                "status": account.user_details.account_status,
                "roles": list(account.user_details.roles),
                "comment": account.comment
            }
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    

@app.route("/ledger/verify-kyc", methods=["POST"])
def verify_kyc():

    data = request.get_json()

    result = invoke_kyc(
        participant_account_id=data["participant_account_id"],
        customer_did=data["customer_did"],
        product_type=data["product_type"],
        identity_hash=data["identity_hash"],
        address_hash=data["address_hash"],
        dob_hash=data["dob_hash"],
        verified_by=data["verified_by"],
        verified_timestamp=data["verified_timestamp"],
    )
    return jsonify(result)   

@app.route("/ledger/query-contract", methods=["POST"])
def query():

    data = request.get_json()

    result = query_contract(
        contract_id=data["contract_id"]
    )

    return jsonify(result) 
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        debug=False,
    )