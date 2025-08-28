import SkillDistributionChart from "./SkillDistributionChart";
import PerformanceChart from "./PerformanceChart";

import { SkillDistributionData, PerformanceData } from "../../types/dashboard";

interface ChartsSectionProps {
  skillDistributionData: SkillDistributionData[];
  performanceData: PerformanceData[];
}

const ChartsSection = ({
  skillDistributionData,
  performanceData,
}: ChartsSectionProps) => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <SkillDistributionChart data={skillDistributionData} />
      <PerformanceChart data={performanceData} />
    </div>
  );
};

export default ChartsSection;
