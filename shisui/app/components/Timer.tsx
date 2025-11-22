import React, { useState, useEffect } from 'react';

interface TimerProps {
    durationMinutes: number;
    label: string;
    onComplete?: () => void;
}

const Timer: React.FC<TimerProps> = ({ durationMinutes, label, onComplete }) => {
    const [timeLeft, setTimeLeft] = useState(durationMinutes * 60); // Convert to seconds
    const [isActive, setIsActive] = useState(true);
    const [isPaused, setIsPaused] = useState(false);

    useEffect(() => {
        let interval: NodeJS.Timeout | null = null;

        if (isActive && !isPaused && timeLeft > 0) {
            interval = setInterval(() => {
                setTimeLeft((time) => {
                    if (time <= 1) {
                        setIsActive(false);
                        if (onComplete) onComplete();
                        // Play completion sound or notification
                        if ('Notification' in window && Notification.permission === 'granted') {
                            new Notification('Timer Complete!', {
                                body: `${label} timer has finished`,
                                icon: '/Shisui_logo.svg'
                            });
                        }
                        return 0;
                    }
                    return time - 1;
                });
            }, 1000);
        }

        return () => {
            if (interval) clearInterval(interval);
        };
    }, [isActive, isPaused, timeLeft, label, onComplete]);

    const formatTime = (seconds: number): string => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    };

    const togglePause = () => {
        setIsPaused(!isPaused);
    };

    const reset = () => {
        setTimeLeft(durationMinutes * 60);
        setIsActive(true);
        setIsPaused(false);
    };

    const stop = () => {
        setIsActive(false);
        setTimeLeft(0);
    };

    const progress = ((durationMinutes * 60 - timeLeft) / (durationMinutes * 60)) * 100;

    return (
        <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-200 max-w-sm mx-auto">
            {/* Header */}
            <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-green-500 animate-pulse"></div>
                    <span className="text-sm font-medium text-gray-600">Active Timer</span>
                </div>
                <button
                    onClick={stop}
                    className="text-gray-400 hover:text-gray-600 transition-colors"
                    title="Stop timer"
                >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>

            {/* Label */}
            <h3 className="text-lg font-semibold text-gray-800 mb-4">{label}</h3>

            {/* Timer Display */}
            <div className="relative mb-6">
                {/* Progress Circle */}
                <svg className="w-48 h-48 mx-auto transform -rotate-90">
                    <circle
                        cx="96"
                        cy="96"
                        r="88"
                        stroke="#e5e7eb"
                        strokeWidth="8"
                        fill="none"
                    />
                    <circle
                        cx="96"
                        cy="96"
                        r="88"
                        stroke="#365c12"
                        strokeWidth="8"
                        fill="none"
                        strokeDasharray={`${2 * Math.PI * 88}`}
                        strokeDashoffset={`${2 * Math.PI * 88 * (1 - progress / 100)}`}
                        strokeLinecap="round"
                        className="transition-all duration-1000 ease-linear"
                    />
                </svg>

                {/* Time Text */}
                <div className="absolute inset-0 flex items-center justify-center">
                    <span className="text-5xl font-bold text-gray-800 font-mono">
                        {formatTime(timeLeft)}
                    </span>
                </div>
            </div>

            {/* Controls */}
            <div className="flex gap-3 justify-center">
                <button
                    onClick={togglePause}
                    className="px-6 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg font-medium transition-colors flex items-center gap-2"
                >
                    {isPaused ? (
                        <>
                            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z" />
                            </svg>
                            Resume
                        </>
                    ) : (
                        <>
                            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M5 4a2 2 0 012-2h6a2 2 0 012 2v12a2 2 0 01-2 2H7a2 2 0 01-2-2V4z" />
                            </svg>
                            Pause
                        </>
                    )}
                </button>
                <button
                    onClick={reset}
                    className="px-6 py-2 bg-[#365c12] hover:bg-[#2a4a0e] text-white rounded-lg font-medium transition-colors flex items-center gap-2"
                >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                    Reset
                </button>
            </div>

            {/* Status */}
            <div className="mt-4 text-center">
                <p className="text-sm text-gray-500">
                    {isPaused ? '⏸️ Paused' : timeLeft === 0 ? '✅ Complete!' : '⏱️ Running'}
                </p>
            </div>
        </div>
    );
};

export default Timer;
