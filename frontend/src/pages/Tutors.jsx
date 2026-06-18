import { useEffect, useState } from "react";
import { api } from "../services/api";

export default function Tutors() {
    const [tutors, setTutors] = useState([]);

    useEffect(() => {
        const fetchTutors = async () => {
            try {
                const response = await api.get("/tutors");
                setTutors(response.data);
            } catch (error) {
                console.error(error);
            }
        };

        fetchTutors();
    }, []);

    return (
        <div className="p-8">
            <h1 className="text-3xl mb-4">Tutores</h1>

            <table className="w-full bg-white shadow rounded">
                <thead>
                    <tr>
                        <th className="p-3">Nome</th>
                        <th>Email</th>
                        <th>CPF</th>
                    </tr>
                </thead>

                <tbody>
                    {tutors.map((tutor) => (
                        <tr key={tutor.id}>
                            <td className="p-3">{tutor.nome}</td>
                            <td>{tutor.email}</td>
                            <td>{tutor.cpf}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}