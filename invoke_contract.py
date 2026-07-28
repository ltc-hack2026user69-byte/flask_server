from google.cloud.universalledger.v1 import (
    transactions_pb2,
    types_pb2,
    common_pb2,
)

from lloyds_ltc_reboot_2026 import helpers


def invoke_kyc(
    participant_account_id: str,
    customer_did: str,
    product_type: str,
    identity_hash: str,
    address_hash: str,
    dob_hash: str,
    verified_by: str,
    verified_timestamp: str,
):
    """
    Invokes the register_kyc() method of the deployed KYC Smart Contract.
    """

    # Load participant private key
    _, participant_private_pem, _ = helpers.load_user_account_by_id(
        participant_account_id
    )

    # Connect to Universal Ledger
    stub, endpoint = helpers.get_stub_and_endpoint()

    # Get sequence number
    seq_num = helpers.get_sequence_number(
        stub,
        endpoint,
        participant_account_id,
    )

    # Build invoke transaction
    contract_id="1:CTR:00443aKgJA2TaQMtJZf4jzhLpULPEb4DEuNfAQEL8WFd8"
    invoke_tx = transactions_pb2.InvokeContractMethod(
        contract_id=contract_id,
        method_name="register_kyc",
        arguments={
            "customer_did": common_pb2.Value(
                string_value=customer_did
            ),
            "product_type": common_pb2.Value(
                string_value=product_type
            ),
            "identity_hash": common_pb2.Value(
                string_value=identity_hash
            ),
            "address_hash": common_pb2.Value(
                string_value=address_hash
            ),
            "dob_hash": common_pb2.Value(
                string_value=dob_hash
            ),
            "verified_by": common_pb2.Value(
                string_value=verified_by
            ),
            "verified_timestamp": common_pb2.Value(
                string_value=verified_timestamp
            ),
        },
    )

    client_tx = types_pb2.ClientTransaction(
        sender_id=participant_account_id,
        sequence_number=seq_num,
        invoke_contract_method_transaction=invoke_tx,
    )

    # Sign & submit
    tx_digest, cert = helpers.sign_and_submit_with_local_key(
        stub,
        endpoint,
        participant_account_id,
        participant_private_pem,
        client_tx,
    )

    return {
        "success": True,
        "transaction_digest": tx_digest,
    }
