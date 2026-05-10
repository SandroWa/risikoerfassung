from __future__ import annotations

from datetime import date
from uuid import UUID, uuid4

import pytest

from app.models.risiko.risiko_models import (
    Risikoart,
    RisikoCreateDto,
    RisikoUpdateDto,
    Status,
)
from app.service.risiko_service import (
    RisikoNotFoundError,
    RisikoService,
    RisikoVersionConflictError,
)


class _BaseRisikoServiceTest:
    """
    Basisklasse für alle Risiko-Service-Tests.

    `setup_method` wird von pytest vor jedem Test in einer Klasse aufgerufen
    und sorgt dafür, dass der klassenweite In-Memory-Store leer ist und jeder
    Test eine frische `RisikoService`-Instanz erhält. Damit beeinflussen sich
    die Tests gegenseitig nicht.
    """

    service: RisikoService

    def setup_method(self) -> None:
        RisikoService._store.clear()
        self.service = RisikoService()

    def teardown_method(self) -> None:
        RisikoService._store.clear()


def make_create_dto(
    *,
    versichert_ab_datum: date | None = None,
    status: Status = Status.NEU,
    risikoart: Risikoart | None = Risikoart.GEBAEUDE,
    ort_adresse: str | None = "Musterstraße 1",
    policennummer: str | None = "P-1",
    zusammenfassung: str | None = "Zusammenfassung",
) -> RisikoCreateDto:
    return RisikoCreateDto(
        versichert_ab_datum=versichert_ab_datum or date(2026, 1, 1),
        status=status,
        risikoart=risikoart,
        ort_adresse=ort_adresse,
        policennummer=policennummer,
        zusammenfassung=zusammenfassung,
    )


# ---------------------------------------------------------------------------
# create
# ---------------------------------------------------------------------------

class TestCreate(_BaseRisikoServiceTest):
    def test_create_speichert_risiko_und_setzt_id_und_version(self) -> None:
        dto = make_create_dto()

        risiko = self.service.create(dto)

        assert isinstance(risiko.id, UUID)
        assert risiko.version == 1
        assert risiko.versichert_ab_datum == dto.versichert_ab_datum
        assert risiko.status == dto.status
        assert risiko.risikoart == dto.risikoart
        assert risiko.ort_adresse == dto.ort_adresse
        assert risiko.policennummer == dto.policennummer
        assert risiko.zusammenfassung == dto.zusammenfassung
        assert RisikoService._store[risiko.id] is risiko

    def test_create_mit_nur_pflichtfeldern(self) -> None:
        dto = RisikoCreateDto(versichert_ab_datum=date(2026, 5, 1), status=Status.NEU)

        risiko = self.service.create(dto)

        assert risiko.risikoart is None
        assert risiko.ort_adresse is None
        assert risiko.policennummer is None
        assert risiko.zusammenfassung is None

    def test_create_vergibt_unterschiedliche_ids(self) -> None:
        r1 = self.service.create(make_create_dto())
        r2 = self.service.create(make_create_dto())

        assert r1.id != r2.id


# ---------------------------------------------------------------------------
# get
# ---------------------------------------------------------------------------

class TestGet(_BaseRisikoServiceTest):
    def test_get_liefert_gespeichertes_risiko(self) -> None:
        created = self.service.create(make_create_dto())

        result = self.service.get(created.id)

        assert result is created

    def test_get_unbekannte_id_wirft_not_found(self) -> None:
        unknown = uuid4()
        with pytest.raises(RisikoNotFoundError) as exc_info:
            self.service.get(unknown)

        assert exc_info.value.risiko_id == unknown


# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------

class TestList(_BaseRisikoServiceTest):
    def test_list_leerer_store(self) -> None:
        assert self.service.list() == []

    def test_list_ohne_filter_liefert_alle(self) -> None:
        a = self.service.create(make_create_dto(risikoart=Risikoart.GEBAEUDE, status=Status.NEU))
        b = self.service.create(
            make_create_dto(risikoart=Risikoart.FIRMA, status=Status.IN_BEARBEITUNG)
        )

        result = self.service.list()

        assert {r.id for r in result} == {a.id, b.id}

    def test_list_filter_nach_risikoart(self) -> None:
        gebaeude = self.service.create(make_create_dto(risikoart=Risikoart.GEBAEUDE))
        self.service.create(make_create_dto(risikoart=Risikoart.FIRMA))
        self.service.create(make_create_dto(risikoart=Risikoart.PERSON))

        result = self.service.list(risikoart=Risikoart.GEBAEUDE)

        assert [r.id for r in result] == [gebaeude.id]

    def test_list_filter_nach_status(self) -> None:
        self.service.create(make_create_dto(status=Status.NEU))
        policiert = self.service.create(make_create_dto(status=Status.POLICIERT))

        result = self.service.list(status=Status.POLICIERT)

        assert [r.id for r in result] == [policiert.id]

    def test_list_filter_kombiniert(self) -> None:
        treffer = self.service.create(
            make_create_dto(risikoart=Risikoart.PERSON, status=Status.IN_BEARBEITUNG)
        )
        # andere Risikoart
        self.service.create(
            make_create_dto(risikoart=Risikoart.FIRMA, status=Status.IN_BEARBEITUNG)
        )
        # anderer Status
        self.service.create(make_create_dto(risikoart=Risikoart.PERSON, status=Status.NEU))

        result = self.service.list(risikoart=Risikoart.PERSON, status=Status.IN_BEARBEITUNG)

        assert [r.id for r in result] == [treffer.id]

    def test_list_filter_ohne_treffer(self) -> None:
        self.service.create(make_create_dto(risikoart=Risikoart.GEBAEUDE))

        assert self.service.list(risikoart=Risikoart.PERSON) == []


