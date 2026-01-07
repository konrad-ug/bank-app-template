from flask import Flask, request, jsonify
from src.account_registry import AccountRegistry
from src.personal_account import PersonalAccount

app = Flask(__name__)
registry = AccountRegistry()

@app.route("/api/accounts", methods=['POST'])
def create_account():
   data = request.get_json()
   print("Create account request received")
   print(f"Create account request: {data}")
   if registry.get_account_by_pesel(data["pesel"]):
       return jsonify({"message": "Account with this PESEL already exists"}), 409
   account = PersonalAccount(data["name"], data["surname"], data["pesel"])
   registry.add_account(account)
   return jsonify({"message": "Account created"}), 201

@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    print("Get all accounts request received")
    accounts = registry.get_all_accounts()
    accounts_data = [{"name": acc.first_name, "surname": acc.last_name, "pesel": acc.pesel, "balance": acc.balance} for acc in accounts]
    return jsonify(accounts_data), 200

@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    print("Get account count request received")
    count = registry.get_account_count()
    return jsonify({"count": count}), 200

@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    account = registry.get_account_by_pesel(pesel)
    if account:
        account_data = {"namaa": account.first_name, "surname": account.last_name, "pesel": account.pesel, "balance": account.balance}
        return jsonify(account_data), 200
    else:
        return jsonify({"message": "Account not found"}), 404

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    data = request.get_json()
    if not data or (not data.get("name") and not data.get("surname")):
        return jsonify({"message": "Request body must contain 'name' and/or 'surname'"}), 400
    account = registry.get_account_by_pesel(pesel)
    if not account:
        return jsonify({"message": "Account not found"}), 404
    if "name" in data:
        account.first_name = data["name"]
    if "surname" in data:
        account.last_name = data["surname"]
    return jsonify({"message": "Account updated"}), 200

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    account = registry.get_account_by_pesel(pesel)
    if not account:
        return jsonify({"message": "Account not found"}), 404
    registry.delete_account(pesel)
    return jsonify({"message": "Account deleted"}), 200

@app.route("/api/accounts/<pesel>/transfer", methods=['POST'])
def execute_transfer(pesel):
    data = request.get_json()
    if not data or "amount" not in data or "type" not in data:
        return jsonify({"message": "Request body must contain 'amount' and 'type'"}), 400
    account = registry.get_account_by_pesel(pesel)
    if not account:
        return jsonify({"message": "Account not found"}), 404
    amount = data["amount"]
    transfer_type = data["type"]
    transfers_types_mapping = {
        "incoming": account.incoming_transfer,
        "outgoing": account.outgoing_transfer,
        "express": account.express_outgoing_transfer
    }
    if transfer_type in transfers_types_mapping:
        transfer_method = transfers_types_mapping[transfer_type]
        success = transfer_method(amount)
        if success:
            return jsonify({"message": "Transfer successful"}), 200
        else:
            return jsonify({"message": "There was an issue with transfer"}), 422

# @app.route("/api/accounts/<pesel>/transfer", methods=['POST'])
# def execute_transfer(pesel):
#     data = request.get_json()
#     if not data or "amount" not in data or "type" not in data:
#         return jsonify({"message": "Request body must contain 'amount' and 'type'"}), 400
#     account = registry.get_account_by_pesel(pesel)
#     if not account:
#         return jsonify({"message": "Account not found"}), 404
#     amount = data["amount"]
#     transfer_type = data["type"]
#     if transfer_type == "incoming":
#         account.incoming_transfer(amount)
#         return jsonify({"message": "Transfer successful"}), 200
#     elif transfer_type == "outgoing":
#         if account.outgoing_transfer(amount):
#             return jsonify({"message": "Transfer successful"}), 200
#     elif transfer_type == "express":
#         if account.express_outgoing_transfer(amount):
#             return jsonify({"message": "Transfer successful"}), 200
#     else:
#         return jsonify({"message": "Unknown transfer type"}), 400
