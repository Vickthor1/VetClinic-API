import { useEffect, useState } from "react";
import { api } from "../../services/api";
import { Link } from "react-router-dom";

import Card from "../../components/Card";
import Loading from "../../components/Loading";
import EmptyState from "../../components/EmptyState";

export default function TutorsList() {
    const [tutors, setTutors] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.get("/tutors")
            .then(res => setTutors(res.data))
            .finally(() => setLoading(false));
    }, []);

    return (
        <div>

            <div className="flex justify-between items-center mb-6">
                <div>
                    <h1 className="text-2xl font-bold">Tutores</h1>
                    <p className="text-sm text-slate-500">
                        Clientes da clínica
                    </p>
                </div>

                <Link
                    to="/tutors/new"
                    className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
                >
                    + Novo Tutor
                </Link>
            </div>

            {loading && <Loading />}

            {!loading && tutors.length === 0 && (
                <EmptyState
                    title="Nenhum tutor cadastrado"
                    description="Adicione clientes para começar"
                />
            )}

            {!loading && tutors.length > 0 && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">

                    {tutors.map(tutor => (
                        <Card
                            key={tutor.id}
                            title={tutor.name}
                            description={tutor.email}
                        >
                            <div className="flex justify-between mt-3 text-sm">

                                <span className="text-slate-400">
                                    ID: {tutor.id}
                                </span>

                                <div className="flex gap-3">
                                    <button className="text-blue-600 hover:underline">
                                        Editar
                                    </button>
                                    <button className="text-red-500 hover:underline">
                                        Excluir
                                    </button>
                                </div>

                            </div>
                        </Card>
                    ))}

                </div>
            )}

        </div>
    );
}