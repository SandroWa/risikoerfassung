# 1006 – Domain-Exceptions statt HTTP-Exceptions im Service

**Status:** akzeptiert
**Datum:** 2026-05

## Kontext

Wenn der Service direkt HTTP-spezifische Exceptions (`NotFoundException`,
`HTTPException(409)`) wirft, wird er an Litestar gekoppelt und kann nicht
mehr unabhängig getestet oder z. B. von einem CLI/Worker wiederverwendet
werden.

## Entscheidung

Der `RisikoService` wirft ausschließlich **fachliche Exceptions** aus dem
Domain-Layer:

- `RisikoNotFoundError(risiko_id)` – wenn ein Risiko nicht existiert.
- `RisikoVersionConflictError(risiko_id, expected, actual)` – wenn die
  erwartete Version nicht zur aktuellen passt.

Erst der `RisikoController` übersetzt diese Exceptions in HTTP-Statuscodes:

- `RisikoNotFoundError` → `404 Not Found`
- `RisikoVersionConflictError` → `409 Conflict`

## Alternativen

- **Direkt HTTP-Exceptions im Service werfen** – kürzer, aber bindet die
  Geschäftslogik an das Web-Framework.
- **Result-Objekte/Either-Pattern** – funktionaler Stil, in Python aber
  unüblich und macht den Code verboser.

## Begründung

- **Framework-Unabhängigkeit:** Der Service kennt kein HTTP.
- **Testbarkeit:** Im Test wird auf `RisikoNotFoundError` direkt geprüft
  (`pytest.raises(...)`), ohne Litestar-Stack.
- **Wiederverwendbarkeit:** Falls später ein CLI-Tool oder Worker dieselbe
  Logik nutzen will, kann er die Exceptions selbst behandeln.

## Konsequenzen

- ➕ Sauber entkoppelte Schichten.
- ➕ Tests prüfen fachliche Fehlersemantik direkt.
- ➖ Der Controller braucht etwas mehr Mapping-Code (kleine try/except-Blöcke
  pro Handler).

