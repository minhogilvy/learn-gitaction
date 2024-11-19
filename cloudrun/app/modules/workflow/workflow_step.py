from typing import List, TypeVar, Generic

T = TypeVar('T')

class WorkflowStep(Generic[T]):
  def __init__(self, body: T) -> None:
    self.id = None
    self.session_id = None