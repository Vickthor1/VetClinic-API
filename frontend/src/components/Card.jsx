export default function Card({ title, description, children }) {
    return (
        <div className="bg-white border rounded-xl p-4 shadow-sm hover:shadow-md transition">
            
            {title && (
                <h3 className="font-semibold text-slate-800 mb-1">
                    {title}
                </h3>
            )}

            {description && (
                <p className="text-sm text-slate-500 mb-3">
                    {description}
                </p>
            )}

            {children}

        </div>
    );
}