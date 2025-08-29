import { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import DashboardLayout from "../components/layouts/DashboardLayout";
import { ProgressSection } from "../components/dashboard";
import {
  JobTrainingHeader,
  JobCard,
  SkillsGrid,
  PlaceholderOverlay,
  placeholderJob,
} from "../components/job-training";
import { SkillCard as SkillCardType } from "../types";
import { Job } from "../types/dashboard";
import { skillsService } from "../services";

const JobTraining = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(true);
  const [selectedJob, setSelectedJob] = useState<Job>(placeholderJob);
  const [isPlaceholderMode, setIsPlaceholderMode] = useState(true);
  const [skills, setSkills] = useState<SkillCardType[]>([]);
  const [skillsLoading, setSkillsLoading] = useState(true);
  const [skillsError, setSkillsError] = useState<string | null>(null);

  useEffect(() => {
    const jobFromState = location.state?.selectedJob;
    const fromSkillTraining = location.state?.fromSkillTraining;

    if (jobFromState) {
      setSelectedJob(jobFromState);
      setIsPlaceholderMode(false);
    } else if (fromSkillTraining) {
      // Coming from skill training but no job state - this shouldn't happen
      // but we'll handle it gracefully by going to dashboard
      navigate("/");
      return;
    } else {
      setSelectedJob(placeholderJob);
      setIsPlaceholderMode(true);
    }
    setIsLoading(false);
  }, [location.state, navigate]);

  useEffect(() => {
    const fetchSkills = async () => {
      try {
        setSkillsLoading(true);
        setSkillsError(null);
        const skillsData = await skillsService.getSkills();
        setSkills(skillsData);
      } catch (err) {
        console.error("Failed to fetch skills:", err);
        setSkillsError("Failed to load skills. Please try again later.");
      } finally {
        setSkillsLoading(false);
      }
    };

    fetchSkills();
  }, []);

  const handleSelectJob = () => {
    navigate("/");
  };

  const handleCreateJob = () => {
    navigate("/job-targeting");
  };

  const handleSkillClick = async (skill: SkillCardType) => {
    try {
      // Fetch real questions and exercises for the skill
      const [questions, exercises] = await Promise.all([
        skillsService.getSkillQuestions(skill.name),
        skillsService.getSkillExercises(skill.name),
      ]);

      navigate("/skill-training", {
        state: {
          skillData: {
            skill,
            questions,
            exercises,
          },
          selectedJob: selectedJob, // Pass the current job state
        },
      });
    } catch (err) {
      console.error("Failed to fetch skill data:", err);
      // You could show a toast notification here
      alert("Failed to load skill data. Please try again.");
    }
  };

  if (skillsLoading) {
    return (
      <DashboardLayout>
        <JobTrainingHeader onBackClick={() => navigate("/")} />
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading skills...</p>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  if (skillsError) {
    return (
      <DashboardLayout>
        <JobTrainingHeader onBackClick={() => navigate("/")} />
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <div className="text-red-500 text-6xl mb-4">⚠️</div>
            <h2 className="text-xl font-semibold text-gray-900 mb-2">
              Failed to load skills
            </h2>
            <p className="text-gray-600 mb-4">{skillsError}</p>
            <button
              onClick={() => window.location.reload()}
              className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
            >
              Try Again
            </button>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <JobTrainingHeader onBackClick={() => navigate("/")} />

      <JobCard
        job={selectedJob}
        isPlaceholderMode={isPlaceholderMode}
        onSelectJob={handleSelectJob}
        onCreateJob={handleCreateJob}
      />

      <SkillsGrid
        skills={skills}
        isPlaceholderMode={isPlaceholderMode}
        onSkillClick={handleSkillClick}
      />

      <ProgressSection
        questionsCompleted={skills.reduce(
          (sum, skill) => sum + skill.questionsCompleted,
          0
        )}
        questionsTotal={skills.reduce(
          (sum, skill) => sum + skill.questionsTotal,
          0
        )}
        exercisesCompleted={skills.reduce(
          (sum, skill) => sum + skill.exercisesCompleted,
          0
        )}
        exercisesTotal={skills.reduce(
          (sum, skill) => sum + skill.exercisesTotal,
          0
        )}
        skillsCompleted={
          skills.filter((skill) => {
            const questionsProgress =
              skill.questionsTotal > 0
                ? (skill.questionsCompleted / skill.questionsTotal) * 100
                : 0;
            const exercisesProgress =
              skill.exercisesTotal > 0
                ? (skill.exercisesCompleted / skill.exercisesTotal) * 100
                : 0;
            return (
              questionsProgress === 100 &&
              (skill.exercisesTotal === 0 || exercisesProgress === 100)
            );
          }).length
        }
        skillsTotal={skills.length}
      />

      <PlaceholderOverlay
        isVisible={!isLoading && isPlaceholderMode}
        onSelectJob={handleSelectJob}
        onCreateJob={handleCreateJob}
      />
    </DashboardLayout>
  );
};

export default JobTraining;
