import { SkillCard as SkillCardType } from "../../types";
import SkillCard from "./SkillCard";

interface SkillsGridProps {
  skills: SkillCardType[];
  isPlaceholderMode: boolean;
  onSkillClick?: (skill: SkillCardType) => void;
}

const SkillsGrid = ({
  skills,
  isPlaceholderMode,
  onSkillClick,
}: SkillsGridProps) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {skills.map((skill) => (
        <SkillCard
          key={skill.name}
          skill={skill}
          isPlaceholderMode={isPlaceholderMode}
          onClick={() => onSkillClick?.(skill)}
        />
      ))}
    </div>
  );
};

export default SkillsGrid;
