# Dashboard Components

This directory contains reusable dashboard components extracted from the HomePage for better maintainability and reusability.

## Components

### Layout Components

- **DashboardLayout** - Main layout wrapper with header and navigation for dashboard pages

### UI Components

- **StatCard** - Displays a single statistic with icon, title, and value
- **JobCard** - Displays job information with progress bar and tech stack

### Section Components

- **WelcomeSection** - Welcome message and description
- **StatsSection** - Grid of stat cards showing dashboard metrics
- **JobTargetsSection** - Job targets management with export and add functionality
- **ChartsSection** - Container for charts and analytics
- **SkillDistributionChart** - Pie chart showing question distribution by skills
- **PerformanceChart** - Bar chart showing performance by difficulty level

## Usage

```tsx
import {
  DashboardLayout,
  WelcomeSection,
  StatsSection,
  JobTargetsSection,
  ChartsSection,
} from "../components/dashboard";

const DashboardPage = () => {
  return (
    <DashboardLayout>
      <WelcomeSection />
      <StatsSection stats={stats} />
      <JobTargetsSection jobs={jobs} />
      <ChartsSection
        skillDistributionData={skillDistributionData}
        performanceData={performanceData}
      />
    </DashboardLayout>
  );
};
```

## Types

All component types are defined in `../types/dashboard.ts` for consistency and reusability.

## Benefits

- **Reusability**: Components can be used across different dashboard pages
- **Maintainability**: Each component has a single responsibility
- **Testability**: Individual components can be tested in isolation
- **Consistency**: Centralized types ensure consistent data structures
- **Scalability**: Easy to add new dashboard features by creating new components
