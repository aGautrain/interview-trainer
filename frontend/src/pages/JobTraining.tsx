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
  sampleSkills,
} from "../components/job-training";
import { SkillCard as SkillCardType } from "../types/job-training";
import { Job } from "../types/dashboard";

const JobTraining = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [selectedJob, setSelectedJob] = useState<Job>(placeholderJob);
  const [isPlaceholderMode, setIsPlaceholderMode] = useState(true);
  const [skills] = useState<SkillCardType[]>(sampleSkills);

  useEffect(() => {
    const jobFromState = location.state?.selectedJob;
    if (jobFromState) {
      setSelectedJob(jobFromState);
      setIsPlaceholderMode(false);
    } else {
      setSelectedJob(placeholderJob);
      setIsPlaceholderMode(true);
    }
  }, [location.state]);

  const handleSelectJob = () => {
    navigate("/");
  };

  const handleCreateJob = () => {
    navigate("/job-targeting");
  };

  const handleSkillClick = (skill: SkillCardType) => {
    // Handle skill click - could open practice mode, etc.
    console.log("Skill clicked:", skill.name);
  };

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
        isVisible={isPlaceholderMode}
        onSelectJob={handleSelectJob}
        onCreateJob={handleCreateJob}
      />
    </DashboardLayout>
  );
};

export default JobTraining;
