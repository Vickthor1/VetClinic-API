import { useLocation, useNavigate } from "react-router-dom";

export default function Header({ title }) {
    const navigate = useNavigate();
    const location = useLocation();

    const isHome = location.pathname === "/";

    return (
        <header className="bg-white border-b px-6 py-4 flex items-center justify-between">

            <h1 className="font-semibold text-slate-700">
                {title}
            </h1>

            {!isHome && (
                <button
                    onClick={() => navigate(-1)}
                    className="text-sm bg-slate-200 px-3 py-1 rounded hover:bg-slate-300"
                >
                    ← Voltar
                </button>
            )}

        </header>
    );
}