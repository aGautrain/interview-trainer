import { Routes, Route } from "react-router-dom";
import { useState } from "react";
import LandingPage from "./pages/LandingPage";
import JobAnalyzer from "./pages/JobAnalyzer";
import QuestionGenerator from "./pages/QuestionGenerator";
import ExerciseGenerator from "./pages/ExerciseGenerator";
import History from "./pages/History";
import { UserPreferences } from "./types";

function App() {
  const [preferences, setPreferences] = useState<UserPreferences>({
    defaultDifficulty: "intermediate",
    preferredLanguages: ["JavaScript", "Python"],
    questionTypes: ["technical", "behavioral"],
    theme: "light",
  });

  const [isConfigured, setIsConfigured] = useState(false);

  const handlePreferencesUpdate = (
    newPreferences: Partial<UserPreferences>
  ) => {
    setPreferences((prev) => ({ ...prev, ...newPreferences }));
  };

  const handleConfigurationComplete = () => {
    setIsConfigured(true);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Routes>
        <Route
          path="/"
          element={
            <LandingPage
              preferences={preferences}
              onPreferencesUpdate={handlePreferencesUpdate}
              onConfigurationComplete={handleConfigurationComplete}
            />
          }
        />
        {isConfigured && (
          <>
            <Route path="/analyze" element={<JobAnalyzer />} />
            <Route path="/questions" element={<QuestionGenerator />} />
            <Route path="/exercises" element={<ExerciseGenerator />} />
            <Route path="/history" element={<History />} />
          </>
        )}
      </Routes>
    </div>
  );
}

export default App;
