from __future__ import annotations

import logging
from datetime import date

from app.models.risiko.risiko_models import RisikoCreateDto, Risikoart, Status
from app.service.risiko_service import RisikoService

logger = logging.getLogger(__name__)


SEED_RISIKEN: list[RisikoCreateDto] = [
    RisikoCreateDto(
        versichert_ab_datum=date(2026, 1, 15),
        status=Status.POLICIERT,
        risikoart=Risikoart.GEBAEUDE,
        ort_adresse="Hauptstraße 1, 12345 Musterstadt",
        policennummer="POL-2026-0001",
        zusammenfassung="Mehrfamilienhaus mit 8 Wohneinheiten, Baujahr 1998",
    ),
    RisikoCreateDto(
        versichert_ab_datum=date(2026, 2, 1),
        status=Status.IN_BEARBEITUNG,
        risikoart=Risikoart.FIRMA,
        ort_adresse="Industrieweg 10, 80331 München",
        policennummer="POL-2026-0002",
        zusammenfassung="Maschinenbauunternehmen, 120 Mitarbeitende",
    ),
    RisikoCreateDto(
        versichert_ab_datum=date(2026, 3, 12),
        status=Status.NEU,
        risikoart=Risikoart.PERSON,
        ort_adresse="Lindenallee 22, 10115 Berlin",
        policennummer="POL-2026-0003",
        zusammenfassung="Einzelperson, Lebensversicherung",
    ),
    RisikoCreateDto(
        versichert_ab_datum=date(2026, 4, 1),
        status=Status.NEU,
        risikoart=Risikoart.GEBAEUDE,
        ort_adresse="Bergstraße 47, 70173 Stuttgart",
        policennummer="POL-2026-0004",
        zusammenfassung="Bürogebäude, 5 Stockwerke, Tiefgarage",
    ),
    RisikoCreateDto(
        versichert_ab_datum=date(2026, 4, 20),
        status=Status.IN_BEARBEITUNG,
        risikoart=Risikoart.FIRMA,
        ort_adresse="Hafenstraße 3, 20457 Hamburg",
        policennummer="POL-2026-0005",
        zusammenfassung="Logistikunternehmen mit Lagerhalle",
    ),
    RisikoCreateDto(
        versichert_ab_datum=date(2026, 5, 5),
        status=Status.POLICIERT,
        risikoart=Risikoart.PERSON,
        ort_adresse="Rosenweg 8, 50667 Köln",
        policennummer="POL-2026-0006",
        zusammenfassung="Berufsunfähigkeitsversicherung, Angestellte",
    ),
]


def seed_risiken() -> None:
    service = RisikoService()
    if service.list():
        logger.info("Seed übersprungen – es sind bereits Risiken vorhanden.")
        return

    for dto in SEED_RISIKEN:
        service.create(dto)
    logger.info("Seed abgeschlossen: %d Risiken angelegt.", len(SEED_RISIKEN))

