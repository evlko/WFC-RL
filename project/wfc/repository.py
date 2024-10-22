from typing import List, Set

from project.wfc.pattern import Pattern
from project.wfc.special_rules import SpecialRule


class Repository:
    def __init__(self) -> None:
        self.patterns = None

    def register_patterns(self, patterns: List[Pattern]) -> None:
        self.patterns = patterns

    def get_all_patterns(self) -> List[Pattern]:
        return self.patterns

    def get_patterns_by_special_rule(self, rule: str) -> List[Pattern]:
        """Get patterns by a special rule"""
        result = []

        if rule == SpecialRule.ALL.value:
            result = self.patterns

        return result

    def get_patterns_by_tag(self, tag: str) -> List[Pattern]:
        """Get patterns by a tag"""
        result = []

        for pattern in self.patterns:
            if tag in pattern.tags:
                result.append(pattern)

        return result

    def handle_text_rule(self, rule: str):
        if rule in SpecialRule:
            return self.get_patterns_by_special_rule(rule=rule)
        return self.get_patterns_by_tag(tag=rule)

    def get_pattern_by_uid(self, uid: List[int]) -> Pattern:
        """Find one pattern with uid"""
        result = None

        for pattern in self.patterns:
            if pattern.uid == uid:
                result = pattern
                break

        return result


repository = Repository()
