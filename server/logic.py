import random
from typing import Optional, Dict, Any
from pydantic import BaseModel

class NewsAction(BaseModel):
    action_type: str  
    query_or_label: str

class NewsObservation(BaseModel):
    headline: str
    evidence: str
    steps_left: int

class FakeNewsLogic:
    def __init__(self):
        # IDs are task-1, task-2, task-3 for Meta Validator
        self.task_data = {
            "task-1": {
                "headline": "NASA confirms the Moon is made of 100% Swiss Cheese.",
                "label": "false",
                "base_evidence": "Basic planetary science contradicts this.",
                "search_results": "Scientific journals confirm Moon is made of rock and metal."
            },
            "task-2": {
                "headline": "New government policy: All citizens to receive 1000 units of currency tomorrow.",
                "label": "true",
                "base_evidence": "Social media rumors are circulating.",
                "search_results": "Official Government Gazette Vol 42 confirms the 'Economic Stimulus Act'."
            },
            "task-3": {
                "headline": "Study shows drinking coffee leads to immediate 20% increase in IQ.",
                "label": "false",
                "base_evidence": "A viral blog post claims this study is revolutionary.",
                "search_results": "Original study found temporary alertness, not IQ increase."
            }
        }
        self.reset("task-1")

    def reset(self, task_id: str = None) -> NewsObservation:
        # Fallback to random task if ID is missing or wrong
        if not task_id or task_id not in self.task_data:
            task_id = random.choice(list(self.task_data.keys()))
            
        self.current_task_id = task_id
        self.current_task = self.task_data[task_id]
        self.collected_evidence = self.current_task["base_evidence"]
        self.steps_left = 5
        self.done = False
        
        return self._get_obs()

    def step(self, action: NewsAction):
        if self.done:
            return self._get_obs(), 0.05, True, {"score": 0.05}

        self.steps_left -= 1
        reward = 0.05 # Default small reward to avoid 0.0
        
        if action.action_type == "search":
            # Reward for gathering evidence
            if self.collected_evidence == self.current_task["base_evidence"]:
                reward = 0.15
                self.collected_evidence = self.current_task["search_results"]
            else:
                reward = 0.08
            
        elif action.action_type == "verify":
            self.done = True
            # Check answer
            if action.query_or_label.strip().lower() == self.current_task["label"].lower():
                reward = 0.95 # Success (strictly < 1)
            else:
                reward = 0.05 # Failure (strictly > 0)
        
        if self.steps_left <= 0:
            self.done = True
            
        # IMPORTANT: Return 4 values and include "score" in info dict
        return self._get_obs(), float(reward), self.done, {"score": float(reward)}

    def _get_obs(self) -> NewsObservation:
        return NewsObservation(
            headline=self.current_task["headline"],
            evidence=self.collected_evidence,
            steps_left=self.steps_left
        )
