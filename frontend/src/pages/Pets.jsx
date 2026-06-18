import { useEffect, useState } from "react";
import { api } from "../services/api";

export default function Pets() {
    const [pets, setPets] = useState([]);

    useEffect(() => {
        const fetchPets = async () => {
            try {
                const response = await api.get("/pets");
                setPets(response.data);
            } catch (error) {
                console.error(error);
            }
        };

        fetchPets();
    }, []);

    return (
        <div className="p-8">
            <h1 className="text-3xl mb-4">Animais</h1>

            <div className="grid gap-4">
                {pets.map((pet) => (
                    <div
                        key={pet.id}
                        className="bg-white p-4 rounded shadow"
                    >
                        <h2 className="font-bold">{pet.nome}</h2>
                        <p>{pet.especie}</p>
                        <p>{pet.raca}</p>
                    </div>
                ))}
            </div>
        </div>
    );
}