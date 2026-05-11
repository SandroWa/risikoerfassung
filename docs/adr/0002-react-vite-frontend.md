# 0002 – React + Vite als Frontend-Stack

**Status:** akzeptiert
**Datum:** 2026-05

## Kontext

Es wird ein kleines Web-UI benötigt, das die Risiken-Liste anzeigt, einen
Anlegen-Dialog bereitstellt und auf das Litestar-Backend zugreift. Der Stack
soll modern, schnell startbar und einfach zu warten sein.

## Entscheidung

Verwendet wird **[React 18](https://react.dev/)** als UI-Library zusammen mit
**[Vite 5](https://vitejs.dev/)** als Dev-Server und Bundler.

## Alternativen

- **Next.js** – bietet SSR/Routing/SSG, ist aber für einen einfachen API-Client
  ohne SEO-Anspruch zu schwergewichtig.
- **Angular** – größere Lernkurve, mehr Konventionen als nötig.
- **Svelte/SvelteKit** – attraktiv, aber weniger verbreitet im Team-Kontext.

## Begründung

- **Vite** bietet extrem schnelle Dev-Server-Starts und Hot-Module-Reloading
  über native ES-Module.
- **React** ist weit verbreitet, gut dokumentiert und passt perfekt zu einem
  einfachen CRUD-Frontend.
- Die Kombination ist „opinion-light": kein SSR, kein File-Routing, keine
  Magie.
- Sehr kleines Bundle ohne große Defaults.

## Konsequenzen

- ➕ Sekundenschneller Dev-Start, schneller Build.
- ➕ Einfache Integration mit TypeScript.
- ➖ Kein eingebautes Routing → wird durch `react-router-dom` ergänzt.
- ➖ Keine SSR (für diese Anwendung aber kein Nachteil).

