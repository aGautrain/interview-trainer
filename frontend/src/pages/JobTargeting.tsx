import { useState } from "react";
import DashboardLayout from "../components/layouts/DashboardLayout";
import {
  JobTargetingHeader,
  JobDescriptionInput,
  UrlExtractionModal,
  AnalyzeButton,
} from "../components/job-targeting";

const JobTargeting = () => {
  const [jobDescription, setJobDescription] = useState("");
  const [jobUrl, setJobUrl] = useState("");
  const [isUrlPopupOpen, setIsUrlPopupOpen] = useState(false);

  const handleAnalyzeJob = () => {
    // TODO: Implement job analysis logic
    console.log("Analyzing job:", { jobDescription, jobUrl });
  };

  const handleExtractFromUrl = () => {
    // TODO: Implement URL extraction logic
    console.log("Extracting from URL:", jobUrl);
    setIsUrlPopupOpen(false);
  };

  const openUrlPopup = () => {
    setIsUrlPopupOpen(true);
  };

  const closeUrlPopup = () => {
    setIsUrlPopupOpen(false);
  };

  return (
    <DashboardLayout>
      <JobTargetingHeader
        title="Job Targeting"
        subtitle="Analyze job descriptions to extract requirements and skills."
      />

      <JobDescriptionInput
        jobDescription={jobDescription}
        onJobDescriptionChange={setJobDescription}
        onExtractFromUrl={openUrlPopup}
      />

      <AnalyzeButton onAnalyze={handleAnalyzeJob} />

      <UrlExtractionModal
        isOpen={isUrlPopupOpen}
        jobUrl={jobUrl}
        onJobUrlChange={setJobUrl}
        onExtract={handleExtractFromUrl}
        onClose={closeUrlPopup}
      />
    </DashboardLayout>
  );
};

export default JobTargeting;
