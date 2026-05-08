# Frontend – Risikoerfassung

Vite + React + TypeScript-Frontend mit Listenansicht aller Risiken.

## Setup

```powershell
cd frontend
npm install
```

## Starten (Dev-Server)

Erst das Backend starten (Litestar auf Port 8000):

```powershell
litestar --app app.main:app run --reload
```

Dann in einem zweiten Terminal:

```powershell
cd frontend
npm run dev
```

Geöffnet wird http://127.0.0.1:5173. Der Vite-Devserver leitet alle
Requests von `/api/*` per Proxy an `http://127.0.0.1:8000/*` weiter,
sodass keine CORS-Konfiguration im Backend nötig ist.

## Funktionen

- Listenansicht aller Risiken aus `GET /risiken`
- Filter nach `Risikoart` und `Status`
- Aktualisieren-Button
- Statusanzeige als farbiges Badge

