import React from 'react';

interface Task {
    time: string;
    activity: string;
}

interface ScheduleProps {
    schedule: Task[];
    onClose?: () => void;
}

const Schedule: React.FC<ScheduleProps> = ({ schedule, onClose }) => {
    return (
        <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-200 max-w-sm mx-auto">
            {/* Header */}
            <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-blue-500"></div>
                    <span className="text-sm font-medium text-gray-600">Study Schedule</span>
                </div>
                <button
                    onClick={onClose}
                    className="text-gray-400 hover:text-gray-600 transition-colors"
                    title="Close schedule"
                >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>

            {/* Schedule List */}
            <div className="space-y-3 max-h-96 overflow-y-auto">
                {schedule.map((task, index) => (
                    <div key={index} className="flex gap-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                        <div className="flex-shrink-0 w-16 text-sm font-semibold text-blue-600">
                            {task.time}
                        </div>
                        <div className="text-sm text-gray-700">
                            {task.activity}
                        </div>
                    </div>
                ))}
            </div>

            {/* Footer */}
            <div className="mt-4 pt-4 border-t border-gray-100 text-center">
                <p className="text-xs text-gray-400">
                    {schedule.length} tasks scheduled
                </p>
            </div>
        </div>
    );
};

export default Schedule;
