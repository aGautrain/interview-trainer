"""
Sample data for the Interview Trainer backend.
This data is extracted from the frontend mocked data and converted to match our Pydantic schemas.
"""

from datetime import datetime, timezone
from schemas import (
    DashboardStats,
    Job,
    SkillDistributionData,
    PerformanceData,
    SkillType,
    SkillCard,
    Question,
    Exercise,
    Skill,
    UserPreferences,
    LLMConfig
)

# Sample dashboard data
SAMPLE_DASHBOARD_STATS = DashboardStats(
    activeJobs=2,
    questionsCompleted=1,
    avgProgress=53,
    successRate=78
)

SAMPLE_JOBS = [
    Job(
        id="1",
        title="Senior Frontend Developer",
        company="TechCorp",
        description="We are looking for a Senior Frontend Developer to join our team and help build amazing user experiences.",
        requirements=["5+ years of frontend development experience", "Strong knowledge of React and TypeScript", "Experience with modern frontend tooling"],
        skills=["React", "TypeScript", "JavaScript", "CSS", "HTML"],
        techStack=["React", "TypeScript"],
        location="Remote Friendly",
        type="Full-time",
        level="Senior",
        salaryRange="$90k - $120k",
        progress=65,
        isRemote=True,
        createdAt="2024-01-15T00:00:00Z",
        updatedAt="2024-01-15T00:00:00Z"
    ),
    Job(
        id="2",
        title="Full Stack Engineer",
        company="StartupXYZ",
        description="Join our fast-growing startup as a Full Stack Engineer and help us build the next big thing.",
        requirements=["3+ years of full stack development", "Experience with Python and Django", "Knowledge of modern web technologies"],
        skills=["Python", "Django", "JavaScript", "SQL", "AWS"],
        techStack=["Python", "Django"],
        location="Fully Remote",
        type="Full-time",
        level="Mid-level",
        salaryRange="$80k - $110k",
        progress=40,
        isRemote=True,
        createdAt="2024-01-10T00:00:00Z",
        updatedAt="2024-01-10T00:00:00Z"
    )
]

SAMPLE_SKILL_DISTRIBUTION_DATA = [
    SkillDistributionData(name="Frontend", value=35, color="#f97316"),
    SkillDistributionData(name="Backend", value=25, color="#14b8a6"),
    SkillDistributionData(name="Full Stack", value=20, color="#1e40af"),
    SkillDistributionData(name="DevOps", value=12, color="#eab308"),
    SkillDistributionData(name="Data Science", value=8, color="#06b6d4")
]

SAMPLE_PERFORMANCE_DATA = [
    PerformanceData(difficulty="beginner", success=12, failure=3),
    PerformanceData(difficulty="intermediate", success=6, failure=4),
    PerformanceData(difficulty="advanced", success=2, failure=4)
]

# Sample skills data
SAMPLE_SKILLS = [
    SkillCard(
        name="JavaScript",
        type=SkillType.PROGRAMMING,
        questionsCompleted=7,
        questionsTotal=12,
        exercisesCompleted=4,
        exercisesTotal=8
    ),
    SkillCard(
        name="System Design",
        type=SkillType.SYSTEM_DESIGN,
        questionsCompleted=4,
        questionsTotal=10,
        exercisesCompleted=0,
        exercisesTotal=0
    ),
    SkillCard(
        name="Team Leadership",
        type=SkillType.SOFT_SKILL,
        questionsCompleted=5,
        questionsTotal=9,
        exercisesCompleted=0,
        exercisesTotal=0
    ),
    SkillCard(
        name="React",
        type=SkillType.FRAMEWORK,
        questionsCompleted=9,
        questionsTotal=15,
        exercisesCompleted=6,
        exercisesTotal=10
    ),
    SkillCard(
        name="Communication",
        type=SkillType.SOFT_SKILL,
        questionsCompleted=8,
        questionsTotal=14,
        exercisesCompleted=0,
        exercisesTotal=0
    ),
    SkillCard(
        name="Node.js",
        type=SkillType.FRAMEWORK,
        questionsCompleted=6,
        questionsTotal=11,
        exercisesCompleted=3,
        exercisesTotal=9
    ),
    SkillCard(
        name="TypeScript",
        type=SkillType.PROGRAMMING,
        questionsCompleted=3,
        questionsTotal=8,
        exercisesCompleted=2,
        exercisesTotal=5
    ),
    SkillCard(
        name="Problem Solving",
        type=SkillType.ALGORITHMS,
        questionsCompleted=10,
        questionsTotal=16,
        exercisesCompleted=7,
        exercisesTotal=12
    ),
    SkillCard(
        name="API Design",
        type=SkillType.ARCHITECTURE,
        questionsCompleted=2,
        questionsTotal=7,
        exercisesCompleted=1,
        exercisesTotal=4
    )
]

