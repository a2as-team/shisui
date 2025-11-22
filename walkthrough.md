# Walkthrough - Schedule Feature Implementation

I have implemented a new scheduling feature that allows the Course Agent to create and display study schedules for the user.

## Changes

### Backend

1.  **New Tool (`tools/schedule_tool.py`)**:
    -   Created `create_study_schedule` tool that accepts a list of tasks (time and activity) and returns a structured response with action `set_schedule`.

2.  **Agent Update (`agents/course_agent.py`)**:
    -   Added `create_schedule` wrapper function.
    -   Updated `course_agent` instructions to use this tool for planning study days.
    -   Added the tool to the agent's tool list.

3.  **Event Handling (`main.py`)**:
    -   Updated the chat loop to detect `set_schedule` action.
    -   Emits a new `schedule_set` SSE event to the frontend.

### Frontend

1.  **New Component (`shisui/app/components/Schedule.tsx`)**:
    -   Created a visual component to display the list of scheduled tasks.
    -   Styled consistently with the existing Timer component.

2.  **Page Update (`shisui/app/page.tsx`)**:
    -   Added `activeSchedule` state.
    -   Added handler for `schedule_set` event.
    -   Added the `Schedule` component overlay to the UI.

## Verification

To verify this feature:
1.  Ask the agent: "Create a study schedule for learning Python today."
2.  The Course Agent should use the `create_schedule` tool.
3.  A schedule card should appear in the bottom-left corner of the screen with the proposed tasks.
