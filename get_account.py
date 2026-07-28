from google.cloud.universalledger.v1 import universalledger_pb2
from lloyds_ltc_reboot_2026 import helpers


def get_account(account_id: str):
    stub, endpoint = helpers.get_stub_and_endpoint()

    request = universalledger_pb2.QueryAccountRequest(
        endpoint=endpoint,
        account_id=account_id,
    )

    response = stub.QueryAccount(request)

    print(response)
    return response

