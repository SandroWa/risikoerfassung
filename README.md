# Risikoerfassung

Kleine **Litestar**-basierte Beispielanwendung zur Erfassung von Risiken
(Gebäude, Firmen, Personen) mit einem React/Vite-Frontend.

Das Projekt dient primär zu Lern- und Demozwecken und nutzt einen
**In-Memory-Store** – es gibt also (noch) keine Datenbank.

---

## Projektstruktur

```
risikoerfassung/
├── app/                         # Backend (Litestar)
│   ├── main.py                  # Litestar-App, OpenAPI, Prometheus, Startup-Hooks
│   ├── seed.py                  # Beispiel-Daten beim Start
│   ├── controller/
│   │   └── risiko_controller.py # HTTP-Endpunkte unter /risiken
│   ├── service/
│   │   └── risiko_service.py    # Geschäftslogik + In-Memory-Store
│   └── models/
│       └── risiko/
│           └── risiko_models.py # Domänenmodelle, DTOs, Enums
├── frontend/                    # Vite + React + TypeScript
│   └── src/
│       ├── pages/               # Landing- und Risiken-Seite
│       ├── components/          # Dialog & Liste
│       └── service/             # API-Aufrufe ans Backend
├── tests/                       # pytest Unit-Tests
└── requirements.txt
```

---

## Backend-Domain

Die Backend-Domain dreht sich um eine zentrale Entität: **`Risiko`**.

### Klassen / Module

| Modul                                  | Klasse / Funktion              | Aufgabe                                                                                |
|----------------------------------------|--------------------------------|----------------------------------------------------------------------------------------|
| `app.models.risiko.risiko_models`      | `Risikoart` (Enum)             | Erlaubte Werte: `Gebäude`, `Firma`, `Person`                                            |
|                                        | `Status` (Enum)                | Erlaubte Werte: `neu`, `in Bearbeitung`, `policiert`                                    |
|                                        | `Risiko` (Dataclass)           | Domänen-/Antwortmodell                                                                  |
|                                        | `RisikoCreateDto` (Dataclass)  | Eingabemodell für `POST /risiken` (ohne `id`/`version`)                                 |
|                                        | `RisikoUpdateDto` (Dataclass)  | Eingabemodell für `PATCH /risiken/{id}` (Optimistic Locking via `version`)              |
| `app.service.risiko_service`           | `RisikoService`                | Geschäftslogik: `list / get / create / update / delete` mit Optimistic Locking          |
|                                        | `RisikoNotFoundError`          | Wird geworfen, wenn eine ID nicht existiert                                             |
|                                        | `RisikoVersionConflictError`   | Wird bei Versionskonflikten (Optimistic Locking) geworfen                               |
| `app.controller.risiko_controller`     | `RisikoController`             | Litestar-Controller, mappt HTTP-Routen auf den Service                                  |
|                                        | `provide_risiko_service`       | DI-Provider für `RisikoService`                                                         |
| `app.main`                             | `app`                          | `Litestar`-App mit OpenAPI, Prometheus-Middleware und Seeding beim Start                |
| `app.seed`                             | `seed_risiken`                 | Legt beim Startup ein paar Beispieldaten in den In-Memory-Store                         |

### Architekturprinzip

```
HTTP-Request → RisikoController → RisikoService → In-Memory-Store
                       ↑                ↑
                  DTOs/Enums     Domänenmodell `Risiko`
```

- **Controller** kümmert sich nur um HTTP/DTO-Mapping und übersetzt Domain-Exceptions in HTTP-Statuscodes
  (`RisikoNotFoundError` → 404, `RisikoVersionConflictError` → 409).
- **Service** enthält die gesamte Geschäftslogik und verwaltet den Store sowie das
  Optimistic Locking (Version wird serverseitig hochgezählt).
- **Modelle** sind reine Dataclasses – `id` und `version` werden vom Server vergeben.

---

## Datenmodell

Ein `Risiko` besteht aus:

| Feld                  | Typ                                          | Pflicht | Beschreibung                                |
|-----------------------|----------------------------------------------|---------|---------------------------------------------|
| `id`                  | UUID                                         | auto    | Eindeutige ID, vom Server vergeben          |
| `version`             | int                                          | auto    | Optimistic-Locking-Version (startet bei 1)  |
| `versichert_ab_datum` | Datum (ISO 8601, z. B. `2026-05-08`)         | ja      | Beginn des Versicherungsschutzes            |
| `status`              | Enum: `neu`, `in Bearbeitung`, `policiert`   | ja      | Bearbeitungsstatus                          |
| `risikoart`           | Enum: `Gebäude`, `Firma`, `Person`           | nein    | Art des Risikos                             |
| `ort_adresse`         | Text                                         | nein    | Ort bzw. Adresse                            |
| `policennummer`       | Text                                         | nein    | Policennummer                               |
| `zusammenfassung`     | Text                                         | nein    | Zusammenfassung des Risikos                 |

