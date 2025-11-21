import React from 'react';
import { Search, Clock, FileText, Wrench } from 'lucide-react';

interface ToolIndicatorProps {
    toolName?: string;
    toolStatus?: 'in-progress' | 'done';
}

const ToolIndicator: React.FC<ToolIndicatorProps> = ({ toolName, toolStatus }) => {
    const getToolIcon = (toolName?: string) => {
        if (!toolName) return <Wrench size={14} />;
        if (toolName.includes('search')) return <Search size={14} />;
        if (toolName.includes('timer')) return <Clock size={14} />;
        if (toolName.includes('exam') || toolName.includes('test')) return <FileText size={14} />;
        return <Wrench size={14} />;
    };

    return (
        <div className="flex justify-start mb-4">
            <div className="max-w-md">
                <span className="inline-flex items-center gap-1.5 px-3 py-1 text-xs rounded-md text-white bg-[#365c12]">
                    {getToolIcon(toolName)} {toolName || 'tool'}
                </span>
            </div>
        </div>
    );
};

export default ToolIndicator;
