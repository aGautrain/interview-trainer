import { SparklesIcon } from "@heroicons/react/24/outline";

interface JobDescriptionInputProps {
  jobDescription: string;
  onJobDescriptionChange: (value: string) => void;
  onExtractFromUrl: () => void;
}

const JobDescriptionInput = ({
  jobDescription,
  onJobDescriptionChange,
  onExtractFromUrl,
}: JobDescriptionInputProps) => {
  return (
    <div className="max-w-4xl mx-auto mb-8">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 relative">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-gray-900">
            Job Description
          </h2>
          <button
            onClick={onExtractFromUrl}
            className="p-2 bg-blue-600 text-white hover:bg-blue-700 rounded-lg transition-colors"
            title="Extract from URL"
          >
            <SparklesIcon className="w-5 h-5" />
          </button>
        </div>
        <p className="text-gray-600 mb-4">
          Copy and paste the job description directly, or use the magic wand to
          extract from a URL.
        </p>
        <textarea
          value={jobDescription}
          onChange={(e) => onJobDescriptionChange(e.target.value)}
          placeholder="Paste the job description here..."
          className="w-full h-48 p-4 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        />
      </div>
    </div>
  );
};

export default JobDescriptionInput;
