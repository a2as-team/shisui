# Walkthrough - Message Duplication Fix

I have fixed the issue where messages were being duplicated in the chat interface.

## Changes

### Frontend (`shisui/app/page.tsx`)

The issue was caused by how the chat component handled incoming Server-Sent Events (SSE) for message content. It was accumulating the entire message history in a way that caused conflicts when tool calls occurred, leading to duplicated text.

I updated the `content` event handler to:
1.  Check if the last message in the state is an `assistant` message.
2.  If it is, append the new content chunk to it.
3.  If not (e.g., the last message was a tool indicator), create a new `assistant` message.

```typescript
// shisui/app/page.tsx

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
```

### Backend (`Shisui-backend/main.py`)

I added temporary debug logs to investigate the issue and confirmed that the backend was sending the correct events. These logs have been removed to keep the code clean.

## Verification

The fix ensures that:
-   Standard text responses are streamed correctly without duplication.
-   Responses following a tool call (like setting a timer) are appended as new messages or continuations as appropriate, preventing the "overwrite" behavior that led to duplication.
