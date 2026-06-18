import { useState } from "react";
import { api } from "../../services/api";
import { useNavigate } from "react-router-dom";

export default function NewTutor() {
    const navigate = useNavigate();

    const [form, setForm] = useState({
        name: "",
        email: ""
    });

    function handleChange(e) {
        setForm({ ...form, [e.target.name]: e.target.value });
    }

    async function handleSubmit(e) {
        e.preventDefault();
        await api.post("/tutors", form);
        navigate("/tutors");
    }

    return (
        <form className="bg-white p-6 rounded shadow max-w-md" onSubmit={handleSubmit}>
            <h1 className="text-xl font-bold mb-4">Novo Tutor</h1>

            <input
                name="name"
                placeholder="Nome"
                className="border p-2 w-full mb-2"
                onChange={handleChange}
            />

            <input
                name="email"
                placeholder="Email"
                className="border p-2 w-full mb-2"
                onChange={handleChange}
            />

            <button className="bg-blue-600 text-white px-4 py-2 rounded">
                Salvar
            </button>
        </form>
    );
}