# Sample questions for different skills
SAMPLE_QUESTIONS = {
    "JavaScript": [
        Question(
            id="js-1",
            text="Explain the difference between let, const, and var in JavaScript.",
            type="theoretical",
            difficulty="beginner",
            category="JavaScript",
            skills=[],
            isCompleted=False,
            createdAt="2024-01-15T00:00:00Z"
        ),
        Question(
            id="js-2",
            text="What are closures in JavaScript and how do they work?",
            type="theoretical",
            difficulty="intermediate",
            category="JavaScript",
            skills=[],
            isCompleted=False,
            createdAt="2024-01-15T00:00:00Z"
        ),
        Question(
            id="js-3",
            text="Explain the event loop in JavaScript and how it handles asynchronous operations.",
            type="theoretical",
            difficulty="advanced",
            category="JavaScript",
            skills=[],
            isCompleted=False,
            createdAt="2024-01-15T00:00:00Z"
        )
    ],
    "React": [
        Question(
            id="react-1",
            text="What is the difference between state and props in React?",
            type="theoretical",
            difficulty="beginner",
            category="React",
            skills=[],
            isCompleted=False,
            createdAt="2024-01-15T00:00:00Z"
        ),
        Question(
            id="react-2",
            text="Explain the React component lifecycle methods.",
            type="theoretical",
            difficulty="intermediate",
            category="React",
            skills=[],
            isCompleted=False,
            createdAt="2024-01-15T00:00:00Z"
        ),
        Question(
            id="react-3",
            text="What are React hooks and how do they work?",
            type="theoretical",
            difficulty="intermediate",
            category="React",
            skills=[],
            isCompleted=False,
            createdAt="2024-01-15T00:00:00Z"
        )
    ],
    "System Design": [
        Question(
            id="sd-1",
            text="What are the key considerations when designing a scalable system?",
            type="theoretical",
            difficulty="intermediate",
            category="System Design",
            skills=[],
            isCompleted=False,
            createdAt="2024-01-15T00:00:00Z"
        ),
        Question(
            id="sd-2",
            text="Explain the CAP theorem and its implications for distributed systems.",
            type="theoretical",
            difficulty="advanced",
            category="System Design",
            skills=[],
            isCompleted=False,
            createdAt="2024-01-15T00:00Z"
        )
    ]
}

# Sample exercises for different skills
SAMPLE_EXERCISES = {
    "JavaScript": [
        Exercise(
            id="js-ex-1",
            title="Implement a debounce function",
            description="Create a debounce function that delays the execution of a function until after a specified delay has elapsed since the last time it was invoked.",
            difficulty="intermediate",
            category="JavaScript",
            skills=[],
            isCompleted=False,
            createdAt="2024-01-15T00:00:00Z"
        ),
        Exercise(
            id="js-ex-2",
            title="Array flattening",
            description="Write a function that flattens a nested array to a single level.",
            difficulty="beginner",
            category="JavaScript",
            skills=[],
            isCompleted=False,
            createdAt="2024-01-15T00:00:00Z"
        ),
        Exercise(
            id="js-ex-3",
            title="Promise.all implementation",
            description="Implement your own version of Promise.all that handles an array of promises.",
            difficulty="advanced",
            category="JavaScript",
            skills=[],
            isCompleted=False,
            createdAt="2024-01-15T00:00:00Z"
        )
    ],
    "React": [
        Exercise(
            id="react-ex-1",
            title="Custom hook for form handling",
            description="Create a custom React hook that manages form state and validation.",
            difficulty="intermediate",
            category="React",
            skills=[],
            isCompleted=False,
            createdAt="2024-01-15T00:00:00Z"
        ),
        Exercise(
            id="react-ex-2",
            title="Context API implementation",
            description="Implement a theme switcher using React Context API.",
            difficulty="beginner",
            category="React",
            skills=[],
            isCompleted=False,
            createdAt="2024-01-15T00:00:00Z"
        )
    ],
    "Problem Solving": [
        Exercise(
            id="ps-ex-1",
            title="Two Sum",
            description="Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
            difficulty="beginner",
            category="Algorithms",
            skills=[],
            isCompleted=False,
            createdAt="2024-01-15T00:00:00Z"
        ),
        Exercise(
            id="ps-ex-2",
            title="Valid Parentheses",
            description="Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.",
            difficulty="intermediate",
            category="Algorithms",
            skills=[],
            isCompleted=False,
            createdAt="2024-01-15T00:00:00Z"
        )
    ]
}

# Sample user preferences
SAMPLE_USER_PREFERENCES = UserPreferences(
    defaultDifficulty="intermediate",
    preferredLanguages=["JavaScript", "Python", "TypeScript"],
    questionTypes=["technical", "behavioral", "coding"],
    theme="auto"
)

# Sample LLM configuration
SAMPLE_LLM_CONFIG = LLMConfig(
    apiKey="sample-api-key",
    model="gpt-4",
    temperature=0.7,
    maxTokens=2000
)

def get_sample_questions(skill_name: str) -> list[Question]:
    """Get sample questions for a specific skill"""
    return SAMPLE_QUESTIONS.get(skill_name, [
        Question(
            id="default-1",
            text="What are the key concepts in this skill area?",
            type="theoretical",
            difficulty="intermediate",
            category=skill_name,
            skills=[],
            isCompleted=False,
            createdAt="2024-01-15T00:00:00Z"
        )
    ])

def get_sample_exercises(skill_name: str) -> list[Exercise]:
    """Get sample exercises for a specific skill"""
    return SAMPLE_EXERCISES.get(skill_name, [])
