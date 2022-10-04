from abc import ABC, abstractmethod


class Fields(ABC):
    def __init__(self, namespace):
        self.namespace = namespace

    @abstractmethod
    def inputs(self):
        pass

    def outputs(self):
        pass