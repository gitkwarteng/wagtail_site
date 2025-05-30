from django.db.models import F

from .models import ProductRecord


class Calculator(object):

    # Map of field name to weight
    weights = {
        'num_views': 1,
        'num_basket_additions': 3,
        'num_purchases': 5
    }

    def __init__(self, logger):
        self.logger = logger

    def run(self):
        self.calculate_scores()

    def calculate_scores(self):
        self.logger.info("Calculating product scores")
        total_weight = float(sum(self.weights.values()))
        weighted_fields = [
            self.weights[name] * F(name) for name in self.weights.keys()]
        ProductRecord.objects.update(
            score=sum(weighted_fields) / total_weight)
