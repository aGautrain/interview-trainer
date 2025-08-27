# Interview Trainer Frontend

A modern React application for AI-powered interview preparation, built with TypeScript, Vite, and Tailwind CSS.

## Features

- **Job Analysis**: Analyze job postings to extract required skills and get preparation recommendations
- **Question Generator**: Generate personalized interview questions based on skills and preferences
- **Exercise Generator**: Create coding challenges and exercises in various programming languages
- **History Tracking**: View and manage your generation history
- **Responsive Design**: Modern, mobile-first UI built with Tailwind CSS
- **Mock API**: Development-friendly mock API for testing without backend

## Tech Stack

- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **UI Components**: Headless UI + Heroicons
- **Forms**: React Hook Form
- **Routing**: React Router DOM
- **Testing**: Vitest + React Testing Library
- **HTTP Client**: Axios

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. Install dependencies:

```bash
npm install
```

2. Start development server:

```bash
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run test` - Run tests
- `npm run test:ui` - Run tests with UI
- `npm run test:coverage` - Run tests with coverage report

## Project Structure

```
src/
├── components/          # Reusable UI components
│   └── Layout.tsx     # Main layout with navigation
├── pages/              # Page components
│   ├── LandingPage.tsx # Welcome and configuration
│   ├── JobAnalyzer.tsx # Job analysis interface
│   ├── QuestionGenerator.tsx # Question generation
│   ├── ExerciseGenerator.tsx # Exercise generation
│   └── History.tsx    # Generation history
├── services/           # API and business logic
│   └── mockApi.ts     # Mock API service
├── types/              # TypeScript type definitions
│   └── index.ts       # Core types
├── utils/              # Utility functions
├── test/               # Test configuration
│   └── setup.ts       # Test setup
├── App.tsx             # Main app component
├── main.tsx            # App entry point
└── index.css           # Global styles
```

## Key Components

### LandingPage

Multi-step configuration wizard for:

- LLM API setup (OpenAI, etc.)
- User preferences (languages, question types, difficulty)
- Getting started guidance

### JobAnalyzer

- Job description input form
- AI-powered skill extraction
- Requirements analysis
- Preparation recommendations

### QuestionGenerator

- Skill-based question filtering
- Multiple question types (technical, behavioral, etc.)
- Difficulty levels
- Sample answers and tips

### ExerciseGenerator

- Programming language selection
- Skill-based exercise filtering
- Test cases and solutions
- Hints and requirements

### Layout

- Responsive navigation
- Breadcrumb navigation
- Mobile-friendly design

## Mock API

The frontend includes a comprehensive mock API service (`src/services/mockApi.ts`) that simulates:

- Job analysis with realistic skill extraction
- Question generation with sample content
- Exercise generation with test cases
- History tracking
- Realistic API delays and error simulation

This allows development and testing without requiring a backend or API keys.

## Styling

The application uses Tailwind CSS with:

- Custom color palette (primary, secondary)
- Responsive design utilities
- Custom animations and transitions
- Component-based utility classes
- Dark/light theme support (planned)

## Testing

Tests are configured with Vitest and React Testing Library:

- Component testing
- User interaction testing
- Mock API testing
- Accessibility testing

## Development

### Code Style

- TypeScript strict mode enabled
- ESLint configuration
- Prettier formatting
- Conventional commit messages

### State Management

- React hooks for local state
- Context API for global state (planned)
- Local storage for user preferences

### Error Handling

- Comprehensive error boundaries
- User-friendly error messages
- Fallback UI components

## Deployment

### Build

```bash
npm run build
```

The build output is in the `dist/` directory.

### Environment Variables

Create a `.env` file for environment-specific configuration:

```env
VITE_API_URL=http://localhost:5000
VITE_APP_TITLE=Interview Trainer
```

## Contributing

1. Follow the existing code style
2. Add tests for new features
3. Update documentation
4. Use conventional commits

## License

MIT License - see LICENSE file for details.

## Roadmap

- [ ] Dark/light theme toggle
- [ ] Export functionality (PDF, Markdown)
- [ ] Offline support with PWA
- [ ] Real-time collaboration
- [ ] Advanced analytics and insights
- [ ] Integration with real LLM APIs
- [ ] User authentication and profiles
- [ ] Community question sharing
