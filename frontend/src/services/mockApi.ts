import {
  JobPosting,
  Skill,
  Question,
  CodingExercise,
  JobAnalysisResult,
  ApiResponse,
  QuestionGenerationRequest,
  ExerciseGenerationRequest,
} from "@/types";

// Mock data for development
const mockSkills: Skill[] = [
  {
    id: "1",
    name: "JavaScript",
    category: "programming",
    proficiency: "intermediate",
  },
  {
    id: "2",
    name: "React",
    category: "framework",
    proficiency: "intermediate",
  },
  { id: "3", name: "Node.js", category: "framework", proficiency: "beginner" },
  { id: "4", name: "Python", category: "programming", proficiency: "advanced" },
  {
    id: "5",
    name: "PostgreSQL",
    category: "database",
    proficiency: "intermediate",
  },
  { id: "6", name: "AWS", category: "cloud", proficiency: "beginner" },
  { id: "7", name: "Docker", category: "tool", proficiency: "intermediate" },
  {
    id: "8",
    name: "System Design",
    category: "soft-skill",
    proficiency: "beginner",
  },
];

const mockQuestions: Question[] = [
  {
    id: "1",
    text: "Explain the difference between var, let, and const in JavaScript.",
    type: "technical",
    difficulty: "beginner",
    category: "JavaScript Fundamentals",
    skills: [mockSkills[0]],
    sampleAnswer:
      "var is function-scoped and can be redeclared, let is block-scoped and can be reassigned, const is block-scoped and cannot be reassigned.",
    tips: [
      "Focus on scope differences",
      "Mention hoisting behavior",
      "Explain practical use cases",
    ],
    createdAt: new Date().toISOString(),
  },
  {
    id: "2",
    text: "How would you handle state management in a large React application?",
    type: "technical",
    difficulty: "intermediate",
    category: "React Architecture",
    skills: [mockSkills[1]],
    sampleAnswer:
      "For large applications, I would use Redux Toolkit or Zustand for global state, React Query for server state, and local state for component-specific data.",
    tips: [
      "Consider performance implications",
      "Discuss different state management patterns",
      "Mention when to use each approach",
    ],
    createdAt: new Date().toISOString(),
  },
];

const mockExercises: CodingExercise[] = [
  {
    id: "1",
    title: "Implement a Stack Data Structure",
    description:
      "Create a Stack class with push, pop, peek, and isEmpty methods. Include proper error handling.",
    difficulty: "beginner",
    programmingLanguage: "JavaScript",
    skills: [mockSkills[0]],
    requirements: [
      "Implement push method",
      "Implement pop method",
      "Implement peek method",
      "Implement isEmpty method",
      "Add error handling",
    ],
    testCases: [
      {
        input: "stack.push(1); stack.push(2); stack.pop()",
        expectedOutput: "2",
        description: "Basic push and pop operations",
      },
      {
        input: "stack.isEmpty()",
        expectedOutput: "true",
        description: "Check if stack is empty",
      },
    ],
    solution: `class Stack {
  constructor() {
    this.items = [];
  }
  
  push(element) {
    this.items.push(element);
  }
  
  pop() {
    if (this.isEmpty()) {
      throw new Error('Stack is empty');
    }
    return this.items.pop();
  }
  
  peek() {
    if (this.isEmpty()) {
      throw new Error('Stack is empty');
    }
    return this.items[this.items.length - 1];
  }
  
  isEmpty() {
    return this.items.length === 0;
  }
}`,
    hints: [
      "Think about using an array as the underlying data structure",
      "Consider what happens when trying to pop from an empty stack",
    ],
    timeLimit: 15,
    createdAt: new Date().toISOString(),
  },
];

// Simulate API delay
const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

export class MockApiService {
  // Job Analysis
  async analyzeJob(
    _jobData: Partial<JobPosting>
  ): Promise<ApiResponse<JobAnalysisResult>> {
    await delay(1500); // Simulate processing time

    // Use jobData if available, otherwise use defaults
    const extractedSkills = mockSkills.slice(0, 4); // Random selection
    const requirements = [
      "Strong understanding of modern JavaScript",
      "Experience with React ecosystem",
      "Knowledge of backend development",
      "Familiarity with databases",
    ];

    return {
      success: true,
      data: {
        skills: extractedSkills,
        requirements,
        summary:
          "This role requires a full-stack developer with strong JavaScript skills and experience in modern web development frameworks.",
        difficulty: "intermediate",
        estimatedExperience: "2-4 years",
        recommendations: [
          "Focus on JavaScript fundamentals",
          "Practice React component design",
          "Learn basic backend concepts",
          "Understand database relationships",
        ],
      },
    };
  }

  // Question Generation
  async generateQuestions(
    request: QuestionGenerationRequest
  ): Promise<ApiResponse<Question[]>> {
    await delay(2000);

    const filteredQuestions = mockQuestions.filter(
      (q) =>
        request.skills.some((skill) =>
          q.skills.some((qSkill) => qSkill.name === skill.name)
        ) &&
        q.difficulty === request.difficulty &&
        q.type === request.type
    );

    return {
      success: true,
      data: filteredQuestions.slice(0, request.count),
    };
  }

  // Exercise Generation
  async generateExercises(
    request: ExerciseGenerationRequest
  ): Promise<ApiResponse<CodingExercise[]>> {
    await delay(2500);

    const filteredExercises = mockExercises.filter(
      (e) =>
        request.skills.some((skill) =>
          e.skills.some((eSkill) => eSkill.name === skill.name)
        ) &&
        e.difficulty === request.difficulty &&
        e.programmingLanguage === request.language
    );

    return {
      success: true,
      data: filteredExercises.slice(0, request.count),
    };
  }

  // Get Skills
  async getSkills(): Promise<ApiResponse<Skill[]>> {
    await delay(500);
    return {
      success: true,
      data: mockSkills,
    };
  }

  // Get History
  async getHistory(): Promise<ApiResponse<any[]>> {
    await delay(800);
    return {
      success: true,
      data: [
        {
          id: "1",
          type: "job-analysis",
          input: { title: "Frontend Developer", company: "Tech Corp" },
          output: { skills: 4, requirements: 4 },
          model: "gpt-4",
          tokensUsed: 1500,
          duration: 2.3,
          createdAt: new Date(Date.now() - 86400000).toISOString(), // 1 day ago
        },
        {
          id: "2",
          type: "question-generation",
          input: { skills: ["JavaScript", "React"], count: 3 },
          output: { questions: 3 },
          model: "gpt-4",
          tokensUsed: 800,
          duration: 1.8,
          createdAt: new Date(Date.now() - 172800000).toISOString(), // 2 days ago
        },
      ],
    };
  }

  // Simulate errors
  async simulateError(): Promise<ApiResponse<any>> {
    await delay(1000);
    return {
      success: false,
      error: "Simulated API error for testing",
      message: "This is a test error to demonstrate error handling",
    };
  }
}

export const mockApi = new MockApiService();
