import { useEffect, useState } from "react";
import { api } from "../../services/api";
import { Link } from "react-router-dom";

import Card from "../../components/Card";
import Loading from "../../components/Loading";
import EmptyState from "../../components/EmptyState";

export default function PetsList() {
    const [pets, setPets] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.get("/pets")
            .then(res => setPets(res.data))
            .finally(() => setLoading(false));
    }, []);

    return (
        <div>

            <div className="flex justify-between items-end mb-8">
                <div>
                    <h1 className="text-3xl font-semibold">Pets</h1>
                    <p className="text-slate-500 mt-1">
                        Animais cadastrados na clínica
                    </p>
                </div>

                <Link
                    to="/pets/new"
                    className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
                >
                    + Novo Pet
                </Link>
            </div>

            {loading && <Loading />}

            {!loading && pets.length === 0 && (
                <EmptyState
                    title="Nenhum pet cadastrado"
                    description="Adicione o primeiro pet para começar"
                />
            )}

            {!loading && pets.length > 0 && (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">

                    {pets.map(pet => (
                        <Card
                            key={pet.id}
                            title={pet.name}
                            description={`Espécie: ${pet.species}`}
                        >
                            <div className="flex justify-between mt-3 text-sm">

                                <span className="text-slate-400">
                                    ID: {pet.id}
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