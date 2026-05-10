# 1003 – Dataclasses als Domänenmodelle

**Status:** akzeptiert
**Datum:** 2026-05

## Kontext

Die Domänenmodelle (`Risiko`) und DTOs (`RisikoCreateDto`, `RisikoUpdateDto`)
benötigen Typannotationen, automatische `__init__`/`__repr__`-Methoden und
gute Interoperabilität mit Litestar zur Serialisierung.

## Entscheidung

Es werden **Python-`@dataclass`-Klassen** (stdlib) verwendet:

```python
@dataclass
class Risiko:
    versichert_ab_datum: date
    status: Status
    risikoart: Risikoart | None = None
    ...
    id: UUID = field(default_factory=uuid4)
    version: int = 1
```

## Alternativen

- **Pydantic** – mehr Funktionen (Validatoren, Coercion), aber zusätzliche
  Abhängigkeit und etwas Magic.
- **attrs** – sehr flexibel, aber externe Abhängigkeit für etwas, das die
  stdlib bereits gut löst.
- **Plain Classes mit `__init__`** – mehr Boilerplate.

## Begründung

- **Stdlib only** – keine zusätzliche Abhängigkeit.
- Litestar versteht Dataclasses nativ als Request- und Response-Modelle und
  generiert daraus automatisch OpenAPI-Schemas.
- `dataclasses.asdict()` erlaubt einfaches Mapping zwischen Domain und DTO
  (siehe `RisikoService.create` und `update`).
- Type-Hints und Default-Werte sind klar lesbar.

## Konsequenzen

- ➕ Wenig Boilerplate, klar lesbar, keine externe Lib.
- ➕ Defaults via `field(default_factory=...)` erlauben sauberes Setzen von
  `id` und `version` ohne Setter-Logik.
- ➖ Keine eingebaute Laufzeit-Validierung; Validierung erfolgt durch
  Litestar (Typprüfung) und ggf. durch Service-Logik.

