from aggregation.Aggregator import Aggregator
from aggregation.AggregationStrategy import AggregationStrategy
import importlib
import pkgutil


class AggregationFactory:
    @staticmethod
    def create_strategies():
        strategies = {}
        package_name = "aggregation.strategies"

        for importer, modname, ispkg in pkgutil.iter_modules(importlib.import_module(package_name).__path__):
            module = importlib.import_module(f"{package_name}.{modname}")
            for attr_name, attr_obj in module.__dict__.items():
                if "Aggregation" in attr_name and attr_name != "AggregationStrategy":
                    strategies[attr_name] = Aggregator(strategy=attr_obj())

        return strategies
