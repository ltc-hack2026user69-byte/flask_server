import gcul


class KYCContract(gcul.Contract):
    """KYC Verification Smart Contract."""

    # Customer Information
    customer_did: str
    ledger_account_id: str
    product_type: str

    # Document Hashes
    identity_hash: str
    address_hash: str
    dob_hash: str

    # Verification Details
    verified: bool
    verified_by: str
    verified_timestamp: str

    def register_kyc(
        self,
        customer_did: str,
        ledger_account_id: str,
        product_type: str,
        identity_hash: str,
        address_hash: str,
        dob_hash: str,
        verified_by: str,
        verified_timestamp: str,
    ) -> None:
        """Registers a customer's verified KYC."""

        self.customer_did = customer_did
        self.ledger_account_id = ledger_account_id
        self.product_type = product_type

        self.identity_hash = identity_hash
        self.address_hash = address_hash
        self.dob_hash = dob_hash

        self.verified = True
        self.verified_by = verified_by
        self.verified_timestamp = verified_timestamp

    def update_kyc(
        self,
        identity_hash: str,
        address_hash: str,
        dob_hash: str,
        verified_by: str,
        verified_timestamp: str,
    ) -> None:
        """Updates verified document hashes."""

        self.identity_hash = identity_hash
        self.address_hash = address_hash
        self.dob_hash = dob_hash

        self.verified = True
        self.verified_by = verified_by
        self.verified_timestamp = verified_timestamp

    def revoke_kyc(
        self,
        revoked_by: str,
        revoked_timestamp: str,
    ) -> None:
        """Revokes KYC."""

        self.verified = False
        self.verified_by = revoked_by
        self.verified_timestamp = revoked_timestamp

    def get_customer_did(self) -> str:
        return self.customer_did

    def get_ledger_account_id(self) -> str:
        return self.ledger_account_id

    def get_product_type(self) -> str:
        return self.product_type

    def get_identity_hash(self) -> str:
        return self.identity_hash

    def get_address_hash(self) -> str:
        return self.address_hash

    def get_dob_hash(self) -> str:
        return self.dob_hash

    def is_verified(self) -> bool:
        return self.verified

    def get_verified_by(self) -> str:
        return self.verified_by

    def get_verified_timestamp(self) -> str:
        return self.verified_timestamp