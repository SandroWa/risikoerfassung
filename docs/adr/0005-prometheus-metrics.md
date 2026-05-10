# 0006 – Prometheus für Metriken

**Status:** akzeptiert
**Datum:** 2026-05

## Kontext

Die Anwendung soll grundlegende Beobachtbarkeit (Observability) bieten –
mindestens Request-Anzahl, -Dauer und In-Flight-Requests pro Route, Methode
und Statuscode.

## Entscheidung

Es wird die in Litestar enthaltene **Prometheus-Integration**
(`litestar.contrib.prometheus`) zusammen mit dem offiziellen
[`prometheus_client`](https://github.com/prometheus/client_python) verwendet.
Metriken werden unter **`/metrics`** im Prometheus-Textformat exponiert.

Konfiguration in `app/main.py`:

- `app_name="risikoerfassung"`, `prefix="risikoerfassung"`.
- `group_path=True` → Pfad-Parameter werden als Template-Label gespeichert
  (z. B. `/risiken/{risiko_id}`), um die Label-Kardinalität niedrig zu halten.

## Alternativen

- **OpenTelemetry** – mächtiger (Traces/Logs/Metriken), aber zusätzlicher
  Setup-Aufwand inkl. Collector.
- **Logging only** – zu wenig für Performance-Beobachtung.
- **Eigene Middleware** – Wheel-Reinvention.

## Begründung

- Direkt in Litestar integriert, kaum Code nötig.
- Prometheus-Format ist Industriestandard und wird von Grafana, Alertmanager,
  Loki etc. nativ unterstützt.
- Geringe Laufzeit-Overhead.

## Konsequenzen

- ➕ Einfache Anbindung an bestehende Monitoring-Stacks.
- ➕ Standardisiertes Label-Schema.
- ➖ Reine Metriken – Tracing/Logs müssten separat ergänzt werden.

