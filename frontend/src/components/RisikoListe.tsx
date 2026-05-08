import type { Risiko, Status } from "../types";

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

interface Props {
  risiken: Risiko[];
}

export default function RisikoListe({ risiken }: Props) {
  if (risiken.length === 0) return null;

  return (
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
  );
}

