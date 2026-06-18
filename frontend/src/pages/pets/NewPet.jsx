import { useState } from "react";
import { api } from "../../services/api";
import { useNavigate } from "react-router-dom";

export default function NewPet() {
    const navigate = useNavigate();

    const [form, setForm] = useState({
        name: "",
        species: ""
    });

    function handleChange(e) {
        setForm({ ...form, [e.target.name]: e.target.value });
    }

    async function handleSubmit(e) {
        e.preventDefault();

        try {
            await api.post("/pets", form);
            navigate("/pets");
        } catch (err) {
            console.error(err);
        }
    }

    return (
        <form onSubmit={handleSubmit} className="bg-white p-6 rounded shadow max-w-md">
            <h1 className="text-xl font-bold mb-4">Novo Pet</h1>

            <input
                name="name"
                placeholder="Nome"
                className="border p-2 w-full mb-2"
                onChange={handleChange}
            />

            <input
                name="species"
                placeholder="Espécie"
                className="border p-2 w-full mb-2"
                onChange={handleChange}
            />

            <button className="bg-blue-600 text-white px-4 py-2 rounded">
                Salvar
            </button>
        </form>
    );
}