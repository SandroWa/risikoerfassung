# 1001 – Layered Architecture (Controller → Service → Modell)

**Status:** akzeptiert
**Datum:** 2026-05

## Kontext

Die Backend-Logik soll klar in Verantwortlichkeiten getrennt sein: HTTP-Handling
(Routing, Statuscodes, Serialisierung) gehört nicht in dieselbe Schicht wie
Geschäftslogik oder Datenmodelle.

## Entscheidung

Es wird eine klassische **dreischichtige Architektur** implementiert:

```
RisikoController  →  RisikoService  →  Risiko (Domänenmodell) + Store
   (HTTP-Layer)      (Geschäftslogik)        (Daten/State)
```

- **Controller (`app/controller/`)** – nimmt HTTP-Requests entgegen, mappt
  DTOs, übersetzt Domain-Exceptions in HTTP-Statuscodes
  (`RisikoNotFoundError` → 404, `RisikoVersionConflictError` → 409).
- **Service (`app/service/`)** – enthält die gesamte Geschäftslogik
  (Filtern, Optimistic Locking, Versionsverwaltung).
- **Model (`app/models/`)** – pure Datenklassen ohne Logik.

## Alternativen

- **Fat Controller** mit gesamter Logik direkt in den HTTP-Handlern – schnell
  zu schreiben, aber schwer testbar und nicht wiederverwendbar.
- **Hexagonal/Clean Architecture** – noch sauberer, für die Größe des Projekts
  jedoch übertrieben.

## Begründung

- **Testbarkeit:** Der Service ist ohne HTTP-Stack instanziierbar → schnelle
  Unit-Tests (siehe `tests/test_risiko_service.py`).
- **Austauschbarkeit:** Der Store kann später durch eine echte Datenbank
  ersetzt werden, ohne den Controller anzufassen.
- **Lesbarkeit:** Jeder Modul-Pfad spiegelt seine Aufgabe wider.

## Konsequenzen

- ➕ Klare Verantwortlichkeiten, einfache Tests.
- ➕ HTTP-Details bleiben aus der Geschäftslogik raus.
- ➖ Mehr Dateien/Module für ein eigentlich kleines Projekt.
- ➖ Bei sehr trivialen Endpunkten ein wenig Boilerplate.

