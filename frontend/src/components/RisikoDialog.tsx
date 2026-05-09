import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { ApiValidationError, createRisiko } from "../service/risiken_service";
import type { Risikoart, Status, RisikoCreate } from "../types";

const RISIKOARTEN: Risikoart[] = ["Gebäude", "Firma", "Person"];
const STATUS_WERTE: Status[] = ["neu", "in Bearbeitung", "policiert"];
const ISO_DATE_RE = /^\d{4}-\d{2}-\d{2}$/;

interface FormState {
  risikoart: string;
  versichert_ab_datum: string;
  ort_adresse: string;
  policennummer: string;
  zusammenfassung: string;
  status: string;
}

const INITIAL: FormState = {
  risikoart: "",
  versichert_ab_datum: "",
  ort_adresse: "",
  policennummer: "",
  zusammenfassung: "",
  status: "neu",
};

interface Props {
  /** Wird aufgerufen, nachdem ein Risiko erfolgreich angelegt wurde. */
  onCreated?: () => void;
  /** Optional: Beschriftung des Buttons. */
  label?: string;
  /** Optional: zusätzliche CSS-Klasse für den Button. */
  className?: string;
}

export default function RisikoDialog({ onCreated, label = "+ Neues Risiko", className }: Props) {
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState<FormState>(INITIAL);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const onClose = () => setOpen(false);

  useEffect(() => {
    if (open) {
      setForm(INITIAL);
      setErrors({});
      setSubmitError(null);
      setSubmitting(false);
    }
  }, [open]);

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onClose]);

  const update = <K extends keyof FormState>(key: K, value: string) => {
    setForm((f) => ({ ...f, [key]: value }));
    setErrors((e) => {
      if (!e[key]) return e;
      const { [key]: _removed, ...rest } = e;
      return rest;
    });
  };

  const validate = (): Record<string, string> => {
    const errs: Record<string, string> = {};
    if (!form.versichert_ab_datum) {
      errs.versichert_ab_datum = "Pflichtfeld";
    } else if (!ISO_DATE_RE.test(form.versichert_ab_datum)) {
      errs.versichert_ab_datum = "Ungültiges Datum (YYYY-MM-DD)";
    } else if (Number.isNaN(new Date(form.versichert_ab_datum).getTime())) {
      errs.versichert_ab_datum = "Ungültiges Datum";
    }
    if (!form.status) {
      errs.status = "Pflichtfeld";
    } else if (!STATUS_WERTE.includes(form.status as Status)) {
      errs.status = "Ungültiger Status";
    }
    if (form.risikoart && !RISIKOARTEN.includes(form.risikoart as Risikoart)) {
      errs.risikoart = "Ungültige Risikoart";
    }
    return errs;
  };

  const buildPayload = (): RisikoCreate => {
    const p: RisikoCreate = {
      versichert_ab_datum: form.versichert_ab_datum,
      status: form.status as Status,
    };
    if (form.risikoart) p.risikoart = form.risikoart as Risikoart;
    if (form.ort_adresse.trim()) p.ort_adresse = form.ort_adresse.trim();
    if (form.policennummer.trim()) p.policennummer = form.policennummer.trim();
    if (form.zusammenfassung.trim()) p.zusammenfassung = form.zusammenfassung.trim();
    return p;
  };

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const v = validate();
    if (Object.keys(v).length > 0) {
      setErrors(v);
      setSubmitError(null);
      toast.error("Bitte Eingaben prüfen");
      return;
    }
    setSubmitting(true);
    setSubmitError(null);
    try {
      await createRisiko(buildPayload());
      setOpen(false);
      onCreated?.();
    } catch (err) {
      let msg: string;
      if (err instanceof ApiValidationError) {
        setErrors(err.fieldErrors);
        setSubmitError(err.message);
        msg = err.message;
      } else {
        msg = err instanceof Error ? err.message : "Unbekannter Fehler";
        setSubmitError(msg);
      }
      toast.error(`Fehler beim Anlegen: ${msg}`);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <>
      <button
        type="button"
        className={className ?? "btn primary"}
        onClick={() => setOpen(true)}
      >
        {label}
      </button>

      {open && (
        <div className="dialog-overlay" onClick={onClose}>
          <div className="dialog" onClick={(e) => e.stopPropagation()}>
            <div className="dialog-header">
              <h2>Neues Risiko anlegen</h2>
              <button type="button" className="icon-btn" onClick={onClose} aria-label="Schließen">
                ×
              </button>
            </div>

            <form onSubmit={onSubmit} noValidate>
              <div className="form-grid">
                <div className="field">
                  <label htmlFor="f-risikoart">Risikoart</label>
                  <select
                    id="f-risikoart"
                    value={form.risikoart}
                    onChange={(e) => update("risikoart", e.target.value)}
                  >
                    <option value="">— nicht angeben —</option>
                    {RISIKOARTEN.map((r) => (
                      <option key={r} value={r}>{r}</option>
                    ))}
                  </select>
                  {errors.risikoart && <div className="field-error">{errors.risikoart}</div>}
                </div>

                <div className="field">
                  <label htmlFor="f-datum">Versichert ab *</label>
                  <input
                    id="f-datum"
                    type="date"
                    required
                    value={form.versichert_ab_datum}
                    onChange={(e) => update("versichert_ab_datum", e.target.value)}
                  />
                  {errors.versichert_ab_datum && (
                    <div className="field-error">{errors.versichert_ab_datum}</div>
                  )}
                </div>

                <div className="field">
                  <label htmlFor="f-status">Status *</label>
                  <select
                    id="f-status"
                    required
                    value={form.status}
                    onChange={(e) => update("status", e.target.value)}
                  >
                    {STATUS_WERTE.map((s) => (
                      <option key={s} value={s}>{s}</option>
                    ))}
                  </select>
                  {errors.status && <div className="field-error">{errors.status}</div>}
                </div>

                <div className="field">
                  <label htmlFor="f-policennummer">Policennummer</label>
                  <input
                    id="f-policennummer"
                    type="text"
                    value={form.policennummer}
                    onChange={(e) => update("policennummer", e.target.value)}
                  />
                  {errors.policennummer && <div className="field-error">{errors.policennummer}</div>}
                </div>

                <div className="field field--full">
                  <label htmlFor="f-ort">Ort / Adresse</label>
                  <input
                    id="f-ort"
                    type="text"
                    value={form.ort_adresse}
                    onChange={(e) => update("ort_adresse", e.target.value)}
                  />
                  {errors.ort_adresse && <div className="field-error">{errors.ort_adresse}</div>}
                </div>

                <div className="field field--full">
                  <label htmlFor="f-zusammenfassung">Zusammenfassung</label>
                  <textarea
                    id="f-zusammenfassung"
                    rows={3}
                    value={form.zusammenfassung}
                    onChange={(e) => update("zusammenfassung", e.target.value)}
                  />
                  {errors.zusammenfassung && (
                    <div className="field-error">{errors.zusammenfassung}</div>
                  )}
                </div>
              </div>

              {submitError && <div className="error" style={{ marginTop: "1rem" }}>⚠ {submitError}</div>}

              <div className="dialog-actions">
                <button type="submit" className="btn primary" disabled={submitting}>
                  {submitting ? "Speichern…" : "Speichern"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  );
}
