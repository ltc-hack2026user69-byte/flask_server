import gcul


class KYCContract(gcul.Contract):
    """KYC Verification Smart Contract."""

    customer_did: str
    product_type: str

    identity_document_type: str
    address_document_type: str
    dob_document_type: str

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

        identity_document_type: str,
        address_document_type: str,
        dob_document_type: str,

        identity_hash: str,
        address_hash: str,
        dob_hash: str,

        verified_by: str,
        verified_timestamp: str,
    ) -> None:
        """Stores verified KYC metadata."""

        self.customer_did = customer_did
        self.product_type = product_type

        self.identity_document_type = identity_document_type
        self.address_document_type = address_document_type
        self.dob_document_type = dob_document_type

        self.identity_hash = identity_hash
        self.address_hash = address_hash
        self.dob_hash = dob_hash

        self.verified = True
        self.verified_by = verified_by
        self.verified_timestamp = verified_timestamp

    def update_documents(
        self,
        identity_document_type: str,
        address_document_type: str,
        dob_document_type: str,

        identity_hash: str,
        address_hash: str,
        dob_hash: str,

        verified_by: str,
        verified_timestamp: str,
    ) -> None:
        """Updates KYC documents."""

        self.identity_document_type = identity_document_type
        self.address_document_type = address_document_type
        self.dob_document_type = dob_document_type

        self.identity_hash = identity_hash
        self.address_hash = address_hash
        self.dob_hash = dob_hash

        self.verified = True
        self.verified_by = verified_by
        self.verified_timestamp = verified_timestamp

    def revoke_kyc(
        self,
        verified_by: str,
        verified_timestamp: str,
    ) -> None:
        """Revokes customer KYC."""

        self.verified = False
        self.verified_by = verified_by
        self.verified_timestamp = verified_timestamp