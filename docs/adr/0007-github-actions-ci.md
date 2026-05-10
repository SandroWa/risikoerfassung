# 0008 – GitHub Actions als CI/CD

**Status:** akzeptiert
**Datum:** 2026-05

## Kontext

Bei Änderungen sollen automatisch Tests laufen, das Frontend gebaut und ein
Release-Artefakt erzeugt werden, ohne dass dies manuell geschieht.

## Entscheidung

Es wird **GitHub Actions** mit dem Workflow `.github/workflows/ci.yml`
verwendet. Drei Jobs:

1. `backend-tests` – pytest mit Python 3.14.
2. `frontend-build` – Node 20 + Vite Build (`npm run build`).
3. `package` – baut nach erfolgreichen Vorgängern ein `.tar.gz` und `.zip`
   aus Backend + Frontend-Build.

## Alternativen

- **GitLab CI** – setzt GitLab als Hoster voraus.
- **Jenkins** – eigene Infrastruktur nötig.
- **CircleCI / Travis** – externe Services, zusätzliche Accounts/Setups.

## Begründung

- Kein zusätzliches Hosting nötig, da das Repository ohnehin auf GitHub liegt.
- Action-Marketplace bietet fertige Bausteine
  (`actions/setup-python`, `actions/setup-node`, `actions/upload-artifact`).
- Kostenlos für öffentliche/kleine Repos.
- Caching für `pip` und `npm` direkt eingebaut.

## Konsequenzen

- ➕ Sofort einsatzbereit, keine Extra-Infra.
- ➕ Versionierung der Pipeline neben dem Code.
- ➖ Vendor-Lock-in zu GitHub – ein Wechsel zu z. B. GitLab erfordert
  Workflow-Übersetzung.

