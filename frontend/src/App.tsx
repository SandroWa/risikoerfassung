import { NavLink, Outlet } from "react-router-dom";

export default function App() {
  return (
    <div className="container">
      <header className="header">
        <h1>Risikoerfassung</h1>
        <nav className="nav">
          <NavLink
            to="/"
            end
            className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}
          >
            Startseite
          </NavLink>
          <NavLink
            to="/risiken"
            className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}
          >
            Risiken
          </NavLink>
        </nav>
      </header>

      <Outlet />
    </div>
  );
}
