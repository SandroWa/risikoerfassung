# Risikoerfassung

Kleine Litestar-Anwendung zur Erfassung von Risiken.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Starten

```powershell
litestar --app app.main:app run --reload
```

Anschließend erreichbar unter:

- API-Root: http://127.0.0.1:8000/
- Swagger UI: http://127.0.0.1:8000/schema/swagger
- Risiken-Endpunkte: http://127.0.0.1:8000/risiken

## Endpunkte

| Methode | Pfad                  | Beschreibung              |
|---------|-----------------------|---------------------------|
| GET     | `/risiken`            | Alle Risiken auflisten    |
| GET     | `/risiken/{id}`       | Einzelnes Risiko abrufen  |
| POST    | `/risiken`            | Neues Risiko anlegen      |
| PATCH   | `/risiken/{id}`       | Risiko aktualisieren      |
| DELETE  | `/risiken/{id}`       | Risiko löschen            |

## Datenmodell

Ein `Risiko` besteht aus:

| Feld                  | Typ                                          | Beschreibung                          |
|-----------------------|----------------------------------------------|---------------------------------------|
| `id`                  | UUID (auto)                                  | Eindeutige ID                         |
| `risikoart`           | Enum: `Gebäude`, `Firma`, `Person`           | Art des Risikos                       |
| `versichert_ab_datum` | Datum (ISO 8601, z. B. `2026-05-08`)         | Beginn des Versicherungsschutzes      |
| `ort_adresse`         | Text                                         | Ort bzw. Adresse                      |
| `policennummer`       | Text                                         | Policennummer                         |
| `zusammenfassung`     | Text                                         | Zusammenfassung des Risikos           |
| `status`              | Enum: `neu`, `in Bearbeitung`, `policiert`   | Bearbeitungsstatus (Default: `neu`)   |
| `erstellt_am`         | DateTime (auto)                              | Erstellungszeitpunkt                  |

Die Liste `GET /risiken` unterstützt zusätzlich die optionalen Query-Parameter `risikoart` und `status` zum Filtern.

### Beispiel: Risiko anlegen

```json
POST /risiken
{
  "risikoart": "Gebäude",
  "versichert_ab_datum": "2026-05-08",
  "ort_adresse": "Hauptstraße 1, 12345 Musterstadt",
  "policennummer": "POL-2026-0001",
  "zusammenfassung": "Mehrfamilienhaus mit 8 Wohneinheiten",
  "status": "neu"
}
```

