import os

from google.cloud.universalledger.v1 import (
    transactions_pb2,
    types_pb2,
)

from lloyds_ltc_reboot_2026 import helpers


def deploy_kyc_contract(
    creator_account_id: str,
    contract_path: str | None = None,
):
    """
    Deploy a new KYC smart contract and return its contract_id.
    """

    _, creator_private_pem, _ = helpers.load_user_account_by_id(
        creator_account_id
    )

    # Common locations for the compiled contract
    possible_paths = [
        contract_path,
        "gculpy/smart.bin",
        "gculpy/our-sc.bin",
        "smart.bin",
        "our-sc.bin",
    ]

    contract_file = None

    for path in possible_paths:
        if path and os.path.exists(path):
            contract_file = path
            break

    if contract_file is None:
        raise FileNotFoundError(
            f"""
Compiled smart contract (.bin) not found.

Looked in:
{possible_paths}

Current working directory:
{os.getcwd()}

Files in current directory:
{os.listdir('.')}

If your contract has not been compiled, compile it first using gculpyc.
"""
        )

    with open(contract_file, "rb") as f:
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
        raise RuntimeError("Contract deployment failed. No contract_id returned.")

    return {
        "success": True,
        "contract_id": contract_id,
        "transaction_digest": tx_digest,
    }