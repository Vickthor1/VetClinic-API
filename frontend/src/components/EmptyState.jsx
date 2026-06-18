export default function EmptyState({ title, description }) {
    return (
        <div className="text-center py-10 text-slate-500">
            <p className="font-semibold text-lg">{title}</p>
            <p className="text-sm">{description}</p>
        </div>
    );
}