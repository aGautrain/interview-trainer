import { ComponentType } from "react";
import AnimatedNumber from "./AnimatedNumber";

interface StatCardProps {
  icon: ComponentType<{ className?: string; style?: React.CSSProperties }>;
  title: string;
  value: string | number;
  color: string;
  animateValue?: boolean;
  isPercentage?: boolean;
  formatValue?: (value: number) => string;
}

const StatCard = ({
  icon: Icon,
  title,
  value,
  color,
  animateValue = false,
  isPercentage = false,
  formatValue,
}: StatCardProps) => {
  const renderValue = () => {
    if (animateValue && typeof value === "number") {
      return (
        <AnimatedNumber
          targetValue={value}
          duration={1500}
          delay={500}
          className="text-2xl font-bold text-gray-900"
          showPercentage={isPercentage}
          formatValue={formatValue}
        />
      );
    }

    return (
      <p className="text-2xl font-bold text-gray-900">
        {formatValue
          ? formatValue(value as number)
          : typeof value === "number" && isPercentage
          ? `${value}%`
          : value}
      </p>
    );
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div className="flex items-center space-x-3">
        <div
          className="p-3 rounded-lg"
          style={{ backgroundColor: `${color}20` }}
        >
          <Icon className="w-6 h-6" style={{ color: color }} />
        </div>
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          {renderValue()}
        </div>
      </div>
    </div>
  );
};

export default StatCard;