# ---------------------------------------------------------------------------
# update
# ---------------------------------------------------------------------------

class TestUpdate(_BaseRisikoServiceTest):
    def test_update_aendert_felder_und_erhoeht_version(self) -> None:
        created = self.service.create(make_create_dto(status=Status.NEU))

        updated = self.service.update(
            created.id,
            RisikoUpdateDto(status=Status.POLICIERT, version=created.version),
        )

        assert updated.status == Status.POLICIERT
        assert updated.version == 2
        assert updated.id == created.id

    def test_update_ignoriert_none_felder(self) -> None:
        created = self.service.create(make_create_dto(ort_adresse="Alt", policennummer="P-1"))

        updated = self.service.update(
            created.id,
            RisikoUpdateDto(ort_adresse="Neu", version=created.version),
        )

        assert updated.ort_adresse == "Neu"
        assert updated.policennummer == "P-1"  # unverändert

    def test_update_setzt_version_nicht_aus_dto(self) -> None:
        """`version` im DTO ist die erwartete Version, nicht der neue Wert."""
        created = self.service.create(make_create_dto())
        version_vor_update = created.version

        updated = self.service.update(
            created.id,
            RisikoUpdateDto(ort_adresse="X", version=version_vor_update),
        )

        assert updated.version == version_vor_update + 1

    def test_update_mehrfach_inkrementiert_version(self) -> None:
        created = self.service.create(make_create_dto())

        self.service.update(created.id, RisikoUpdateDto(ort_adresse="A", version=1))
        # `created` ist dieselbe Instanz, daher reflektiert created.version den aktuellen Stand
        assert created.version == 2

        self.service.update(created.id, RisikoUpdateDto(ort_adresse="B", version=2))
        assert created.version == 3
        assert created.ort_adresse == "B"

    def test_update_unbekannte_id_wirft_not_found(self) -> None:
        unknown = uuid4()
        with pytest.raises(RisikoNotFoundError):
            self.service.update(unknown, RisikoUpdateDto(version=1, ort_adresse="X"))

    def test_update_ohne_version_wirft_konflikt(self) -> None:
        created = self.service.create(make_create_dto())

        with pytest.raises(RisikoVersionConflictError) as exc_info:
            self.service.update(created.id, RisikoUpdateDto(ort_adresse="X"))

        assert exc_info.value.expected is None
        assert exc_info.value.actual == created.version

    def test_update_falsche_version_wirft_konflikt(self) -> None:
        created = self.service.create(make_create_dto())

        with pytest.raises(RisikoVersionConflictError) as exc_info:
            self.service.update(
                created.id,
                RisikoUpdateDto(ort_adresse="X", version=created.version + 5),
            )

        assert exc_info.value.expected == created.version + 5
        assert exc_info.value.actual == created.version

    def test_update_konflikt_aendert_keinen_zustand(self) -> None:
        created = self.service.create(make_create_dto(ort_adresse="Alt"))

        with pytest.raises(RisikoVersionConflictError):
            self.service.update(
                created.id,
                RisikoUpdateDto(ort_adresse="Neu", version=999),
            )

        unchanged = self.service.get(created.id)
        assert unchanged.ort_adresse == "Alt"
        assert unchanged.version == 1


# ---------------------------------------------------------------------------
# delete
# ---------------------------------------------------------------------------

class TestDelete(_BaseRisikoServiceTest):
    def test_delete_entfernt_risiko(self) -> None:
        created = self.service.create(make_create_dto())

        self.service.delete(created.id, expected_version=created.version)

        assert created.id not in RisikoService._store
        with pytest.raises(RisikoNotFoundError):
            self.service.get(created.id)

    def test_delete_unbekannte_id_wirft_not_found(self) -> None:
        with pytest.raises(RisikoNotFoundError):
            self.service.delete(uuid4(), expected_version=1)

    def test_delete_ohne_version_wirft_konflikt(self) -> None:
        created = self.service.create(make_create_dto())

        with pytest.raises(RisikoVersionConflictError) as exc_info:
            self.service.delete(created.id)

        assert exc_info.value.expected is None
        assert exc_info.value.actual == created.version
        assert created.id in RisikoService._store  # nicht gelöscht

    def test_delete_falsche_version_wirft_konflikt(self) -> None:
        created = self.service.create(make_create_dto())

        with pytest.raises(RisikoVersionConflictError) as exc_info:
            self.service.delete(created.id, expected_version=created.version + 1)

        assert exc_info.value.expected == created.version + 1
        assert exc_info.value.actual == created.version
        assert created.id in RisikoService._store


# ---------------------------------------------------------------------------
# Store-Verhalten
# ---------------------------------------------------------------------------

class TestSharedStore(_BaseRisikoServiceTest):
    def test_store_wird_zwischen_instanzen_geteilt(self) -> None:
        s1 = RisikoService()
        s2 = RisikoService()

        created = s1.create(make_create_dto())

        assert s2.get(created.id) is created

