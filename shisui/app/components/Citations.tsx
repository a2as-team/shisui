import React from 'react';
import { ExternalLink } from 'lucide-react';

interface CitationsProps {
    citations: string[];
}

const Citations: React.FC<CitationsProps> = ({ citations }) => {
    if (!citations || citations.length === 0) return null;


    const getDomain = (url: string) => {
        try {
            const domain = new URL(url).hostname.replace('www.', '');
            return domain;
        } catch {
            return 'link';
        }
    };

    const getFaviconUrl = (url: string) => {
        try {
            const domain = new URL(url).hostname;
            return `https://www.google.com/s2/favicons?domain=${domain}&sz=32`;
        } catch {
            return null;
        }
    };

    return (
        <div className="mt-4 pt-4 border-t border-gray-200">
            <p className="text-xs font-semibold text-gray-700 mb-3">Sources</p>
            <div className="flex flex-wrap gap-2">
                {citations.map((citation, index) => {
                    const domain = getDomain(citation);
                    const faviconUrl = getFaviconUrl(citation);

                    return (
                        <a
                            key={index}
                            href={citation}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="group inline-flex items-center gap-2 px-3 py-1.5 bg-white border border-gray-200 rounded-full hover:border-[#365c12] hover:bg-gray-50 transition-all duration-200 shadow-sm hover:shadow"
                        >
                            {faviconUrl && (
                                <img
                                    src={faviconUrl}
                                    alt=""
                                    className="w-4 h-4 flex-shrink-0"
                                    onError={(e) => {
                                        e.currentTarget.style.display = 'none';
                                    }}
                                />
                            )}
                            <span className="text-xs text-gray-700 group-hover:text-[#365c12] font-medium truncate max-w-[200px]">
                                {domain}
                            </span>
                            <ExternalLink className="w-3 h-3 text-gray-400 group-hover:text-[#365c12] flex-shrink-0" />
                        </a>
                    );
                })}
            </div>
        </div>
    );

};

export default Citations;
