from google.cloud.universalledger.v1 import (
    accounts_pb2,
    transactions_pb2,
    types_pb2,
)

from lloyds_ltc_reboot_2026 import helpers


def grant_contract_roles(
    account_manager_id: str,
    account_manager_kms_key: str,
    account_id: str,
):
    """
    Grants CONTRACT_CREATOR and CONTRACT_PARTICIPANT roles
    to a Universal Ledger user account.
    """

    # Connect to Universal Ledger
    stub, endpoint = helpers.get_stub_and_endpoint()

    # Get Account Manager sequence number
    seq_num = helpers.get_sequence_number(
        stub,
        endpoint,
        account_manager_id,
    )

    # Build AddRoles transaction
    add_roles_tx = transactions_pb2.AddRoles(
        account_id=account_id,
        roles=[
            accounts_pb2.ROLE_CONTRACT_CREATOR,
            accounts_pb2.ROLE_CONTRACT_PARTICIPANT,
        ],
    )

    client_tx = types_pb2.ClientTransaction(
        sender_id=account_manager_id,
        sequence_number=seq_num,
        add_roles_transaction=add_roles_tx,
    )

    # Sign with Cloud KMS
    tx_digest, cert = helpers.sign_and_submit_with_kms(
        stub,
        endpoint,
        account_manager_id,
        account_manager_kms_key,
        client_tx,
    )

    return {
        "success": True,
        "transaction_digest": tx_digest,
        "certificate": cert,
    }