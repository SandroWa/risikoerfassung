import { useCallback, useEffect, useRef, useState } from "react";
import toast from "react-hot-toast";
import { fetchRisiken } from "../service/risiken_service";
import type { Risiko, Risikoart, Status } from "../types";
import RisikoDialog from "./RisikoDialog.tsx";

const RISIKOARTEN: Risikoart[] = ["Gebäude", "Firma", "Person"];
const STATUS_WERTE: Status[] = ["neu", "in Bearbeitung", "policiert"];

function formatDate(value: string | null | undefined): string {
  if (!value) return "—";
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return value;
  return d.toLocaleDateString("de-DE");
}

function statusBadgeClass(status: Status): string {
  switch (status) {
    case "neu":
      return "badge badge--neu";
    case "in Bearbeitung":
      return "badge badge--bearbeitung";
    case "policiert":
      return "badge badge--policiert";
  }
}

export default function RisikoListe() {
  const [risiken, setRisiken] = useState<Risiko[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [filterRisikoart, setFilterRisikoart] = useState<string>("");
  const [filterStatus, setFilterStatus] = useState<string>("");
  const [reloadKey, setReloadKey] = useState(0);
  const isInitialLoad = useRef(true);

  const load = useCallback(async (notify = false) => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchRisiken({
        risikoart: filterRisikoart || undefined,
        status: filterStatus || undefined,
      });
      setRisiken(data);
      if (notify) {
        toast.success(`Liste aktualisiert (${data.length} Einträge)`);
      }
    } catch (e) {
      const msg = e instanceof Error ? e.message : "Unbekannter Fehler";
      setError(msg);
      if (notify) toast.error(msg);
    } finally {
      setLoading(false);
    }
  }, [filterRisikoart, filterStatus]);

  useEffect(() => {
    const notify = !isInitialLoad.current;
    isInitialLoad.current = false;
    void load(notify);
  }, [load, reloadKey]);

  return (
    <>
      <section className="toolbar">
        <label>
          Risikoart:
          <select
            value={filterRisikoart}
            onChange={(e) => setFilterRisikoart(e.target.value)}>
            <option value="">Alle</option>
            {RISIKOARTEN.map((r) => (
              <option key={r} value={r}>
                {r}
              </option>
            ))}
          </select>
        </label>

        <label>
          Status:
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
          >
            <option value="">Alle</option>
            {STATUS_WERTE.map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>
        </label>

        <button onClick={() => void load(true)} disabled={loading}>
          {loading ? "Lädt…" : "Aktualisieren"}
        </button>

        <div style={{ marginLeft: "auto" }}>
          <RisikoDialog onCreated={() => {
            toast.success("Risiko erfolgreich angelegt");
            setReloadKey((k) => k + 1);
          }} />
        </div>
      </section>

      {error && <div className="error">⚠ {error}</div>}

      {!error && !loading && risiken.length === 0 && (
        <div className="empty">Keine Risiken vorhanden.</div>
      )}

      {risiken.length > 0 && (
        <div className="table-wrapper">
          <table className="risiko-table">
            <thead>
              <tr>
                <th>Policennummer</th>
                <th>Risikoart</th>
                <th>Versichert ab</th>
                <th>Ort / Adresse</th>
                <th>Zusammenfassung</th>
                <th>Status</th>
                <th>Version</th>
              </tr>
            </thead>
            <tbody>
              {risiken.map((r) => (
                <tr key={r.id}>
                  <td>{r.policennummer ?? "—"}</td>
                  <td>{r.risikoart ?? "—"}</td>
                  <td>{formatDate(r.versichert_ab_datum)}</td>
                  <td>{r.ort_adresse ?? "—"}</td>
                  <td className="summary">{r.zusammenfassung ?? "—"}</td>
                  <td>
                    <span className={statusBadgeClass(r.status)}>{r.status}</span>
                  </td>
                  <td>{r.version}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="count">{risiken.length} Eintrag/Einträge</div>
        </div>
      )}
    </>
  );
}
