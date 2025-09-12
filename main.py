import os
import json

# Updated imports for the new project structure
from src.ceo.agent import create_ceo_prompt
from src.orchestrator.main import Orchestrator

# For now, we will continue to mock the LLM response.
def get_llm_response(prompt: str) -> str:
    """
    Simulates a call to an LLM.
    Returns a hardcoded JSON string that mimics the expected output.
    """
    print("--- [CEO] PROMPT SENT TO MOCK LLM ---")
    # print(prompt) # The prompt is very long, so we can hide it for cleaner output
    print("--- [CEO] MOCK RESPONSE RECEIVED ---")

    mock_response = {
        "plan": [
            {
                "task_id": 1,
                "description": "Design the data models for blog posts, comments, and users. Define the API endpoints.",
                "agent": "Architect",
                "dependencies": []
            },
            {
                "task_id": 2,
                "description": "Implement the database schemas and API endpoints based on the Architect's design.",
                "agent": "Backend Developer",
                "dependencies": [1]
            },
            {
                "task_id": 3,
                "description": "Build the UI components for displaying blog posts and handling user comments.",
                "agent": "Frontend Developer",
                "dependencies": [1]
            },
            {
                "task_id": 4,
                "description": "Write and execute tests for the entire blog feature (API and UI).",
                "agent": "QA Engineer",
                "dependencies": [2, 3]
            },
            {
                "task_id": 5,
                "description": "Deploy the new blog feature to production.",
                "agent": "DevOps Engineer",
                "dependencies": [4]
            }
        ]
    }
    return json.dumps(mock_response, indent=2)

def generate_plan(task: str):
    """
    Generates a project plan for a given task using the AI CEO.
    """
    prompt = create_ceo_prompt(task)
    llm_output = get_llm_response(prompt)

    try:
        plan_data = json.loads(llm_output)
        return plan_data
    except json.JSONDecodeError:
        print("Error: The CEO output was not valid JSON.")
        return None

def main_cli():
    """
    The main command-line interface loop for the application.
    """
    print("--- Multi-Agent AI Coding Assistant ---")
    print("Enter a task for the AI CEO to plan and execute. Type 'exit' or 'quit' to end.")

    while True:
        user_task = input("\nYour Task > ")
        if user_task.lower() in ["exit", "quit"]:
            print("Exiting. Goodbye!")
            break

        if not user_task:
            continue

        # Step 1: Get the plan from the AI CEO
        print(f"\n[CEO] Generating plan for task: '{user_task}'...")
        plan_json = generate_plan(user_task)

        if not plan_json or "plan" not in plan_json:
            print("Sorry, the AI CEO could not generate a plan for that task.")
            continue

        print("[CEO] Plan generated successfully.")

        # Step 2: Hand the plan to the Orchestrator to execute
        orchestrator = Orchestrator(plan=plan_json["plan"])
        orchestrator.execute_plan()

        print("\n--- Task execution complete. Ready for new task. ---")


if __name__ == "__main__":
    main_cli()
