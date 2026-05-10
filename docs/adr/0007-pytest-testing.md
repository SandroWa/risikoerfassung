# 0007 – pytest als Test-Framework

**Status:** akzeptiert
**Datum:** 2026-05

## Kontext

Der `RisikoService` enthält die Geschäftslogik inkl. Optimistic Locking und
soll automatisiert getestet werden, bevor Änderungen ins Frontend/Backend
durchgereicht werden.

## Entscheidung

Tests werden mit **[pytest](https://docs.pytest.org/)** geschrieben und liegen
unter `tests/`. Die Test-Suite ist klassenbasiert (`TestCreate`, `TestUpdate`,
…) und nutzt eine Basisklasse `_BaseRisikoServiceTest` mit `setup_method` /
`teardown_method`, die den klassenweiten In-Memory-Store vor und nach jedem
Test leert.

## Alternativen

- **unittest** (stdlib) – verbosser, weniger ergonomisch.
- **nose2** – nicht mehr aktiv genug.
- **doctest** – ungeeignet für komplexere Szenarien.

## Begründung

- pytest ist der De-facto-Standard im Python-Ökosystem.
- Sehr gute Fehlermeldungen (Assertion-Introspection).
- Einfaches Parametrisieren und Fixtures – auch wenn wir hier bewusst auf
  klassische `setup_method`-Hooks setzen, um die Test-Isolation explizit zu
  machen (siehe Kommentar in der Basisklasse).

## Konsequenzen

- ➕ Schnelle, lesbare Tests (24 Tests in < 0,2 s).
- ➕ Keine Abhängigkeit zu Litestar-Runtime im Test → reine Unit-Tests des
  Service-Layers.
- ➖ Pytest-spezifische Konventionen (Discovery, `conftest.py` etc.) müssen
  bekannt sein.

