import { Job } from "../../types/dashboard";
import { SkillCard, SkillType } from "../../types/job-training";

// Placeholder job for when none is selected
export const placeholderJob: Job = {
  id: "placeholder",
  title: "Select a Job to Train For",
  company: "Choose from your job targets",
  salaryRange: "Not specified",
  location: "Not specified",
  techStack: ["Select a job first"],
  progress: 0,
  isRemote: false,
};

// Sample skills data
export const sampleSkills: SkillCard[] = [
  {
    name: "JavaScript",
    type: SkillType.PROGRAMMING,
    questionsCompleted: 7,
    questionsTotal: 12,
    exercisesCompleted: 4,
    exercisesTotal: 8,
  },
  {
    name: "System Design",
    type: SkillType.SYSTEM_DESIGN,
    questionsCompleted: 4,
    questionsTotal: 10,
    exercisesCompleted: 0,
    exercisesTotal: 0,
  },
  {
    name: "Team Leadership",
    type: SkillType.SOFT_SKILL,
    questionsCompleted: 5,
    questionsTotal: 9,
    exercisesCompleted: 0,
    exercisesTotal: 0,
  },
  {
    name: "React",
    type: SkillType.FRAMEWORK,
    questionsCompleted: 9,
    questionsTotal: 15,
    exercisesCompleted: 6,
    exercisesTotal: 10,
  },
  {
    name: "Communication",
    type: SkillType.SOFT_SKILL,
    questionsCompleted: 8,
    questionsTotal: 14,
    exercisesCompleted: 0,
    exercisesTotal: 0,
  },
  {
    name: "Node.js",
    type: SkillType.FRAMEWORK,
    questionsCompleted: 6,
    questionsTotal: 11,
    exercisesCompleted: 3,
    exercisesTotal: 9,
  },
  {
    name: "TypeScript",
    type: SkillType.PROGRAMMING,
    questionsCompleted: 3,
    questionsTotal: 8,
    exercisesCompleted: 2,
    exercisesTotal: 5,
  },
  {
    name: "Problem Solving",
    type: SkillType.ALGORITHMS,
    questionsCompleted: 10,
    questionsTotal: 16,
    exercisesCompleted: 7,
    exercisesTotal: 12,
  },
  {
    name: "API Design",
    type: SkillType.ARCHITECTURE,
    questionsCompleted: 2,
    questionsTotal: 7,
    exercisesCompleted: 1,
    exercisesTotal: 4,
  },
];
