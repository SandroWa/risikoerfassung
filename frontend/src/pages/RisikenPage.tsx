import { useEffect, useState, useCallback } from "react";
import { fetchRisiken } from "../api";
import type { Risiko, Risikoart, Status } from "../types";
import RisikoDialog from "../components/RisikoDialog";
import RisikoListe from "../components/RisikoListe";

const RISIKOARTEN: Risikoart[] = ["Gebäude", "Firma", "Person"];
const STATUS_WERTE: Status[] = ["neu", "in Bearbeitung", "policiert"];

export default function RisikenPage() {
  const [risiken, setRisiken] = useState<Risiko[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [filterRisikoart, setFilterRisikoart] = useState<string>("");
  const [filterStatus, setFilterStatus] = useState<string>("");
  const [dialogOpen, setDialogOpen] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchRisiken({
        risikoart: filterRisikoart || undefined,
        status: filterStatus || undefined,
      });
      setRisiken(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Unbekannter Fehler");
    } finally {
      setLoading(false);
    }
  }, [filterRisikoart, filterStatus]);

  useEffect(() => {
    void load();
  }, [load]);

  return (
    <>
      <p className="subtitle">Übersicht aller erfassten Risiken</p>

      <section className="toolbar">
        <label>
          Risikoart:
          <select
            value={filterRisikoart}
            onChange={(e) => setFilterRisikoart(e.target.value)}
          >
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

        <button onClick={() => void load()} disabled={loading}>
          {loading ? "Lädt…" : "Aktualisieren"}
        </button>

        <button
          type="button"
          className="btn primary"
          onClick={() => setDialogOpen(true)}
          style={{ marginLeft: "auto" }}
        >
          + Neues Risiko
        </button>
      </section>

      {error && <div className="error">⚠ {error}</div>}

      {!error && !loading && risiken.length === 0 && (
        <div className="empty">Keine Risiken vorhanden.</div>
      )}

      <RisikoListe risiken={risiken} />

      <RisikoDialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        onCreated={() => {
          setDialogOpen(false);
          void load();
        }}
      />
    </>
  );
}
