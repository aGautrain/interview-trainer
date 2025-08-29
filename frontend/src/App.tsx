import { Routes, Route } from "react-router-dom";

import HomePage from "./pages/HomePage";
import JobTargeting from "./pages/JobTargeting";
import JobTraining from "./pages/JobTraining";
import SkillTraining from "./pages/SkillTraining";
import DebugButton from "./components/DebugButton";

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/job-targeting" element={<JobTargeting />} />
        <Route path="/job-training" element={<JobTraining />} />
        <Route path="/skill-training" element={<SkillTraining />} />

        <Route
          path="/analyze"
          element={<div>Job Analyzer (Coming Soon)</div>}
        />
        <Route
          path="/questions"
          element={<div>Question Generator (Coming Soon)</div>}
        />
        <Route
          path="/exercises"
          element={<div>Exercise Generator (Coming Soon)</div>}
        />
        <Route path="/history" element={<div>History (Coming Soon)</div>} />
      </Routes>

      {/* Global debug button */}
      <DebugButton />
    </div>
  );
}

export default App;
