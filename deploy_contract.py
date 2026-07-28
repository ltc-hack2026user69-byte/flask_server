from google.cloud.universalledger.v1 import (
    transactions_pb2,
    types_pb2,
)

from lloyds_ltc_reboot_2026 import helpers


def deploy_kyc_contract(
    creator_account_id: str,
    contract_path: str = "gculpy/smart.bin",
):
    """
    Deploy a new KYC smart contract and return its contract_id.
    """

    _, creator_private_pem, _ = helpers.load_user_account_by_id(
        creator_account_id
    )

    with open(contract_path, "rb") as f:
        contract_bytes = f.read()

    stub, endpoint = helpers.get_stub_and_endpoint()

    seq_num = helpers.get_sequence_number(
        stub,
        endpoint,
        creator_account_id,
    )

    create_contract_tx = transactions_pb2.CreateContract(
        contract_bytes=contract_bytes,
        contract_comment="KYC Contract",
    )

    client_tx = types_pb2.ClientTransaction(
        sender_id=creator_account_id,
        sequence_number=seq_num,
        create_contract_transaction=create_contract_tx,
    )

    tx_digest, cert = helpers.sign_and_submit_with_local_key(
        stub,
        endpoint,
        creator_account_id,
        creator_private_pem,
        client_tx,
    )

    contract_id = None

    for event in cert.events:
        if event.type in ("contract_created", "transaction_output"):
            for attr in event.attributes:
                if attr.key in ("contract_id", "value"):
                    contract_id = attr.value
                    break
        if contract_id:
            break

    if contract_id is None:
        raise RuntimeError("Contract deployment failed.")

    return {
        "success": True,
        "contract_id": contract_id,
        "transaction_digest": tx_digest,
    }