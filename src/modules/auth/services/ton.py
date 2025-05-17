from time import time
from typing import Literal

from fastapi import status
from httpx import AsyncClient, HTTPStatusError
from loguru import logger
from pytoniq_core import Address
from tonutils.tonconnect.models import Account, TonProof, WalletInfo

from src.config import settings
from src.modules.auth.constants import PROOF_LENGTH, PROOF_PREFIX_LENGTH
from src.modules.auth.dto import ProofVerificationDTO
from src.modules.auth.exceptions.application import ProofVerificationException
from src.modules.auth.exceptions.details import ProofVerificationExceptionDetail


async def check_proof(proof: ProofVerificationDTO) -> Literal[True]:
    wallet_info = await _get_wallet_info_from_proof(proof)
    return _verify_proof_payload(proof_hex=proof.proof.payload, wallet_info=wallet_info)


async def _get_wallet_info_from_proof(proof: ProofVerificationDTO) -> WalletInfo:
    address = Address(proof.address)
    account = Account.from_dict(
        {
            "address": f"{address.wc}:{address.hash_part.hex()}",
            "network": str(proof.network),
            "walletStateInit": proof.proof.state_init,
            "publicKey": await _get_public_key(proof.proof.state_init),
        }
    )
    ton_proof = TonProof.from_dict(proof.model_dump(by_alias=True))
    return WalletInfo(account=account, ton_proof=ton_proof)


async def _get_public_key(state_init: str) -> str | None:
    url = settings.tonapi_url.removesuffix("/") + "/v2/tonconnect/stateinit"
    payload = {"state_init": state_init}
    async with AsyncClient() as client:
        response = await client.post(url, json=payload)
    try:
        response.raise_for_status()
    except HTTPStatusError as exc:
        if exc.response.status_code is status.HTTP_400_BAD_REQUEST:
            logger.debug(response.json()["error"])
            message = ProofVerificationExceptionDetail.invalid_proof_format_exception
            raise ProofVerificationException(message=message) from exc
        return None

    data = response.json()
    if not isinstance(data, dict):
        return None
    return data.get("public_key")


def _verify_proof_payload(proof_hex: str, wallet_info: WalletInfo) -> Literal[True]:
    """
    Verifies that a proof payload (provided as hex) is valid and unexpired.

    :param proof_hex: The proof payload as a hex-encoded string.
    :param wallet_info: A WalletInfo instance providing the verify_proof() method.
    :return: True if the proof is valid and not expired, raises a ProofVerificationException otherwise.
    """
    if len(proof_hex) < PROOF_LENGTH:
        message = ProofVerificationExceptionDetail.invalid_length_exception.format(length=PROOF_LENGTH)
        logger.debug(message)
        raise ProofVerificationException(message)

    # Check the cryptographic proof via the wallet.
    if not wallet_info.verify_proof(proof_hex):
        logger.debug(ProofVerificationExceptionDetail.verification_failed_exception)
        raise ProofVerificationException(ProofVerificationExceptionDetail.verification_failed_exception)

    # Extract the expiration time from the latter 8 bytes of the hex string.
    try:
        expire_time = int(proof_hex[PROOF_PREFIX_LENGTH:PROOF_LENGTH], 16)
    except ValueError as exc:
        logger.debug(ProofVerificationExceptionDetail.invalid_proof_format_exception)
        raise ProofVerificationException(ProofVerificationExceptionDetail.invalid_proof_format_exception) from exc

    # Check whether the current time has exceeded the expiration time.
    if time() > expire_time:
        logger.debug(ProofVerificationExceptionDetail.proof_expired_exception)
        raise ProofVerificationException(ProofVerificationExceptionDetail.proof_expired_exception)

    return True
