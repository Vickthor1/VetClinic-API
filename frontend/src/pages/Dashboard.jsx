import { Link } from "react-router-dom";

export default function Dashboard() {
    return (
        <div className="min-h-screen bg-slate-100 p-8">
            <h1 className="text-4xl font-bold mb-6">
                VetClinic Dashboard
            </h1>

            <div className="grid grid-cols-2 gap-4">
                <Link
                    to="/tutors"
                    className="bg-white p-6 rounded shadow"
                >
                    Tutores
                </Link>

                <Link
                    to="/pets"
                    className="bg-white p-6 rounded shadow"
                >
                    Animais
                </Link>

                <Link
                    to="/veterinarians"
                    className="bg-white p-6 rounded shadow"
                >
                    Veterinários
                </Link>

                <Link
                    to="/appointments"
                    className="bg-white p-6 rounded shadow"
                >
                    Consultas
                </Link>
            </div>
        </div>
    );
}