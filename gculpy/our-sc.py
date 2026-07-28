import gcul


class KYCContract(gcul.Contract):
    """KYC Verification Smart Contract."""

    customer_did: str
    product_type: str

    identity_hash: str
    address_hash: str
    dob_hash: str

    verified: bool

    verified_by: str
    verified_timestamp: str

    def register_kyc(
        self,
        customer_did: str,
        product_type: str,
        identity_hash: str,
        address_hash: str,
        dob_hash: str,
        verified_by: str,
        verified_timestamp: str,
    ) -> None:
        """Stores verified KYC metadata."""

        self.customer_did = customer_did
        self.product_type = product_type

        self.identity_hash = identity_hash
        self.address_hash = address_hash
        self.dob_hash = dob_hash

        self.verified = True

        self.verified_by = verified_by
        self.verified_timestamp = verified_timestamp

    def revoke_kyc(self) -> None:
        """Marks KYC as revoked."""

        self.verified = False

    def update_documents(
        self,
        identity_hash: str,
        address_hash: str,
        dob_hash: str,
        verified_by: str,
        verified_timestamp: str,
    ) -> None:
        """Updates document hashes after reverification."""

        self.identity_hash = identity_hash
        self.address_hash = address_hash
        self.dob_hash = dob_hash

        self.verified = True
        self.verified_by = verified_by
        self.verified_timestamp = verified_timestamp