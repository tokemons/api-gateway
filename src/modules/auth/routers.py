from dependency_injector.wiring import inject
from fastapi import APIRouter
from loguru import logger
from pytoniq import Address
from starlette import status
from tonutils.tonconnect.utils.proof import generate_proof_payload

from src.core.api.exceptions.dto import InternalServerErrorHTTPExceptionDTO
from src.core.api.exceptions.http.common import InternalServerErrorHTTPException
from src.modules.auth.constants import PROOF_TTL
from src.modules.auth.dto import JWTPayload, JWTResponse, PayloadDTO, ProofVerificationDTO
from src.modules.auth.exceptions.application import ProofVerificationException
from src.modules.auth.exceptions.dto import ProofHTTPExceptionDTO
from src.modules.auth.exceptions.http import BaseProofHTTPException
from src.modules.auth.services.jwt import JWT
from src.modules.auth.services.ton import check_proof

router = APIRouter(prefix="/auth")


@router.get("/ton", status_code=status.HTTP_200_OK)
@inject
def ton_proof_payload_generation() -> PayloadDTO:
    payload = generate_proof_payload(PROOF_TTL)
    return PayloadDTO(payload=payload)


@router.post(
    "/ton",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ProofHTTPExceptionDTO},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": InternalServerErrorHTTPExceptionDTO},
    },
)
@inject
async def ton_proof_verification(
    proof: ProofVerificationDTO,
) -> JWTResponse:
    try:
        await check_proof(proof)
    except ProofVerificationException as exc:
        raise BaseProofHTTPException(detail=exc.message) from exc
    except Exception as exc:
        logger.exception(exc)
        raise InternalServerErrorHTTPException from exc

    address = Address(proof.address)
    jwt_payload = JWTPayload(address=address.to_str())
    # user = await get_user_by_address(address.to_str())
    # if user is not None:
    #     return JWT.encode(data=jwt_payload)
    #
    # user = await create_user(address.to_str())
    return JWT.encode(data=jwt_payload)
