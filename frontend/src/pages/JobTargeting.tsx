import { useState } from "react";
import DashboardLayout from "../components/layouts/DashboardLayout";
import {
  JobTargetingHeader,
  JobDescriptionInput,
  UrlExtractionModal,
  AnalyzeButton,
} from "../components/job-targeting";
import { JobAnalysisResults } from "../components/job-targeting/JobAnalysisResults";
import { 
  jobAnalysisService, 
  type JobAnalysisRequest,
  type JobAnalysisError,
  type JobAnalysisState 
} from "../services/jobAnalysisService";

const JobTargeting = () => {
  const [jobDescription, setJobDescription] = useState("");
  const [jobUrl, setJobUrl] = useState("");
  const [isUrlPopupOpen, setIsUrlPopupOpen] = useState(false);
  
  // Analysis state management
  const [analysisState, setAnalysisState] = useState<JobAnalysisState>({
    isLoading: false,
    error: null,
    result: null,
    analysisId: undefined
  });

  const handleAnalyzeJob = async () => {
    if (!jobDescription.trim()) {
      setAnalysisState(prev => ({
        ...prev,
        error: {
          message: "Please enter a job description to analyze",
          code: "EMPTY_JOB_DESCRIPTION"
        }
      }));
      return;
    }

    // Validate request
    const validationErrors = jobAnalysisService.validateJobAnalysisRequest({
      job_description: jobDescription
    });

    if (validationErrors.length > 0) {
      setAnalysisState(prev => ({
        ...prev,
        error: validationErrors[0]
      }));
      return;
    }

    // Clear previous state and start loading
    setAnalysisState({
      isLoading: true,
      error: null,
      result: null,
      analysisId: undefined
    });

    try {
      const request: JobAnalysisRequest = {
        job_description: jobDescription,
        analysis_depth: 'standard'
      };

      const response = await jobAnalysisService.analyzeJob(request);
      
      if (response.success && response.result) {
        setAnalysisState({
          isLoading: false,
          error: null,
          result: response.result,
          analysisId: response.analysis_id
        });
      } else {
        setAnalysisState({
          isLoading: false,
          error: {
            message: response.error_message || "Analysis failed",
            status: response.success ? 200 : 500,
            details: { response }
          },
          result: null,
          analysisId: response.analysis_id
        });
      }
    } catch (error) {
      console.error("Job analysis failed:", error);
      setAnalysisState({
        isLoading: false,
        error: error as JobAnalysisError,
        result: null,
        analysisId: undefined
      });
    }
  };

  const handleRetryAnalysis = () => {
    handleAnalyzeJob();
  };

  const handleClearResults = () => {
    setAnalysisState({
      isLoading: false,
      error: null,
      result: null,
      analysisId: undefined
    });
  };

  const handleNewAnalysis = () => {
    setAnalysisState({
      isLoading: false,
      error: null,
      result: null,
      analysisId: undefined
    });
    setJobDescription("");
  };

  const handleTrainJob = () => {
    // Navigate to job training page with analysis data
    console.log("Navigating to job training with analysis:", analysisState.analysisId);
    // TODO: Implement navigation to job training page
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

  const hasCompletedAnalysis = analysisState.result && !analysisState.isLoading;

  return (
    <DashboardLayout>
      <JobTargetingHeader
        title="Job Targeting"
        subtitle="Analyze job descriptions to extract requirements and skills."
      />

      {/* Show input and analyze sections only when no completed analysis */}
      {!hasCompletedAnalysis && (
        <>
          <JobDescriptionInput
            jobDescription={jobDescription}
            onJobDescriptionChange={setJobDescription}
            onExtractFromUrl={openUrlPopup}
            disabled={analysisState.isLoading}
          />

          <AnalyzeButton 
            onAnalyze={handleAnalyzeJob} 
            isLoading={analysisState.isLoading}
            disabled={!jobDescription.trim() || analysisState.isLoading}
          />
        </>
      )}

      {/* Show action buttons when analysis is complete */}
      {hasCompletedAnalysis && (
        <div className="mb-6 flex justify-center">
          <div className="flex flex-col sm:flex-row gap-4 w-full max-w-md">
            <button
              onClick={handleTrainJob}
              className="flex items-center justify-center space-x-2 px-8 py-4 rounded-lg font-medium transition-all duration-200 bg-gray-800 text-white hover:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              <span>Train Job</span>
            </button>
            <button
              onClick={handleNewAnalysis}
              className="flex items-center justify-center space-x-2 px-6 py-3 rounded-lg font-medium transition-all duration-200 bg-gray-100 hover:bg-gray-200 text-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
            >
              <span>New Analysis</span>
            </button>
          </div>
        </div>
      )}

      {/* Analysis Results Section */}
      {(analysisState.result || analysisState.error) && (
        <JobAnalysisResults
          state={analysisState}
          onRetry={handleRetryAnalysis}
          onClear={handleClearResults}
        />
      )}

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
