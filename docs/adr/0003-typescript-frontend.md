# 0003 – TypeScript im Frontend

**Status:** akzeptiert
**Datum:** 2026-05

## Kontext

Das Frontend kommuniziert mit der Backend-API und arbeitet mit klar
typisierten Datenmodellen (`Risiko`, `RisikoCreate`, Enums wie `Status`).
Fehler in API-Verträgen sollen früh – idealerweise zur Compile-Zeit –
auffallen.

## Entscheidung

Das Frontend wird komplett in **TypeScript** geschrieben (`.tsx` für
Komponenten, `.ts` für Services/Typen).

## Alternativen

- **Plain JavaScript** – weniger Setup, aber keine statische Typprüfung.
- **JSDoc-Typannotationen** – kompromisshaft, in der Praxis weniger ergonomisch.

## Begründung

- API-Verträge (Felder, Enums, Optimistic-Locking-Versionen) sind in
  `src/types.ts` exakt typisiert; Tippfehler führen zu Compile-Fehlern.
- Refactorings (Umbenennen von Feldern, Anpassen von DTOs) sind sicherer.
- Bessere IDE-Unterstützung und Auto-Completion.
- `tsc -b` läuft auch im CI als zusätzlicher Sanity-Check vor dem Vite-Build.

## Konsequenzen

- ➕ Frühzeitige Fehlererkennung, bessere DX.
- ➕ Typsynchronisation zwischen UI und API-Service-Layer.
- ➖ Geringer Mehraufwand für Typdefinitionen.
- ➖ Build-Zeit etwas länger durch Typecheck.

