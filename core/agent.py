from core.logger import log_event
from core.evaluator import evaluate_step_success
from core.goal_evaluator import evaluate_goal

class Agent:
    def __init__(self, llm_client, planner, executor, memory, replanner=None, max_subgoal_retries=2):
        self.llm = llm_client
        self.planner = planner
        self.executor = executor
        self.memory = memory
        self.replanner = replanner
        self.max_subgoal_retries = max_subgoal_retries

    def run(self, user_input: str):
        memory_facts = self.memory.get("user_preferences", {})
        plan = self.planner.create_plan(user_input, memory_facts)
        log_event({"type": "plan_generated", "input": user_input, "plan": plan})

        full_trace = []
        subgoal_results = []

        for sg_index, subgoal in enumerate(plan):
            sg_name = subgoal.get("subgoal", f"subgoal_{sg_index}")
            steps = subgoal.get("steps", [])
            retries_left = self.max_subgoal_retries
            success = False
            failed_step_record = None
            sg_trace = []  # Initialize here to prevent undefined variable errors

            while retries_left >= 0 and not success:
                sg_trace = []
                sg_failed = False
                failed_step_record = None

                for step_index, step in enumerate(steps):
                    action = step.get("action")
                    args = step.get("input", {})

                    if action == "respond":
                        final_answer = step.get("response", "No response provided.")
                        log_event({"type": "final_response", "subgoal": sg_name, "response": final_answer, "trace": full_trace})
                        goal_result = evaluate_goal(user_input, full_trace)
                        log_event({"type": "goal_evaluation", "goal_result": goal_result, "trace": full_trace})
                        return final_answer

                    if action in self.executor.tools:
                        result = self.executor.run(action, args)
                        status = evaluate_step_success(action, args, result)

                        step_record = {
                            "subgoal": sg_name,
                            "step": step_index,
                            "tool": action,
                            "args": args,
                            "result": result,
                            "status": status
                        }
                        sg_trace.append(step_record)
                        full_trace.append(step_record)

                        log_event({"type": "step", "subgoal": sg_name, "tool": action, "result": result, "status": status})

                        if status == "failed":
                            sg_failed = True
                            failed_step_record = step_record
                            break

                if not sg_failed:
                    success = True
                    subgoal_results.append({"subgoal": sg_name, "status": "success", "trace": sg_trace})
                    log_event({"type": "subgoal_complete", "subgoal": sg_name, "status": "success"})
                else:
                    if self.replanner and retries_left > 0 and failed_step_record:
                        error_msg = failed_step_record.get("result", "Unknown error")
                        new_steps = self.replanner.replan_subgoal(subgoal, failed_step_record, error_msg, memory_facts)
                        if new_steps:
                            steps = new_steps
                            log_event({"type": "subgoal_replanned", "subgoal": sg_name, "new_steps": new_steps, "retries_left": retries_left-1})
                            retries_left -= 1
                            continue
                        else:
                            log_event({"type": "subgoal_replan_failed", "subgoal": sg_name})
                            break
                    else:
                        break

            if not success:
                subgoal_results.append({"subgoal": sg_name, "status": "failed", "trace": sg_trace})
                log_event({"type": "subgoal_complete", "subgoal": sg_name, "status": "failed"})
                # Fail fast: stop on first failed subgoal
                break

        goal_result = evaluate_goal(user_input, full_trace)
        log_event({"type": "goal_evaluation", "goal_result": goal_result, "subgoals": subgoal_results})
        return "Execution completed with failures. Check logs."
