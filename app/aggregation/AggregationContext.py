from aggregation.AggregationStrategy import AggregationStrategy


class AggregationContext:
    def __init__(self, strategy: AggregationStrategy):
        self._strategy = strategy

    def execute(self, data):
        aggregated = self._strategy.aggregate(data)
        html = self._strategy.to_html(aggregated)
        return aggregated, html
