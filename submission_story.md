## Inspiration
As students, we often find ourselves juggling multiple tools—search engines for research, timers for focus, and separate platforms for testing our knowledge. We wanted to unify this fragmented experience into a single, intelligent companion that adapts to our learning style. Inspired by the potential of Google's Gemini API and the spirit of the **MLH Machine Learning Day (Nairobi)**, we set out to create Shisui. Although we couldn't attend the hackathon in person, we were determined to participate and challenge ourselves to build a comprehensive learning companion in under 12 hours.

## What it does
Shisui is a multi-agent learning platform that acts as your personal tutor. It's not just a chatbot; it's a team of specialized AI agents working together:
*   **Smart Research**: The Course Agent uses Perplexity API to fetch real-time, citation-backed information on any topic, ensuring you're learning from up-to-date sources.
*   **Adaptive Testing**: The Exam Agent, powered by **Google Gemini**, generates custom quizzes tailored to what you've just studied. It provides instant feedback and even exports professional PDF exams for offline practice.
*   **Study Management**: Built-in Pomodoro timers and session tracking help you maintain focus and monitor your progress.
*   **Intelligent Orchestration**: A Planner Agent intelligently routes your requests to the right specialist, making the experience seamless.

## How we built it
We built Shisui using a modern, scalable stack designed for speed and performance:
*   **Backend**: We utilized **FastAPI** for its high performance and async capabilities. The core intelligence is powered by **Google's Agent Development Kit (ADK)**, which allowed us to orchestrate multiple specialized agents (Planner, Course, and Exam agents).
*   **AI & Data**: We leveraged **Google Gemini** for high-quality content generation and reasoning, and **Perplexity API** for accurate, real-time web search capabilities. **SQLite** handles our local history and session management.
*   **Frontend**: The user interface is built with **Next.js 16** and **Tailwind CSS v4**, offering a sleek, responsive experience with real-time streaming responses via Server-Sent Events (SSE).
*   **PDF Generation**: We integrated **ReportLab** to dynamically generate professional-grade exam papers from the AI-generated content.

## Challenges we ran into
The biggest challenge was orchestrating the communication between different agents. Ensuring that the Planner Agent correctly identified the user's intent and routed it to the Course or Exam agent without latency was tricky. We also had to handle the asynchronous nature of multiple API calls (Gemini, Perplexity) while keeping the UI responsive and providing real-time feedback to the user. Debugging the state management across these independent agents within the 12-hour constraint was an intense but rewarding experience.

## Accomplishments that we're proud of
We're incredibly proud of the **Agent-to-Agent (A2A) communication** system we built. Seeing the Planner Agent autonomously decide to trigger a research task or generate an exam feels like magic. We're also proud of the **PDF export feature**—taking an abstract AI conversation and turning it into a tangible, study-ready document was a huge win. Most importantly, we managed to build a full-stack, multi-agent application with a polished UI in such a short timeframe.

## What we learned
We learned the immense potential of **agentic workflows**. Instead of a single monolithic prompt, breaking down tasks into specialized agents leads to much higher quality results. We also gained deep insights into the **Google Gemini API** capabilities, particularly in structured data generation for our exam tools. The hackathon format taught us to prioritize core features and iterate quickly.

## What's next for Shisui
We plan to expand Shisui's capabilities by adding:
*   **Voice Interaction**: Allowing students to quiz themselves verbally.
*   **Collaborative Study**: Enabling users to share study guides and quizzes with friends.
*   **More Agents**: Introducing a Coding Agent for programming help and a Math Agent for step-by-step problem solving.
*   **Mobile App**: Bringing the Shisui experience to iOS and Android for learning on the go.
