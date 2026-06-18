import { useEffect, useState } from "react";
import { api } from "../services/api";

export default function Appointments() {
    const [appointments, setAppointments] = useState([]);

    useEffect(() => {
        const fetchAppointments = async () => {
            try {
                const response = await api.get("/appointments");
                setAppointments(response.data);
            } catch (error) {
                console.error(error);
            }
        };

        fetchAppointments();
    }, []);

    return (
        <div className="p-8">
            <h1 className="text-3xl mb-4">Consultas</h1>

            <table className="w-full bg-white rounded shadow">
                <thead>
                    <tr>
                        <th>Status</th>
                        <th>Serviço</th>
                        <th>Urgente</th>
                    </tr>
                </thead>

                <tbody>
                    {appointments.map((appointment) => (
                        <tr key={appointment.id}>
                            <td>{appointment.status}</td>
                            <td>{appointment.tipo_servico}</td>
                            <td>{appointment.urgente ? "Sim" : "Não"}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}