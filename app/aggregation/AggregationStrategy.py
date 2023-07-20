from abc import ABC, abstractmethod


class AggregationStrategy(ABC):
    @abstractmethod
    def aggregate(self, data):
        pass

    @abstractmethod
    def to_html(self, data, depth=0):
        pass
