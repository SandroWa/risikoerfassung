# 1002 – DTO-Pattern für API-Eingaben

**Status:** akzeptiert
**Datum:** 2026-05

## Kontext

Das Domänenmodell `Risiko` enthält **server-verwaltete Felder** wie `id` und
`version`. Würden diese direkt aus dem Request-Body gelesen, könnte ein
Client beliebige IDs setzen oder die Optimistic-Locking-Version manipulieren.
Außerdem unterscheiden sich Pflichtfelder beim Anlegen (POST) und Updaten
(PATCH).

## Entscheidung

Für die API-Eingaben werden **dedizierte DTOs** verwendet:

- `RisikoCreateDto` – nur Felder, die der Client beim Anlegen senden darf;
  ohne `id` und ohne `version`.
- `RisikoUpdateDto` – alle Felder optional; `version` ist hier die
  **erwartete** Version (Optimistic Locking) und nicht der neue Wert.
- `Risiko` – das volle Antwort-/Domänenmodell, niemals als Eingabe verwendet.

## Alternativen

- **Domänenmodell als Request akzeptieren** – einfach, aber unsicher
  (Mass Assignment, Pflichtfeld-Verwirrung).
- **Pydantic-Modelle** – möglich, würden aber eine zweite Modellschicht
  einführen, ohne dass es nötig ist.

## Begründung

- Klare Trennung: was darf rein vs. was geht raus.
- Verhindert versehentliches Überschreiben server-verwalteter Felder.
- Macht POST und PATCH explizit unterschiedlich (z. B. nur PATCH erlaubt
  partielle Updates).
- Litestar serialisiert Dataclass-DTOs automatisch und validiert Pflichtfelder.

## Konsequenzen

- ➕ Sicherer und expliziter API-Vertrag.
- ➕ Bessere OpenAPI-Doku, da Schemas pro Operation passen.
- ➖ Einige Felder existieren in mehreren Klassen (Domain + zwei DTOs) – kleine
  Duplikation.

