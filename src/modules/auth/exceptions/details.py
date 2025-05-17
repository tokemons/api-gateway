from dataclasses import dataclass


@dataclass
class ProofVerificationExceptionDetail:
    invalid_length_exception: str = "The proof must be at least {length} hex chars to contain random bytes+expiry."
    verification_failed_exception: str = "Check the cryptographic proof via the wallet failed."
    invalid_proof_format_exception: str = "Invalid proof format: unable to parse timestamp."
    proof_expired_exception: str = "Proof has expired."
