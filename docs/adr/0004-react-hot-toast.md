# 0005 – react-hot-toast für Benachrichtigungen

**Status:** akzeptiert
**Datum:** 2026-05

## Kontext

Nutzeraktionen wie „Liste aktualisieren", „Risiko anlegen" oder Fehler beim
Speichern sollen visuell rückgemeldet werden – über kleine, nicht-blockierende
Pop-ups (Toasts) am unteren Bildschirmrand.

## Entscheidung

Verwendet wird **[react-hot-toast](https://react-hot-toast.com/)** (≥ 2.6).
Der globale `<Toaster position="bottom-center" />` wird einmal in `main.tsx`
gemountet; Aufrufe erfolgen überall via `toast.success(...)` /
`toast.error(...)`.

## Alternativen

- **react-toastify** – bekannt, aber größer und API umständlicher.
- **Eigene Implementierung** – unnötig, wenn es eine kleine Bibliothek gibt,
  die das Problem sauber löst.
- **Material UI Snackbar / Chakra UI** – würde eine ganze Component-Library
  reinziehen.

## Begründung

- Sehr kleines Bundle (~5 KB).
- Imperative API (`toast.success("...")`) ist ergonomisch und erfordert
  keinen zusätzlichen Context-/Reducer-Code.
- Built-in `toast.promise(...)` für asynchrone Aktionen.
- Konfigurierbares Default-Styling, das zum Dark-Theme der App passt.

## Konsequenzen

- ➕ Konsistentes Feedback in der gesamten App.
- ➕ Erfolgs- und Fehlerfälle werden mit einer einheitlichen UX behandelt.
- ➖ Weitere kleine Frontend-Abhängigkeit.

