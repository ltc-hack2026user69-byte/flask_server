import sys

from google.cloud.universalledger.v1 import (
    accounts_pb2,
    transactions_pb2,
    types_pb2,
)

from lloyds_ltc_reboot_2026 import helpers
from deploy_contract import deploy_kyc_contract


def create_ledger_account(
    account_manager_id: str,
    account_manager_kms_key: str,
):
    """
    Creates a Universal Ledger account,
    deploys a KYC smart contract for that account,
    and returns both account_id and contract_id.
    """

    print("[*] Determining next user account index...")
    index = helpers.get_next_user_index()

    print(f"[*] Generating EC keypair for user_{index:03d}...")
    private_pem, public_pem = helpers.generate_local_ec_keypair()

    print("[*] Connecting to Universal Ledger...")
    stub, endpoint = helpers.get_stub_and_endpoint()

    print("[*] Fetching Account Manager sequence number...")
    seq_num = helpers.get_sequence_number(
        stub,
        endpoint,
        account_manager_id,
    )

    print("[*] Building CreateAccount transaction...")

    create_account_tx = transactions_pb2.CreateAccount(
        public_key=public_pem,
        key_format=transactions_pb2.KEY_FORMAT_PEM_EC_P256_SHA256,
        roles=[
            accounts_pb2.ROLE_PAYER,
            accounts_pb2.ROLE_RECEIVER,
            accounts_pb2.ROLE_CONTRACT_CREATOR,
            accounts_pb2.ROLE_CONTRACT_PARTICIPANT,
        ],
        account_status=accounts_pb2.ACCOUNT_STATUS_ACTIVE,
        account_comment=f"User account {index:03d}",
    )

    client_tx = types_pb2.ClientTransaction(
        sender_id=account_manager_id,
        sequence_number=seq_num,
        create_account_transaction=create_account_tx,
    )

    print("[*] Signing CreateAccount transaction using Cloud KMS...")

    tx_digest, cert = helpers.sign_and_submit_with_kms(
        stub,
        endpoint,
        account_manager_id,
        account_manager_kms_key,
        client_tx,
    )

    new_account_id = None

    for event in cert.events:
        if event.type in ("account_created", "transaction_output"):
            for attr in event.attributes:
                if attr.key in ("account_id", "value"):
                    new_account_id = attr.value
                    break

        if new_account_id:
            break

    if not new_account_id:
        raise RuntimeError("Unable to obtain created account ID.")

    print(f"[+] Account Created: {new_account_id}")

    # Save keys locally
    priv_path, pub_path, meta_path = helpers.save_user_account(
        index,
        new_account_id,
        private_pem,
        public_pem,
    )

    print("[*] Deploying KYC Smart Contract...")

    try:
        contract = deploy_kyc_contract(
            creator_account_id=new_account_id
        )

        contract_id = contract["contract_id"]

        print(f"[+] Contract Created: {contract_id}")

    except Exception as e:
        print(f"[!] Contract deployment failed: {e}")
        raise

    return {
        "success": True,
        "account_id": new_account_id,
        "contract_id": contract_id,
        "transaction_digest": tx_digest,
        "private_key_path": priv_path,
        "public_key_path": pub_path,
        "metadata_path": meta_path,
    }