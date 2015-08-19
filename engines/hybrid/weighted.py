from collections import OrderedDict
from core.engine.hybrid import HybridEngine as ParentHybridEngine

class HybridEngine(ParentHybridEngine):
    def recommend(self, body):
        return self.merge(self.apply_weight(self.get_results(body)))

    def get_results(self, body):
        results = {}
        for name, component in self.components.iteritems():
            result = component.recommend(body, True)
            if result:
                results[name] = result

        return results

    def apply_weight(self, results):
        if 'weight' not in self.settings:
            return results

        for component, result in results.iteritems():
            if component in self.settings['weight']:
                weight = self.settings['weight'][component]
                for recommendation, score in result.iteritems():
                    results[component][recommendation] = score * weight

        return results

    def merge(self, results):
        merged = OrderedDict()
        for result in results.itervalues():
            for recommendation, score in result.iteritems():
                if recommendation in merged and merged[recommendation] >= score:
                    continue

                merged[recommendation] = score

        # this drops the scores, so no needs to call .keys() afterwards
        return sorted(merged, key=merged.__getitem__, reverse=True)
