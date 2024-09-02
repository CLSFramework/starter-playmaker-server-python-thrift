from abc import ABC, abstractmethod
from src.IAgent import IAgent


class IDecisionMaker(ABC):
    @abstractmethod
    def make_decision(self, agent: IAgent):
        pass
