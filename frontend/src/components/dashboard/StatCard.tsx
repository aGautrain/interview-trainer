import { ComponentType } from "react";

interface StatCardProps {
  icon: ComponentType<{ className?: string; style?: React.CSSProperties }>;
  title: string;
  value: string | number;
  color: string;
}

const StatCard = ({ icon: Icon, title, value, color }: StatCardProps) => (
  <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
    <div className="flex items-center space-x-3">
      <div className="p-3 rounded-lg" style={{ backgroundColor: `${color}20` }}>
        <Icon className="w-6 h-6" style={{ color: color }} />
      </div>
      <div>
        <p className="text-sm font-medium text-gray-600">{title}</p>
        <p className="text-2xl font-bold text-gray-900">{value}</p>
      </div>
    </div>
  </div>
);

export default StatCard;
