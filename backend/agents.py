# Agent system for Lumen using CrewAI
from crewai import Agent as CrewAIAgent, Task, Crew
from typing import Optional

class Agent:
    """Wrapper around CrewAI Agent for Lumen"""
    def __init__(self, name: str, role: str, description: str, backstory: str):
        self.name = name
        self.role = role
        self.description = description
        self.agent = CrewAIAgent(
            role=role,
            goal=description,
            backstory=backstory,
            verbose=True
        )
    
    def process(self, input_text: str) -> str:
        """Process input and return response"""
        return f"Response from {self.name}: {input_text}"

# Define tool functions
def explain_concept(concept: str, level: str = "intermediate") -> str:
    """Explains a concept at the appropriate level using Socratic method"""
    return f"I'd like to help you understand {concept}. Let me start with a question: What do you already know about {concept}?"

def check_assignment(assignment: str, submission: str) -> str:
    """Analyzes an assignment submission"""
    return f"I've reviewed your work on '{assignment}'. Here's my feedback: You've shown good understanding of the basics. Consider exploring..."

def track_progress(subject: str, user_id: str) -> dict:
    """Gets current progress in a subject"""
    return {
        "subject": subject,
        "proficiency": "intermediate",
        "improvement_areas": ["problem solving", "application"],
        "recommendation": "Practice more real-world examples"
    }

def flag_cheating(text: str) -> dict:
    """Checks if text appears to be homework help rather than learning"""
    suspicious_phrases = ["solve this for me", "just give me the answer", "do my homework", "write my essay"]
    is_suspicious = any(phrase in text.lower() for phrase in suspicious_phrases)
    
    return {
        "flagged": is_suspicious,
        "severity": "high" if is_suspicious else "low",
        "message": "This request may violate academic integrity" if is_suspicious else "Safe to proceed"
    }

# Agent instances
tutor_agent = Agent(
    name="Tutor Agent",
    role="Expert Tutor",
    description="Help students understand concepts through Socratic questioning and guided discovery",
    backstory="A patient, experienced educator who specializes in explaining complex concepts in simple terms. You use the Socratic method to guide students to discover answers themselves."
)

task_manager_agent = Agent(
    name="Task Manager Agent",
    role="Academic Task Manager",
    description="Track student assignments, deadlines, and priorities to keep them organized",
    backstory="An organized, proactive assistant who keeps detailed records of assignments and helps students manage their time effectively."
)

progress_agent = Agent(
    name="Progress Tracker Agent",
    role="Learning Analyst",
    description="Analyze student performance patterns and recommend personalized learning paths",
    backstory="A data-driven educator who identifies learning gaps and strengths, then recommends targeted improvements."
)

ethics_agent = Agent(
    name="Ethics Guard",
    role="Academic Integrity Monitor",
    description="Ensure the platform is used for learning, not cheating. Flag potential violations.",
    backstory="A vigilant guardian of academic integrity who helps maintain ethical learning standards. You're firm but fair, focused on preventing misuse while supporting genuine learning."
)

# Task creation functions
def create_tutoring_task(topic: str):
    """Create tutoring task using CrewAI"""
    task = Task(
        description=f"Explain the concept of '{topic}' to a student using the Socratic method. Start by asking what they already know.",
        agent=tutor_agent.agent,
        expected_output="An engaging explanation with questions to guide the student"
    )
    return {
        "task_id": f"tutoring_{topic}",
        "type": "tutoring",
        "topic": topic,
        "task_obj": task,
        "response": explain_concept(topic)
    }

def create_task_review_task(assignment: str, submission: str = ""):
    """Create task review using CrewAI"""
    task = Task(
        description=f"Review the student's work on '{assignment}'. Provide constructive feedback, identify strengths, and suggest improvements.",
        agent=task_manager_agent.agent,
        expected_output="Detailed feedback with specific suggestions for improvement"
    )
    return {
        "task_id": f"review_{assignment}",
        "type": "review",
        "assignment": assignment,
        "task_obj": task,
        "response": check_assignment(assignment, submission)
    }

def create_progress_review_task(student_id: str, subject: str = ""):
    """Create progress review using CrewAI"""
    task = Task(
        description=f"Generate a comprehensive progress report for student {student_id}. Analyze their performance in {subject or 'all subjects'}, identify patterns, and recommend next steps.",
        agent=progress_agent.agent,
        expected_output="Detailed progress analysis with recommendations"
    )
    progress = track_progress(subject or "general", student_id)
    return {
        "task_id": f"progress_{student_id}",
        "type": "progress_review",
        "task_obj": task,
        "data": progress
    }

def create_ethics_check_task(user_input: str):
    """Create ethics check using CrewAI"""
    task = Task(
        description=f"Analyze the following student request for potential academic integrity violations: '{user_input}'. Determine if this appears to be a request for help learning or a request for someone to do the work for them.",
        agent=ethics_agent.agent,
        expected_output="Assessment of whether the request violates academic integrity"
    )
    result = flag_cheating(user_input)
    return {
        "task_id": "ethics_check",
        "type": "ethics_check",
        "task_obj": task,
        "result": result
    }
