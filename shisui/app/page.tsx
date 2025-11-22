"use client";

import React, { useState } from 'react';
import ChatSection from './components/ChatSection';
import Timer from './components/Timer';
import Schedule from './components/Schedule';

interface Message {
  role: 'user' | 'assistant' | 'tool-indicator' | 'agent-working';
  content: string;
  toolName?: string;
  toolStatus?: 'in-progress' | 'done';
  agentName?: string;
  agentDisplay?: string;
  citations?: string[];
}

interface TimerData {
  durationMinutes: number;
  label: string;
  message: string;
}

interface ScheduleData {
  schedule: { time: string; activity: string }[];
  message: string;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentAgent, setCurrentAgent] = useState<string | null>(null);
  const [activeTimer, setActiveTimer] = useState<TimerData | null>(null);
  const [activeSchedule, setActiveSchedule] = useState<ScheduleData | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);

  const handleSendMessage = async (text: string) => {
    // Add user message
    const userMessage: Message = { role: 'user', content: text };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text,
          session_id: sessionId
        }),
      });

      if (!response.body) throw new Error('No response body');

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let assistantMessage: Message = { role: 'assistant', content: '' };
      let buffer = '';
      let currentAgentName: string | null = null;
      let currentAgentDisplay: string | null = null;

      setMessages((prev) => [...prev, assistantMessage]);

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });

        // Process complete SSE messages (lines ending with \n\n)
        const lines = buffer.split('\n\n');
        buffer = lines.pop() || ''; // Keep incomplete message in buffer

        for (const line of lines) {
          if (!line.trim() || !line.startsWith('data: ')) continue;

          try {
            // Extract JSON from "data: {...}" format
            const jsonStr = line.substring(6); // Remove "data: " prefix
            const event = JSON.parse(jsonStr);

            switch (event.type) {
              case 'session':
                if (!sessionId) {
                  setSessionId(event.session_id);
                }
                break;

              case 'agent_working':
                currentAgentName = event.agent_name;
                currentAgentDisplay = event.agent_display;
                setCurrentAgent(currentAgentDisplay);
                break;

              case 'tool_call':
                // Add tool indicator message
                setMessages((prev) => [
                  ...prev,
                  {
                    role: 'tool-indicator',
                    content: '',
                    toolName: event.tool_name,
                    toolStatus: 'in-progress'
                  }
                ]);
                break;

              case 'content':
                // Append content to assistant message
                setMessages((prev) => {
                  const newMessages = [...prev];
                  const lastMsg = newMessages[newMessages.length - 1];

                  if (lastMsg && lastMsg.role === 'assistant') {
                    // Update existing assistant message
                    const updatedMsg = {
                      ...lastMsg,
                      content: lastMsg.content + event.content,
                      agentName: event.agent_name || lastMsg.agentName,
                      agentDisplay: event.agent_display || lastMsg.agentDisplay
                    };
                    newMessages[newMessages.length - 1] = updatedMsg;
                    return newMessages;
                  } else {
                    // Create new assistant message (e.g. after tool call)
                    const newMsg: Message = {
                      role: 'assistant',
                      content: event.content,
                      agentName: event.agent_name || currentAgentName || undefined,
                      agentDisplay: event.agent_display || currentAgentDisplay || undefined
                    };
                    return [...newMessages, newMsg];
                  }
                });
                break;

              case 'done':
                setCurrentAgent(null);
                break;

              case 'timer_start':
                // Handle timer start event
                setActiveTimer({
                  durationMinutes: event.duration_minutes,
                  label: event.label,
                  message: event.message
                });
                break;

              case 'schedule_set':
                // Handle schedule set event
                setActiveSchedule({
                  schedule: event.schedule,
                  message: event.message
                });
                break;

              case 'citations':
                // Handle citations event
                assistantMessage.citations = event.citations;
                setMessages((prev) => {
                  const newMessages = [...prev];
                  newMessages[newMessages.length - 1] = { ...assistantMessage };
                  return newMessages;
                });
                break;

              case 'error':
                console.error('Backend error:', event.error);
                assistantMessage.content = `Error: ${event.error}`;
                setMessages((prev) => {
                  const newMessages = [...prev];
                  newMessages[newMessages.length - 1] = { ...assistantMessage };
                  return newMessages;
                });
                break;
            }
          } catch (parseError) {
            console.error('Failed to parse SSE event:', line, parseError);
          }
        }
      }

    } catch (error) {
      console.error('Error:', error);
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'Sorry, something went wrong. Please try again.' }
      ]);
    } finally {
      setIsLoading(false);
      setCurrentAgent(null);
    }
  };

  return (
    <main className="relative">
      <ChatSection
        messages={messages}
        onSendMessage={handleSendMessage}
        isLoading={isLoading}
        currentAgent={currentAgent}
      />

      {/* Timer Overlay */}
      {activeTimer && (
        <div className="fixed bottom-6 right-6 z-50 animate-in slide-in-from-bottom-4">
          <Timer
            durationMinutes={activeTimer.durationMinutes}
            label={activeTimer.label}
            onComplete={() => setActiveTimer(null)}
          />
        </div>
      )}

      {/* Schedule Overlay */}
      {activeSchedule && (
        <div className="fixed bottom-6 left-6 z-50 animate-in slide-in-from-bottom-4">
          <Schedule
            schedule={activeSchedule.schedule}
            onClose={() => setActiveSchedule(null)}
          />
        </div>
      )}
    </main>
  );
}
