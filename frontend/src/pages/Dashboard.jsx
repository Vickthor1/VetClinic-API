import { useEffect, useState } from "react";
import { api } from "../services/api";

export default function Dashboard() {
    const [pets, setPets] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function load() {
            try {
                const res = await api.get("/pets");
                setPets(res.data);
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        }

        load();
    }, []);

    return (
        <div>
            <h1 className="text-2xl font-bold mb-6">Dashboard</h1>

            {loading ? (
                <p>Carregando...</p>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">

                    <div className="bg-white p-6 rounded shadow">
                        <p className="text-slate-500">Total de Pets</p>
                        <p className="text-3xl font-bold">{pets.length}</p>
                    </div>

                    <div className="bg-white p-6 rounded shadow">
                        <p className="text-slate-500">Sistema</p>
                        <p className="text-lg">Online</p>
                    </div>

                    <div className="bg-white p-6 rounded shadow">
                        <p className="text-slate-500">Status</p>
                        <p className="text-lg">Ativo</p>
                    </div>

                </div>
            )}
        </div>
    );
}