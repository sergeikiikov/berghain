import os
import json
from ai_ceo.src.agent import create_ceo_prompt
# In a real scenario, you would use the openai library.
# For this example, we will mock the LLM response.
# from openai import OpenAI
# from dotenv import load_dotenv

def get_llm_response(prompt: str) -> str:
    """
    Simulates a call to an LLM.

    In a real implementation, this function would use the OpenAI client
    to send the prompt and receive a response. For now, it returns a
    hardcoded JSON string that mimics the expected output for the task
    "Add a blog to our company website."
    """
    print("--- PROMPT SENT TO MOCK LLM ---")
    print(prompt)
    print("---------------------------------")

    # This is a mocked response for demonstration purposes.
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
    Generates a project plan for a given task.
    """
    # Step 1: Create the prompt for the AI CEO
    prompt = create_ceo_prompt(task)

    # Step 2: Get the response from the (mock) LLM
    llm_output = get_llm_response(prompt)

    # Step 3: Parse the JSON response
    try:
        plan_data = json.loads(llm_output)
        return plan_data
    except json.JSONDecodeError:
        print("Error: The LLM output was not valid JSON.")
        return None

def main_cli():
    """
    The main command-line interface loop for the AI CEO.
    """
    print("--- AI CEO Interface ---")
    print("Enter a task for the AI CEO to plan. Type 'exit' or 'quit' to end.")

    while True:
        user_task = input("\nYour Task > ")
        if user_task.lower() in ["exit", "quit"]:
            print("Exiting. Goodbye!")
            break

        if not user_task:
            continue

        print(f"\nGenerating plan for task: '{user_task}'...")
        generated_plan = generate_plan(user_task)

        if generated_plan and "plan" in generated_plan:
            print("\n--- GENERATED PROJECT PLAN ---")
            # Pretty print the plan
            for task in generated_plan["plan"]:
                print(f"  Task ID: {task['task_id']}")
                print(f"    Description: {task['description']}")
                print(f"    Agent: {task['agent']}")
                print(f"    Dependencies: {task['dependencies']}")
                print("-" * 20)
        else:
            print("Sorry, I couldn't generate a plan for that task.")

if __name__ == "__main__":
    main_cli()
