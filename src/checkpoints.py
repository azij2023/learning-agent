# src/checkpoints.py
from pydantic import BaseModel
from typing import List

class Checkpoint(BaseModel):
    topic: str
    objectives: List[str]
    success_criteria: str

def build_checkpoints() -> List[Checkpoint]:
    return [
        Checkpoint(topic="Probability Basics", objectives=["sample space", "events", "probability"], success_criteria=">=70%"),
        Checkpoint(topic="Probability Rules", objectives=["addition rule", "multiplication rule"], success_criteria=">=70%"),
        Checkpoint(topic="Conditional Probability", objectives=["conditional probability", "Bayes theorem"], success_criteria=">=70%"),
        Checkpoint(topic="Random Variables", objectives=["discrete", "continuous"], success_criteria=">=70%"),
        Checkpoint(topic="Distributions I", objectives=["binomial", "poisson"], success_criteria=">=70%"),
        Checkpoint(topic="Distributions II", objectives=["normal distribution"], success_criteria=">=70%"),
        Checkpoint(topic="Expectation & Variance", objectives=["mean", "variance", "std deviation"], success_criteria=">=70%"),
        Checkpoint(topic="Hypothesis Testing", objectives=["null hypothesis", "p-value"], success_criteria=">=70%"),
        Checkpoint(topic="Confidence Intervals", objectives=["interval estimation"], success_criteria=">=70%"),
        Checkpoint(topic="Regression Basics", objectives=["linear regression"], success_criteria=">=70%")
    ]
