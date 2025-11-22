import React, { useRef, useEffect, useState } from 'react';
import ChatBubble from './ChatBubble';
import ChatInput from './ChatInput';
import ToolIndicator from './ToolIndicator';
import AgentResponseWrapper from './AgentResponseWrapper';
import WelcomeSuggestions from './WelcomeSuggestions';

interface Message {
    role: 'user' | 'assistant' | 'tool-indicator' | 'agent-working';
    content: string;
    toolName?: string;
    toolStatus?: 'in-progress' | 'done';
    agentName?: string;
    agentDisplay?: string;
    citations?: string[];
}

interface ChatSectionProps {
    messages: Message[];
    onSendMessage: (message: string) => void;
    isLoading?: boolean;
    currentAgent?: string | null;
}

const MessageRenderer = ({ message, index }: { message: Message; index: number }) => {
    switch (message.role) {
        case 'tool-indicator':
            return <ToolIndicator key={index} toolName={message.toolName} toolStatus={message.toolStatus} />;
        case 'agent-working':
            return null;
        default:
            return <ChatBubble key={index} role={message.role} content={message.content} citations={message.citations} />;
    }
};

const ChatSection: React.FC<ChatSectionProps> = ({
    messages,
    onSendMessage,
    isLoading = false,
    currentAgent = null,
}) => {
    const chatContainerRef = useRef<HTMLDivElement>(null);
    const [greeting, setGreeting] = useState("Hello!");

    useEffect(() => {
        const hour = new Date().getHours();
        if (hour < 12) setGreeting("Good morning!");
        else if (hour < 18) setGreeting("Good afternoon!");
        else setGreeting("Good evening!");
    }, []);

    useEffect(() => {
        if (chatContainerRef.current) {
            chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
        }
    }, [messages, isLoading]);

    const hasMessages = messages.length > 0;

    // Group messages by sub-agent turn
    const groupedMessages: (Message | { isGroup: true; agentName: string; agentDisplay: string; messages: Message[] })[] = [];
    let currentGroup: { isGroup: true; agentName: string; agentDisplay: string; messages: Message[] } | null = null;

    for (const message of messages) {
        const agentName = message.agentName;
        const agentDisplay = message.agentDisplay;

        if (agentName && agentDisplay) {
            if (currentGroup && currentGroup.agentName === agentName) {
                currentGroup.messages.push(message);
            } else {
                if (currentGroup) {
                    groupedMessages.push(currentGroup);
                }
                currentGroup = {
                    isGroup: true,
                    agentName,
                    agentDisplay,
                    messages: [message],
                };
            }
        } else {
            if (currentGroup) {
                if (message.role === 'tool-indicator') {
                    currentGroup.messages.push(message);
                    continue;
                }
                groupedMessages.push(currentGroup);
                currentGroup = null;
            }
            groupedMessages.push(message);
        }
    }
    if (currentGroup) {
        groupedMessages.push(currentGroup);
    }

    if (!hasMessages) {
        return (
            <div className="h-screen flex flex-col items-center justify-center relative bg-[#f9fafb] overflow-hidden">
                {/* Background Image */}
                <div className="absolute inset-0 z-0">
                    <img
                        src="/welcome.png"
                        alt=""
                        className="w-full h-full object-cover opacity-30"
                    />
                </div>

                <div className="absolute top-6 left-6 flex items-center gap-3 z-10">
                    <img src="/Shisui_logo.svg" alt="Shisui Logo" className="w-8 h-8" />
                    <span className="text-xl font-bold text-gray-800">Shisui</span>
                </div>
                <div className="text-center mb-8 z-10 relative">
                    <h1 className="text-4xl font-bold text-gray-800">{greeting}</h1>
                    <p className="text-gray-500 mt-2">Your personal learning assistant.</p>
                </div>

                <WelcomeSuggestions onSuggestionClick={(text) => onSendMessage(text)} />
                <ChatInput onSendMessage={onSendMessage} disabled={isLoading} currentAgent={currentAgent} />
            </div>
        );
    }

    return (
        <div className="h-screen relative bg-[#f9fafb]">
            <div className="absolute top-6 left-6 flex items-center gap-3 z-10">
                <img src="/Shisui_logo.svg" alt="Shisui Logo" className="w-8 h-8" />
                <span className="text-lg font-bold text-gray-800">Shisui</span>
            </div>

            <div ref={chatContainerRef} className="h-full overflow-y-auto pt-16 fade-out-bottom scrollbar-hide">
                <div className="max-w-2xl mx-auto px-8 pb-40">
                    <div className="space-y-8">
                        {groupedMessages.map((item, index) => {
                            if ('isGroup' in item) {
                                // Don't wrap planner agent messages
                                if (item.agentName === 'planner_agent') {
                                    return (
                                        <div key={index} className="space-y-4">
                                            {item.messages.map((message, msgIndex) => (
                                                <MessageRenderer key={msgIndex} message={message} index={msgIndex} />
                                            ))}
                                        </div>
                                    );
                                }

                                return (
                                    <AgentResponseWrapper
                                        key={index}
                                        agentName={item.agentName}
                                        agentDisplay={item.agentDisplay}
                                    >
                                        <div className="space-y-4">
                                            {item.messages.map((message, msgIndex) => (
                                                <MessageRenderer key={msgIndex} message={message} index={msgIndex} />
                                            ))}
                                        </div>
                                    </AgentResponseWrapper>
                                );
                            } else {
                                return <MessageRenderer key={index} message={item as Message} index={index} />;
                            }
                        })}

                        {isLoading && (
                            <div className="mb-8">
                                <div className="flex items-start space-x-3">
                                    <div className="flex-shrink-0 w-8 h-8 flex items-center justify-center">
                                        <div
                                            className="rounded-full animate-pulse-scale"
                                            style={{ width: '8px', height: '8px', backgroundColor: '#365c12' }}
                                        ></div>
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </div>

            <div className="fixed bottom-0 left-1/2 -translate-x-1/2 w-full max-w-2xl mb-4 px-4">
                <ChatInput onSendMessage={onSendMessage} disabled={isLoading} currentAgent={currentAgent} />
            </div>
        </div>
    );
};

export default ChatSection;
