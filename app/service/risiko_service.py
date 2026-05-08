from __future__ import annotations

import logging
from dataclasses import asdict
from uuid import UUID

from app.models.risiko.risiko_models import (
    Risiko,
    RisikoCreateDto,
    RisikoUpdateDto,
    Risikoart,
    Status,
)

logger = logging.getLogger(__name__)


class RisikoNotFoundError(Exception):

    def __init__(self, risiko_id: UUID) -> None:
        super().__init__(f"Risiko {risiko_id} nicht gefunden")
        self.risiko_id = risiko_id


class RisikoVersionConflictError(Exception):
    """Optimistic-Locking-Konflikt: erwartete Version stimmt nicht mit der aktuellen überein."""

    def __init__(self, risiko_id: UUID, expected: int | None, actual: int) -> None:
        super().__init__(
            f"Versionskonflikt für Risiko {risiko_id}: erwartet {expected}, aktuell {actual}"
        )
        self.risiko_id = risiko_id
        self.expected = expected
        self.actual = actual


class RisikoService:
    """
    Service-Schicht zwischen Controller und (in-memory) Datenhaltung.

    """

    # Klassenweiter In-Memory-Store (für Demo-Zwecke geteilt zwischen Instanzen)
    _store: dict[UUID, Risiko] = {}

    def list(
        self,
        risikoart: Risikoart | None = None,
        status: Status | None = None,
    ) -> list[Risiko]:
            risiken = list(self._store.values())
            if risikoart is not None:
                risiken = [r for r in risiken if r.risikoart == risikoart]
            if status is not None:
                risiken = [r for r in risiken if r.status == status]
            return risiken

    def get(self, risiko_id: UUID) -> Risiko:
            risiko = self._store.get(risiko_id)
            if risiko is None:
                raise RisikoNotFoundError(risiko_id)
            return risiko

    def create(self, data: RisikoCreateDto) -> Risiko:
            # id und version werden vom Modell/Server gesetzt (nicht aus dem Request)
            risiko = Risiko(**asdict(data))
            self._store[risiko.id] = risiko
            return risiko

    def update(self, risiko_id: UUID, data: RisikoUpdateDto) -> Risiko:
            risiko = self._store.get(risiko_id)
            if risiko is None:
                raise RisikoNotFoundError(risiko_id)

            # Optimistic Locking: Client muss die erwartete Version mitschicken
            if data.version is None:
                raise RisikoVersionConflictError(risiko_id, expected=None, actual=risiko.version)
            if data.version != risiko.version:
                raise RisikoVersionConflictError(
                    risiko_id, expected=data.version, actual=risiko.version
                )

            for key, value in asdict(data).items():
                if value is None:
                    continue
                if key == "version":
                    # version wird vom Server verwaltet, nicht vom Client überschrieben
                    continue
                setattr(risiko, key, value)

            risiko.version += 1
            return risiko

    def delete(self, risiko_id: UUID, expected_version: int | None = None) -> None:
            risiko = self._store.get(risiko_id)
            if risiko is None:
                raise RisikoNotFoundError(risiko_id)

            if expected_version is None:
                raise RisikoVersionConflictError(risiko_id, expected=None, actual=risiko.version)
            if expected_version != risiko.version:
                raise RisikoVersionConflictError(
                    risiko_id, expected=expected_version, actual=risiko.version
                )

            del self._store[risiko_id]
