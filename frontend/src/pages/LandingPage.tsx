import { Link } from "react-router-dom";

export default function LandingPage() {
  return (
    <div className="landing">
      <section className="hero">
        <h2>Willkommen zur Risikoerfassung</h2>
        <p className="subtitle">
          Erfassen, kategorisieren und verfolgen Sie Versicherungsrisiken zentral an einem Ort.
        </p>
        <div className="hero-actions">
          <Link to="/risiken" className="btn primary">
            Zur Risikoliste
          </Link>
        </div>
      </section>
    </div>
  );
}

