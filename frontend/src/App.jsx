import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainLayout from "./layouts/MainLayout";

import Dashboard from "./pages/Dashboard";

// Pets
import PetsList from "./pages/pets/PetsList";
import NewPet from "./pages/pets/NewPet";

// Tutors
import TutorsList from "./pages/tutors/TutorsList";
import NewTutor from "./pages/tutors/NewTutor";

// Veterinarians
import VeterinariansList from "./pages/veterinarians/VeterinariansList";
import NewVeterinarian from "./pages/veterinarians/NewVeterinarian";

export default function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<MainLayout />}>
                    
                    <Route index element={<Dashboard />} />

                    {/* Pets */}
                    <Route path="pets" element={<PetsList />} />
                    <Route path="pets/new" element={<NewPet />} />

                    {/* Tutors */}
                    <Route path="tutors" element={<TutorsList />} />
                    <Route path="tutors/new" element={<NewTutor />} />

                    {/* Veterinarians */}
                    <Route path="veterinarians" element={<VeterinariansList />} />
                    <Route path="veterinarians/new" element={<NewVeterinarian />} />

                </Route>
            </Routes>
        </BrowserRouter>
    );
}