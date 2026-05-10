# Architecture Decision Records (ADR)

Dieser Ordner enthält **Architecture Decision Records** – kurze Markdown-Dokumente,
die die wichtigsten Architektur- und Technologieentscheidungen des Projekts
festhalten und jeweils begründen.

Format orientiert sich locker an [Michael Nygards ADR-Template](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions):

- **Kontext** – Warum musste eine Entscheidung getroffen werden?
- **Entscheidung** – Was wurde gewählt?
- **Alternativen** – Was wurde betrachtet?
- **Konsequenzen** – Was bedeutet das positiv/negativ?

## Übersicht

### Frameworks & Bibliotheken

| Nr.  | Titel                                              |
|------|----------------------------------------------------|
| 0001 | [Litestar als Backend-Framework](0001-litestar-backend.md) |
| 0002 | [React + Vite als Frontend-Stack](0002-react-vite-frontend.md) |
| 0003 | [TypeScript im Frontend](0003-typescript-frontend.md) |
| 0004 | [react-hot-toast für Benachrichtigungen](0004-react-hot-toast.md) |
| 0005 | [Prometheus für Metriken](0005-prometheus-metrics.md) |
| 0006 | [pytest für Tests](0006-pytest-testing.md) |
| 0007 | [GitHub Actions als CI/CD](0007-github-actions-ci.md) |

### Architektur-Prinzipien

| Nr.  | Titel                                              |
|------|----------------------------------------------------|
| 1001 | [Layered Architecture (Controller → Service → Model)](1001-layered-architecture.md) |
| 1002 | [DTO-Pattern für API-Eingaben](1002-dto-pattern.md) |

