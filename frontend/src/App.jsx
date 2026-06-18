import { BrowserRouter, Routes, Route } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Tutors from "./pages/Tutors";
import Pets from "./pages/Pets";
import Veterinarians from "./pages/Veterinarians";
import Appointments from "./pages/Appointments";

export default function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/tutors" element={<Tutors />} />
                <Route path="/pets" element={<Pets />} />
                <Route path="/veterinarians" element={<Veterinarians />} />
                <Route path="/appointments" element={<Appointments />} />
            </Routes>
        </BrowserRouter>
    );
}