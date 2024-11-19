
from abc import ABC, abstractmethod
from typing import List
from .workflow_step import WorkflowStep

class Workflow(ABC):
    def __init__(self) -> None:
        self.steps: List[WorkflowStep]

    