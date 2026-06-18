import { Outlet } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import Header from "../components/Header";

export default function MainLayout() {
    return (
        <div className="flex min-h-screen bg-slate-100">

            {/* SIDEBAR FIXA */}
            <Sidebar />

            {/* CONTEÚDO */}
            <div className="flex-1 flex flex-col">

                <Header title="VetClinic" />

                <main className="flex-1 p-6">
                    
                    {/* CONTAINER PADRÃO (ISSO ORGANIZA TUDO) */}
                    <div className="max-w-6xl mx-auto w-full">
                        <Outlet />
                    </div>

                </main>

            </div>
        </div>
    );
}