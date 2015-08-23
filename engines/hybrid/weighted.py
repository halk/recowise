from collections import OrderedDict
from core.engine.hybrid import HybridEngine as ParentHybridEngine

class HybridEngine(ParentHybridEngine):
    def recommend(self, body):
        data = self.translate(body)
        limit = data['limit'] if 'limit' in data else False
        return self.merge(self.apply_weight(self.get_results(body)), limit)

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
                weight = float(self.settings['weight'][component])
                for recommendation, score in result.iteritems():
                    results[component][recommendation] = score * weight
        print results
        return results

    def merge(self, results, limit=False):
        merged = OrderedDict()
        for result in results.itervalues():
            for recommendation, score in result.iteritems():
                if recommendation in merged and merged[recommendation] >= score:
                    continue

                merged[recommendation] = score

        # this drops the scores, so no needs to call .keys() afterwards
        sorted_results = sorted(merged, key=merged.__getitem__, reverse=True)

        if limit != False:
            return sorted_results[:int(limit)]

        return sorted_results