### Optimistic Locking

- Beim Anlegen wird `version = 1` gesetzt.
- Bei `PATCH` muss der Client die **aktuell ihm bekannte** Version im Body
  mitschicken (`"version": 1`). Stimmt sie nicht überein, antwortet das Backend mit **HTTP 409**.
- Bei `DELETE` muss die erwartete Version als Query-Parameter `?version=…` mitgegeben werden.

---

## Endpunkte

Alle Risiko-Endpunkte liegen unter `/risiken`.

| Methode | Pfad                          | Beschreibung                                              | Status-Codes                |
|---------|-------------------------------|-----------------------------------------------------------|-----------------------------|
| GET     | `/`                           | Service-Info (Name, Doku-/Metrics-Pfad)                   | 200                         |
| GET     | `/risiken`                    | Liste aller Risiken (Filter: `?risikoart=…`, `?status=…`) | 200                         |
| GET     | `/risiken/{risiko_id}`        | Einzelnes Risiko abrufen                                  | 200, 404                    |
| POST    | `/risiken`                    | Neues Risiko anlegen                                      | 201, 400                    |
| PATCH   | `/risiken/{risiko_id}`        | Risiko aktualisieren (Body enthält erwartete `version`)   | 200, 400, 404, 409          |
| DELETE  | `/risiken/{risiko_id}`        | Risiko löschen (Query: `?version=<n>`)                    | 204, 404, 409               |
| GET     | `/schema/swagger`             | Swagger UI                                                | 200                         |
| GET     | `/schema/openapi.json`        | OpenAPI-Spezifikation                                     | 200                         |
| GET     | `/metrics`                    | Prometheus-Metriken                                       | 200                         |

### Beispiel: Risiko anlegen

```http
POST /risiken
Content-Type: application/json

{
  "risikoart": "Gebäude",
  "versichert_ab_datum": "2026-05-08",
  "ort_adresse": "Hauptstraße 1, 12345 Musterstadt",
  "policennummer": "POL-2026-0001",
  "zusammenfassung": "Mehrfamilienhaus mit 8 Wohneinheiten",
  "status": "neu"
}
```

### Beispiel: Risiko aktualisieren

```http
PATCH /risiken/2c1f…  (UUID)
Content-Type: application/json

{
  "status": "policiert",
  "version": 1
}
```

---

## Setup & Start

### Voraussetzungen

- **Python 3.12+** (entwickelt mit 3.14)
- **Node.js 20+** und **npm** (nur für das Frontend)

### 1) Backend

```powershell
# Repository klonen und ins Projekt wechseln
cd risikoerfassung

# Virtuelles Environment anlegen und aktivieren
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Abhängigkeiten installieren
pip install -r requirements.txt

# Anwendung starten (mit Auto-Reload)
litestar --app app.main:app run --reload
```

Backend-URLs nach dem Start:

| Pfad                                  | Inhalt                          |
|---------------------------------------|---------------------------------|
| http://127.0.0.1:8000/                | API-Root (Service-Info)         |
| http://127.0.0.1:8000/risiken         | Risiko-Endpunkte                |
| http://127.0.0.1:8000/schema/swagger  | Swagger UI                      |
| http://127.0.0.1:8000/metrics         | Prometheus-Metriken             |

### 2) Frontend

```powershell
cd frontend
npm install
npm run dev
```

Das Frontend ist anschließend unter http://127.0.0.1:5173 erreichbar und
spricht standardmäßig das Backend auf Port `8000` an.

Produktions-Build:

```powershell
npm run build      # baut nach frontend/dist
npm run preview    # liefert den Build zum lokalen Anschauen aus
```

### 3) Tests ausführen

```powershell
# Im aktivierten venv:
pip install pytest
python -m pytest tests/ -v
```

Die Test-Suite (`tests/test_risiko_service.py`) deckt den `RisikoService`
inklusive Optimistic-Locking-Verhalten ab. Jeder Test setzt den
In-Memory-Store über `setup_method` zurück, sodass sich die Tests nicht
gegenseitig beeinflussen.

---

## Architekturentscheidungen

Die wichtigsten Entscheidungen zu Frameworks und Prinzipien sind als
**Architecture Decision Records (ADR)** unter [`docs/adr/`](docs/adr/README.md)
dokumentiert – jeweils mit Kontext, Entscheidung, Alternativen und
Konsequenzen.

---

## CI/CD

Im Verzeichnis `.github/workflows/ci.yml` liegt ein GitHub-Actions-Workflow,
der bei jedem Push / Pull-Request:

1. die **Backend-Tests** mit pytest ausführt,
2. das **Frontend** mit Vite baut und
3. ein **Release-Artefakt** (`.tar.gz` und `.zip`) aus Backend + Frontend-Build paketiert.
