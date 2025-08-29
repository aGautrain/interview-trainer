import { Job } from "../../types/dashboard";
import {
  SkillCard,
  SkillType,
  Question,
  Exercise,
} from "../../types/job-training";

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

// Sample questions and exercises for different skill types
export const getSampleQuestions = (skillName: string): Question[] => {
  const questionsMap: Record<string, Question[]> = {
    JavaScript: [
      {
        id: "js-1",
        text: "Explain the difference between let, const, and var in JavaScript.",
        type: "theoretical",
        difficulty: "easy",
        category: "JavaScript",
        isCompleted: false,
      },
      {
        id: "js-2",
        text: "What are closures in JavaScript and how do they work?",
        type: "theoretical",
        difficulty: "medium",
        category: "JavaScript",
        isCompleted: false,
      },
      {
        id: "js-3",
        text: "Explain the event loop in JavaScript and how it handles asynchronous operations.",
        type: "theoretical",
        difficulty: "hard",
        category: "JavaScript",
        isCompleted: false,
      },
    ],
    React: [
      {
        id: "react-1",
        text: "What is the difference between state and props in React?",
        type: "theoretical",
        difficulty: "easy",
        category: "React",
        isCompleted: false,
      },
      {
        id: "react-2",
        text: "Explain the React component lifecycle methods.",
        type: "theoretical",
        difficulty: "medium",
        category: "React",
        isCompleted: false,
      },
      {
        id: "react-3",
        text: "What are React hooks and how do they work?",
        type: "theoretical",
        difficulty: "medium",
        category: "React",
        isCompleted: false,
      },
    ],
    "System Design": [
      {
        id: "sd-1",
        text: "What are the key considerations when designing a scalable system?",
        type: "theoretical",
        difficulty: "medium",
        category: "System Design",
        isCompleted: false,
      },
      {
        id: "sd-2",
        text: "Explain the CAP theorem and its implications for distributed systems.",
        type: "theoretical",
        difficulty: "hard",
        category: "System Design",
        isCompleted: false,
      },
    ],
    "Team Leadership": [
      {
        id: "tl-1",
        text: "How do you handle conflicts within a development team?",
        type: "theoretical",
        difficulty: "medium",
        category: "Team Leadership",
        isCompleted: false,
      },
      {
        id: "tl-2",
        text: "What strategies do you use to motivate team members?",
        type: "theoretical",
        difficulty: "medium",
        category: "Team Leadership",
        isCompleted: false,
      },
    ],
  };

  return (
    questionsMap[skillName] || [
      {
        id: "default-1",
        text: "What are the key concepts in this skill area?",
        type: "theoretical",
        difficulty: "medium",
        category: skillName,
        isCompleted: false,
      },
    ]
  );
};

export const getSampleExercises = (skillName: string): Exercise[] => {
  const exercisesMap: Record<string, Exercise[]> = {
    JavaScript: [
      {
        id: "js-ex-1",
        title: "Implement a debounce function",
        description:
          "Create a debounce function that delays the execution of a function until after a specified delay has elapsed since the last time it was invoked.",
        difficulty: "medium",
        category: "JavaScript",
        isCompleted: false,
      },
      {
        id: "js-ex-2",
        title: "Array flattening",
        description:
          "Write a function that flattens a nested array to a single level.",
        difficulty: "easy",
        category: "JavaScript",
        isCompleted: false,
      },
      {
        id: "js-ex-3",
        title: "Promise.all implementation",
        description:
          "Implement your own version of Promise.all that handles an array of promises.",
        difficulty: "hard",
        category: "JavaScript",
        isCompleted: false,
      },
    ],
    React: [
      {
        id: "react-ex-1",
        title: "Custom hook for form handling",
        description:
          "Create a custom React hook that manages form state and validation.",
        difficulty: "medium",
        category: "React",
        isCompleted: false,
      },
      {
        id: "react-ex-2",
        title: "Context API implementation",
        description: "Implement a theme switcher using React Context API.",
        difficulty: "easy",
        category: "React",
        isCompleted: false,
      },
    ],
    "Problem Solving": [
      {
        id: "ps-ex-1",
        title: "Two Sum",
        description:
          "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
        difficulty: "easy",
        category: "Algorithms",
        isCompleted: false,
      },
      {
        id: "ps-ex-2",
        title: "Valid Parentheses",
        description:
          "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.",
        difficulty: "medium",
        category: "Algorithms",
        isCompleted: false,
      },
    ],
  };

  return exercisesMap[skillName] || [];
};
