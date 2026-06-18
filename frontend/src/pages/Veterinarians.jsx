import { useEffect, useState } from "react";
import { api } from "../services/api";

export default function Veterinarians() {
    const [vets, setVets] = useState([]);

    useEffect(() => {
        async function fetchVeterinarians() {
            try {
                const response = await api.get("/veterinarians");
                setVets(response.data);
            } catch (error) {
                console.error(error);
            }
        }

        fetchVeterinarians();
    }, []);

    return (
        <div className="p-8">
            <h1 className="text-3xl mb-4">Veterinários</h1>

            {vets.map((vet) => (
                <div
                    key={vet.id}
                    className="bg-white p-4 rounded shadow mb-3"
                >
                    <h2>{vet.nome}</h2>
                    <p>CRMV: {vet.crmv}</p>
                </div>
            ))}
        </div>
    );
}