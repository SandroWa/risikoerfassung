# 0001 – Litestar als Backend-Framework

**Status:** akzeptiert
**Datum:** 2026-05

## Kontext

Für die Backend-API zur Risikoerfassung wurde ein modernes Python-Web-Framework
mit guter Type-Hint-Unterstützung, automatischer OpenAPI-Generierung und
einfachem Dependency-Injection-Modell benötigt.

## Entscheidung

Es wird **[Litestar](https://litestar.dev/)** (≥ 2.8) als Web-Framework
verwendet.

## Alternativen

- **FastAPI** – sehr verbreitet, basiert auf Starlette + Pydantic. Vergleichbar in
  vielen Aspekten.
- **Flask** – Klassiker, aber kein eingebautes async, keine OpenAPI-Generierung
  ohne Extensions, kein DI.
- **Django REST Framework** – zu schwergewichtig für ein kleines API-Projekt.

## Begründung

- **Class-Based Controller** mit `@get`, `@post`, … erlauben eine saubere
  Strukturierung pro Ressource (`RisikoController`).
- **Built-in Dependency Injection** (`Provide(...)`) ermöglicht einfaches
  Austauschen des Service in Tests.
- **Automatische OpenAPI-Doku + Swagger UI** unter `/schema/swagger`.
- **Native Unterstützung für Dataclasses** als Request-/Response-Modelle –
  wir brauchen kein zusätzliches ORM oder Pydantic.
- **First-class async** und gute Performance.
- Eingebaute Integrationen wie der **Prometheus-Controller**.

## Konsequenzen

- ➕ Wenig Boilerplate, klare Trennung Controller/Service.
- ➕ DTOs sind reine Python-Dataclasses → kein zusätzliches Schema-Layer.
- ➖ Kleinere Community als FastAPI; weniger Stack-Overflow-Antworten.
- ➖ Litestar-spezifisches Wissen ist nicht 1:1 auf andere Frameworks übertragbar.

