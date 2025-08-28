interface PlaceholderOverlayProps {
  isVisible: boolean;
  onSelectJob: () => void;
  onCreateJob: () => void;
}

const PlaceholderOverlay = ({
  isVisible,
  onSelectJob,
  onCreateJob,
}: PlaceholderOverlayProps) => {
  if (!isVisible) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-8 max-w-md mx-4 text-center">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">
          Select a Job to Start Training
        </h3>
        <p className="text-gray-600 mb-6">
          Choose an existing job target or create a new one to begin your skill
          training.
        </p>
        <div className="flex flex-col space-y-3">
          <button onClick={onSelectJob} className="btn-primary w-full py-3">
            Go to Dashboard
          </button>
          <button onClick={onCreateJob} className="btn-secondary w-full py-3">
            Create New Job Target
          </button>
        </div>
      </div>
    </div>
  );
};

export default PlaceholderOverlay;
