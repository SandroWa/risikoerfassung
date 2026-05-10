# 1005 – In-Memory-Store statt Datenbank

**Status:** akzeptiert (vorläufig)
**Datum:** 2026-05

## Kontext

Das Projekt hat aktuell Demo-/Lerncharakter. Eine echte Datenbank
(Postgres, SQLite, …) würde Setup, Migrationen, Connection-Pooling und
weitere Tooling-Themen erfordern.

## Entscheidung

Die Risiken werden in einem **klassenweiten Python-Dictionary** (`dict`)
direkt im `RisikoService` gehalten:

```python
class RisikoService:
    _store: dict[UUID, Risiko] = {}
```

Beim Anwendungsstart werden über `seed.py` ein paar Beispiel-Risiken
angelegt.

## Alternativen

- **SQLite + SQLAlchemy** – wenig Setup, persistent. Realistisches Setup,
  aber zusätzliche Komplexität (Sessions, Migrations).
- **Postgres in Docker** – produktionsnah, aber für Demo Overkill.
- **TinyDB / Pickle-File** – persistiert, aber bringt eigene Fallstricke.

## Begründung

- Maximaler Fokus auf API-Design, Domänenlogik und Frontend ohne DB-Boilerplate.
- Tests laufen schnell und ohne externe Abhängigkeiten.
- Einfacher Einstieg für neue Entwickler im Projekt.

## Konsequenzen

- ➕ Kein DB-Setup, keine Migrationen, keine Treiber-Abhängigkeiten.
- ➕ Tests sind blitzschnell.
- ➖ **Keine Persistenz** – beim Neustart sind alle Daten weg (nur Seeds
  werden neu angelegt).
- ➖ **Nicht thread-/multi-process-sicher** – bei mehreren Workers wäre der
  Store pro Worker getrennt. Daher in `RisikoService._store` als
  Klassenattribut bewusst markiert und nur als Demo zu verstehen.
- ➖ Spätere Migration zu echter DB erfordert Anpassung des Service-Layers
  (geringer Aufwand, da der Layer entkoppelt ist – siehe ADR 1001).

