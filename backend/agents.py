from crewai import Agent, Task, Crew
from langchain.tools import Tool

# Define tools for agents
def explain_concept(concept: str, level: str) -> str:
    """Explains a concept at the appropriate level"""
    return f"Explanation of {concept} for {level} level student"

def check_assignment(assignment: str) -> str:
    """Analyzes an assignment submission"""
    return f"Analysis of: {assignment}"

def track_progress(subject: str) -> str:
    """Gets current progress in a subject"""
    return f"Progress report for {subject}"

def flag_cheating(text: str) -> bool:
    """Checks if text appears to be homework help rather than learning"""
    # Simple heuristic - can be expanded
    suspicious_phrases = ["solve this for me", "just give me the answer", "do my homework"]
    return any(phrase in text.lower() for phrase in suspicious_phrases)

# Tool definitions
explain_tool = Tool(
    name="explain_concept",
    func=explain_concept,
    description="Explains a concept using Socratic method"
)

assignment_tool = Tool(
    name="check_assignment",
    func=check_assignment,
    description="Analyzes student assignment submissions"
)

progress_tool = Tool(
    name="track_progress",
    func=track_progress,
    description="Tracks student progress over time"
)

ethics_tool = Tool(
    name="flag_cheating",
    func=flag_cheating,
    description="Identifies potential homework cheating attempts"
)

# Define Agents
tutor_agent = Agent(
    role="Tutor Agent",
    goal="Help students understand concepts through Socratic questioning",
    backstory="Expert educator who guides students to discover answers themselves",
    tools=[explain_tool],
)

task_manager_agent = Agent(
    role="Task Manager Agent", 
    goal="Track assignments and deadlines",
    backstory="Organized assistant who keeps students on top of their work",
    tools=[assignment_tool],
)

progress_agent = Agent(
    role="Progress Tracker Agent",
    goal="Analyze student performance and identify areas for improvement",
    backstory="Data-driven tutor who personalizes learning paths",
    tools=[progress_tool],
)

ethics_agent = Agent(
    role="Ethics Guard",
    goal="Ensure platform is used for learning, not cheating",
    backstory="Academic integrity monitor preventing misuse",
    tools=[ethics_tool],
)

# Define Tasks
def create_tutoring_task(topic: str):
    return Task(
        description=f"Help student understand {topic} through guided questions",
        agent=tutor_agent,
        expected_output=f"Explanation and questions about {topic}"
    )

def create_task_review_task(assignment: str):
    return Task(
        description=f"Review student work on: {assignment}",
        agent=task_manager_agent,
        expected_output="Feedback on assignment"
    )

def create_progress_review_task(student_id: str):
    return Task(
        description=f"Generate progress report for student {student_id}",
        agent=progress_agent,
        expected_output="Detailed progress analysis"
    )

def create_ethics_check_task(user_input: str):
    return Task(
        description=f"Check if input violates academic integrity: {user_input}",
        agent=ethics_agent,
        expected_output="Safety check result"
    )
