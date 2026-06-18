import { NavLink } from "react-router-dom";

export default function Sidebar() {
    const linkClass = ({ isActive }) =>
        `px-4 py-2 rounded transition block ${
            isActive
                ? "bg-blue-600 text-white"
                : "text-slate-600 hover:bg-slate-200"
        }`;

    return (
        <aside className="w-64 bg-white border-r p-4 space-y-2">
            
            <h1 className="text-xl font-bold mb-6">🐾 VetClinic</h1>

            <NavLink to="/" end className={linkClass}>
                Dashboard
            </NavLink>

            <NavLink to="/pets" className={linkClass}>
                Pets
            </NavLink>

            <NavLink to="/tutors" className={linkClass}>
                Tutores
            </NavLink>

            <NavLink to="/veterinarians" className={linkClass}>
                Veterinários
            </NavLink>

        </aside>
    );
}