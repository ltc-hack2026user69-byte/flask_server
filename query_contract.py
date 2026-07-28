from google.cloud.universalledger.v1 import universalledger_pb2

from lloyds_ltc_reboot_2026 import helpers


def query_contract(contract_id: str):

    stub, endpoint = helpers.get_stub_and_endpoint()

    request = universalledger_pb2.QueryAccountRequest(
        endpoint=endpoint,
        account_id=contract_id,
    )

    response = stub.QueryAccount(request)

    if not response.HasField("account"):
        return {
            "success": False,
            "message": "Contract not found"
        }

    account = response.account

    result = {
        "success": True,
        "contract_id": contract_id,
        "comment": account.comment,
    }

    if account.HasField("contract_details"):

        fields = {}

        for key, value in account.contract_details.contract_fields.fields.items():

            if value.HasField("string_value"):
                fields[key] = value.string_value

            elif value.HasField("bool_value"):
                fields[key] = value.bool_value

            elif value.HasField("int64_value"):
                fields[key] = value.int64_value

        result["contract_state"] = fields

    return result