export type Risikoart = "Gebäude" | "Firma" | "Person";
export type Status = "neu" | "in Bearbeitung" | "policiert";

export interface Risiko {
  id: string;
  risikoart: Risikoart | null;
  versichert_ab_datum: string; // ISO date
  ort_adresse: string | null;
  policennummer: string | null;
  zusammenfassung: string | null;
  status: Status;
  version: number;
  erstellt_am: string; // ISO datetime
}

export interface RisikoCreate {
  versichert_ab_datum: string; // YYYY-MM-DD, Pflicht
  status: Status;              // Pflicht
  risikoart?: Risikoart;
  ort_adresse?: string;
  policennummer?: string;
  zusammenfassung?: string;
}
