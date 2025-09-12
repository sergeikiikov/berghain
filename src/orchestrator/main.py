import time
from typing import List, Dict, Any

# Import the placeholder agent modules
from src.agents import architect, backend_developer, frontend_developer, qa_engineer, devops_engineer

class Orchestrator:
    """
    The Orchestrator class manages the execution of a project plan.
    It dispatches tasks to the appropriate agents based on dependencies.
    """
    def __init__(self, plan: List[Dict[str, Any]]):
        self.plan = plan
        self.task_states: Dict[int, str] = {} # task_id -> "pending" | "ready" | "in_progress" | "completed" | "failed"

        # A registry to map agent roles to their execution modules
        self.agent_registry = {
            "Architect": architect,
            "Backend Developer": backend_developer,
            "Frontend Developer": frontend_developer,
            "QA Engineer": qa_engineer,
            "DevOps Engineer": devops_engineer,
        }
        self._initialize_tasks()

    def _initialize_tasks(self):
        """Sets the initial state of all tasks to 'pending'."""
        for task in self.plan:
            self.task_states[task['task_id']] = "pending"

    def _get_ready_tasks(self) -> List[Dict[str, Any]]:
        """
        Identifies tasks that are ready to be executed.
        A task is ready if it is 'pending' and all its dependencies are 'completed'.
        """
        ready_tasks = []
        for task in self.plan:
            if self.task_states[task['task_id']] == "pending":
                dependencies = task.get('dependencies', [])
                if not dependencies or all(self.task_states.get(dep_id) == "completed" for dep_id in dependencies):
                    ready_tasks.append(task)
        return ready_tasks

    def execute_plan(self):
        """
        Runs the main execution loop for the project plan.
        """
        print("\n--- Starting Project Execution ---")
        completed_tasks_count = 0

        while completed_tasks_count < len(self.plan):
            ready_tasks = self._get_ready_tasks()

            if not ready_tasks:
                # Check for circular dependencies or failed states if no tasks are ready but plan is not complete
                if any(status not in ["completed", "failed"] for status in self.task_states.values()):
                    print("No tasks are ready to run. Waiting... (or potential deadlock)")
                    time.sleep(2) # Wait before re-checking
                    # In a real system, you'd have more sophisticated deadlock detection
                else:
                    break # All tasks are done or failed

            for task in ready_tasks:
                task_id = task['task_id']
                agent_role = task['agent']

                print(f"\nDispatching Task {task_id} to {agent_role}...")
                self.task_states[task_id] = "in_progress"

                agent_module = self.agent_registry.get(agent_role)
                if not agent_module:
                    print(f"Error: Agent '{agent_role}' not found in registry.")
                    self.task_states[task_id] = "failed"
                    continue

                try:
                    # Dispatch the task to the agent's execute function
                    success = agent_module.execute(task['description'])
                    if success:
                        self.task_states[task_id] = "completed"
                        completed_tasks_count += 1
                        print(f"Task {task_id} completed successfully.")
                    else:
                        self.task_states[task_id] = "failed"
                        print(f"Task {task_id} failed.")
                except Exception as e:
                    print(f"An error occurred while executing Task {task_id}: {e}")
                    self.task_states[task_id] = "failed"

        print("\n--- Project Execution Finished ---")
        print("Final Task States:")
        for task_id, status in self.task_states.items():
            print(f"  Task {task_id}: {status}")
