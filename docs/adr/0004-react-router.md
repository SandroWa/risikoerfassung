# 0004 – react-router-dom für Client-Routing

**Status:** akzeptiert
**Datum:** 2026-05

## Kontext

Das Frontend hat (mindestens) zwei Ansichten – eine **Landing Page** und eine
**Risiken-Seite**. Die Navigation soll über URLs ansprechbar und mit dem
Browser-Verlauf kompatibel sein.

## Entscheidung

Es wird **[react-router-dom v6](https://reactrouter.com/)** für das
Client-seitige Routing verwendet.

## Alternativen

- **Eigene State-Variable** statt URL-basiertem Routing – einfacher, aber
  ohne URL-Sharing/Back-Button-Unterstützung.
- **TanStack Router** – mächtiger, aber Overkill für 2–3 Routen.
- **Wouter** – kleinerer Footprint, aber weniger bekannt.

## Begründung

- De-facto-Standard in der React-Welt, sehr gute Doku.
- Reicht für die geringe Komplexität locker aus (`<BrowserRouter>` +
  `<Routes>`).
- Ermöglicht spätere Erweiterung (Detailseiten, geschützte Routen) ohne
  Architekturwechsel.

## Konsequenzen

- ➕ Bookmarkable URLs, funktionierender Back/Forward-Button.
- ➕ Einfacher Einstieg für Entwickler, die React-Router bereits kennen.
- ➖ Zusätzliche Abhängigkeit für ein recht kleines UI.

