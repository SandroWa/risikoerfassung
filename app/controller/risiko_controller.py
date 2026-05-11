from __future__ import annotations

from uuid import UUID

from litestar import Controller, delete, get, patch, post
from litestar.di import Provide
from litestar.exceptions import HTTPException, NotFoundException
from litestar.status_codes import HTTP_204_NO_CONTENT, HTTP_409_CONFLICT

from app.models.risiko.risiko_models import Risiko, RisikoCreateDto, RisikoUpdateDto, Risikoart, Status
from app.service.risiko_service import (
    RisikoNotFoundError,
    RisikoService,
    RisikoVersionConflictError,
)


async def provide_risiko_service() -> RisikoService:
    return RisikoService()


class RisikoController(Controller):
    path = "/risiken"
    tags = ["Risiken"]
    dependencies = {"service": Provide(provide_risiko_service)}

    @get("/")
    async def list_risiken(
        self,
        service: RisikoService,
        risikoart: Risikoart | None = None,
        status: Status | None = None,
    ) -> list[Risiko]:
        return service.list(risikoart=risikoart, status=status)

    @get("/{risiko_id:uuid}")
    async def get_risiko(self, service: RisikoService, risiko_id: UUID) -> Risiko:
        try:
            return service.get(risiko_id)
        except RisikoNotFoundError as e:
            raise NotFoundException(detail=str(e)) from e

    @post("/")
    async def create_risiko(self, service: RisikoService, data: RisikoCreateDto) -> Risiko:
        return service.create(data)

    @patch("/{risiko_id:uuid}")
    async def update_risiko(
        self, service: RisikoService, risiko_id: UUID, data: RisikoUpdateDto
    ) -> Risiko:
        try:
            return service.update(risiko_id, data)
        except RisikoNotFoundError as e:
            raise NotFoundException(detail=str(e)) from e
        except RisikoVersionConflictError as e:
            raise HTTPException(status_code=HTTP_409_CONFLICT, detail=str(e)) from e

    @delete("/{risiko_id:uuid}", status_code=HTTP_204_NO_CONTENT)
    async def delete_risiko(
        self,
        service: RisikoService,
        risiko_id: UUID,
        version: int | None = None,
    ) -> None:
        try:
            service.delete(risiko_id, version)
        except RisikoNotFoundError as e:
            raise NotFoundException(detail=str(e)) from e
        except RisikoVersionConflictError as e:
            raise HTTPException(status_code=HTTP_409_CONFLICT, detail=str(e)) from e
