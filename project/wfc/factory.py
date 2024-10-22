import json
from typing import List

from project.wfc.pattern import Pattern
from project.wfc.repository import repository
from project.wfc.rules import NeighborRuleSet


class Factory:
    def __init__(self, json_path: str):
        with open(json_path, "r") as f:
            self.data = json.load(f)["patterns"]

    def create_patterns(self):
        """Creates patterns and rules from JSON data"""
        patterns_data = {p["id"]: p for p in self.data}
        patterns = [
            Pattern(
                uid=pattern_data["id"],
                image_path=pattern_data["image_path"],
                name=pattern_data["name"],
                tags=set(pattern_data["tags"]),
                weight=pattern_data["weight"],
            )
            for pattern_data in self.data
        ]

        repository.register_patterns(patterns)

        for pattern in patterns:
            rules = self.create_rules(patterns_data[pattern.uid]["rules"])
            pattern.rules = rules

        return patterns

    def create_rules(self, rules) -> NeighborRuleSet:
        """Create a NeighborRuleSet based on the JSON rules"""

        def rules_handler(options: List[str | int]):
            results = []
            for op in options:
                if isinstance(op, str):
                    results += repository.handle_text_rule(op)
                else:
                    results += [repository.get_pattern_by_uid(op)]
            return results

        return NeighborRuleSet(
            allowed_up=rules_handler(rules.get("up", [])),
            allowed_down=rules_handler(rules.get("down", [])),
            allowed_left=rules_handler(rules.get("left", [])),
            allowed_right=rules_handler(rules.get("right", [])),
        )
