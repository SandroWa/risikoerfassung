# 1004 – Optimistic Locking via `version`-Feld

**Status:** akzeptiert
**Datum:** 2026-05

## Kontext

Mehrere Clients (z. B. zwei Browser-Tabs) könnten gleichzeitig dasselbe
Risiko bearbeiten. Ohne Schutz würde der zuletzt schreibende Client die
Änderungen des anderen unbemerkt überschreiben („Lost Update"-Problem).

## Entscheidung

Es wird **Optimistic Locking** über ein `version`-Feld am `Risiko`
implementiert:

- Beim Anlegen: `version = 1`.
- Bei `PATCH /risiken/{id}`: Client schickt die ihm bekannte Version im Body
  mit. Bei Mismatch wirft der Service `RisikoVersionConflictError`, der
  Controller antwortet mit **HTTP 409**.
- Bei `DELETE /risiken/{id}`: Erwartete Version als Query-Parameter
  `?version=<n>`.
- Nach erfolgreichem Update wird `version` serverseitig hochgezählt.

## Alternativen

- **Pessimistisches Locking** (Datenbank-Locks oder Mutex) – aufwändig,
  blockiert andere Requests, für eine HTTP-API praktisch ungeeignet.
- **Last-Write-Wins** – einfach, aber führt zu Datenverlusten und ist für
  fachliche Daten inakzeptabel.
- **ETag / If-Match-Header** – sehr REST-pur, aber für eine kleine API
  schwerer zu implementieren als ein einfaches Feld im Body.

## Begründung

- Sehr leichtgewichtig: nur ein zusätzliches Feld am Modell.
- Skaliert ohne Locks – passend zu HTTP/Stateless-Servern.
- Klare Fehlersemantik (409 Conflict) für den Client.
- Frontend kann den Konflikt erkennen, neu laden und den Nutzer informieren.

## Konsequenzen

- ➕ Verhindert Lost Updates ohne Performance-Einbußen.
- ➕ Klare API-Semantik via 409.
- ➖ Clients **müssen** die Version mitsenden – sonst bewusster Konflikt.
- ➖ Erweiterung um echte Datenbank erfordert, dass dort dieselbe Logik
  konsistent angewendet wird (z. B. SQLAlchemy `version_id_col`).

