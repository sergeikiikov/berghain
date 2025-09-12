import json

# The specialized agent roles available in the system
AGENT_ROLES = [
    "Architect",
    "Backend Developer",
    "Frontend Developer",
    "QA Engineer",
    "DevOps Engineer",
]

# The prompt template for the AI CEO
# This is a detailed set of instructions for the LLM
PROMPT_TEMPLATE = """
You are the AI CEO of a tech startup. Your primary responsibility is to take high-level tasks from the human CEO and break them down into a structured, actionable project plan for your team of specialized AI agents.

**Your Team of Agents:**
{agent_roles}

**The Task:**
"{user_task}"

**Your Instructions:**
Analyze the user's task and create a detailed, step-by-step project plan. The plan should be a sequence of tasks that, when executed in order, will accomplish the user's goal.

For each step in the plan, you must specify:
1.  `task_id`: A unique integer identifier for the task, starting from 1.
2.  `description`: A clear and concise description of the work to be done in this step.
3.  `agent`: The role of the agent best suited to perform this task. You must choose from the list of available agents.
4.  `dependencies`: A list of `task_id`s that must be completed before this task can begin. If there are no dependencies, provide an empty list `[]`.

**Output Format:**
Your final output must be a single, valid JSON object. This object should contain a single key, "plan", which is a list of the task objects you have defined. Do not include any other text, explanations, or apologies before or after the JSON object.

**Example Output:**
{{
  "plan": [
    {{
      "task_id": 1,
      "description": "Design the overall system architecture and data models.",
      "agent": "Architect",
      "dependencies": []
    }},
    {{
      "task_id": 2,
      "description": "Implement the backend API endpoints based on the architecture.",
      "agent": "Backend Developer",
      "dependencies": [1]
    }}
  ]
}}

Now, generate the project plan for the task provided above.
"""

def get_agent_roles_str():
    """Returns the agent roles as a formatted string."""
    return "\n".join(f"- {role}" for role in AGENT_ROLES)

def create_ceo_prompt(user_task):
    """Creates the full prompt for the AI CEO by injecting the task and roles."""
    agent_roles_str = get_agent_roles_str()
    return PROMPT_TEMPLATE.format(agent_roles=agent_roles_str, user_task=user_task)
