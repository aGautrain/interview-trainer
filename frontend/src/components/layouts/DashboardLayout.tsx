import { ReactNode } from "react";
import { Link, useLocation } from "react-router-dom";
import { BriefcaseIcon } from "@heroicons/react/24/outline";

interface DashboardLayoutProps {
  children: ReactNode;
}

const DashboardLayout = ({ children }: DashboardLayoutProps) => {
  const location = useLocation();

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-gradient-to-r from-primary-600 to-primary-800 rounded-lg flex items-center justify-center">
              <BriefcaseIcon className="w-5 h-5 text-white" />
            </div>
            <h1 className="text-xl font-bold text-gray-900">InterviewAce</h1>
          </div>
          <nav className="flex space-x-8">
            <Link
              to="/"
              className={`pb-2 font-medium transition-colors ${
                location.pathname === "/" || location.pathname === "/home"
                  ? "text-primary-600 border-b-2 border-primary-600"
                  : "text-gray-500 hover:text-gray-700"
              }`}
            >
              Dashboard
            </Link>
            <Link
              to="/job-targeting"
              className={`pb-2 font-medium transition-colors ${
                location.pathname === "/job-targeting"
                  ? "text-primary-600 border-b-2 border-primary-600"
                  : "text-gray-500 hover:text-gray-700"
              }`}
            >
              Job Targeting
            </Link>
          </nav>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-6 py-8">{children}</div>
    </div>
  );
};

export default DashboardLayout;
