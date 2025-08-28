interface UrlExtractionModalProps {
  isOpen: boolean;
  jobUrl: string;
  onJobUrlChange: (value: string) => void;
  onExtract: () => void;
  onClose: () => void;
}

const UrlExtractionModal = ({
  isOpen,
  jobUrl,
  onJobUrlChange,
  onExtract,
  onClose,
}: UrlExtractionModalProps) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl p-6 w-full max-w-md mx-4">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">
            Extract from URL
          </h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <svg
              className="w-6 h-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
        <p className="text-gray-600 mb-4">
          Automatically extract job description from URL.
        </p>
        <div className="space-y-4">
          <input
            type="url"
            value={jobUrl}
            onChange={(e) => onJobUrlChange(e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            placeholder="https://company.com/jobs/senior-developer"
          />
          <div className="flex space-x-3">
            <button
              onClick={onClose}
              className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Cancel
            </button>
            <button
              onClick={onExtract}
              className="flex-1 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
            >
              Extract
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UrlExtractionModal;
