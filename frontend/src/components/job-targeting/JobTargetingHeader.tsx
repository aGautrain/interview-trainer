interface JobTargetingHeaderProps {
  title: string;
  subtitle: string;
}

const JobTargetingHeader = ({ title, subtitle }: JobTargetingHeaderProps) => {
  return (
    <div className="mb-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-2">{title}</h1>
      <p className="text-lg text-gray-600">{subtitle}</p>
    </div>
  );
};

export default JobTargetingHeader;
