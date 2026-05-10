from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Annotated
from uuid import UUID, uuid4

from msgspec import Meta


class Risikoart(str, Enum):
    GEBAEUDE = "Gebäude"
    FIRMA = "Firma"
    PERSON = "Person"


class Status(str, Enum):
    NEU = "neu"
    IN_BEARBEITUNG = "in Bearbeitung"
    POLICIERT = "policiert"


# Erlaubtes Format einer Policennummer, z. B. "POL-1234-5678".
POLICENNUMMER_PATTERN = r"^POL-\d{4}-\d{4}$"
Policennummer = Annotated[
    str,
    Meta(pattern=POLICENNUMMER_PATTERN, description="Format: POL-1234-5678"),
]


@dataclass
class Risiko:
    """
    Domänen-/Antwortmodell.

    Pflichtfelder: versichert_ab_datum, status.
    Server-verwaltet: id (auto-generiert), version (auto-verwaltet), erstellt_am.
    Alle übrigen Felder sind optional.
    """

    # Pflichtfelder
    versichert_ab_datum: date
    status: Status

    # Optionale Felder
    risikoart: Risikoart | None = None
    ort_adresse: str | None = None
    policennummer: Policennummer | None = None
    zusammenfassung: str | None = None

    # Server-verwaltet
    id: UUID = field(default_factory=uuid4)
    version: int = 1


@dataclass
class RisikoCreateDto:
    """
    Eingabemodell für POST /risiken.

    `id` und `version` werden vom Server gesetzt und dürfen nicht
    über die API mitgegeben werden.
    """

    # Pflichtfelder
    versichert_ab_datum: date
    status: Status

    # Optionale Felder
    risikoart: Risikoart | None = None
    ort_adresse: str | None = None
    policennummer: Policennummer | None = None
    zusammenfassung: str | None = None


@dataclass
class RisikoUpdateDto:
    """
    Eingabemodell für PATCH /risiken/{id}.

    `version` ist die erwartete Version (Optimistic Locking) und
    nicht der neue Wert. `id` darf nicht überschrieben werden.
    """

    risikoart: Risikoart | None = None
    versichert_ab_datum: date | None = None
    ort_adresse: str | None = None
    policennummer: Policennummer | None = None
    zusammenfassung: str | None = None
    status: Status | None = None
    version: int | None = None
