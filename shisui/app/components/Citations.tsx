import React from 'react';

interface CitationsProps {
    citations: string[];
}

const Citations: React.FC<CitationsProps> = ({ citations }) => {
    if (!citations || citations.length === 0) return null;

    return (
        <div className="mt-4 pt-3 border-t border-gray-200">
            <p className="text-xs font-semibold text-gray-500 mb-2">Sources:</p>
            <ul className="space-y-1">
                {citations.map((citation, index) => (
                    <li key={index} className="text-xs text-gray-500 truncate">
                        <a
                            href={citation}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="hover:text-[#365c12] hover:underline flex items-center gap-1"
                        >
                            <span className="w-4 h-4 inline-flex items-center justify-center rounded-full bg-gray-100 text-gray-600 text-[10px]">
                                {index + 1}
                            </span>
                            {citation}
                        </a>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Citations;
