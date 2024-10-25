from dataclasses import dataclass, field
from enum import Enum
from typing import List, Union

from project.wfc.direction import Direction, reverse_directions
from project.wfc.pattern import MetaPattern
from project.wfc.special_rules import SpecialRule


class ValidationResult(Enum):
    SUCCESS = "success"
    FAIL = "fail"


@dataclass
class ValidationError:
    pattern_uid: int
    neighbour_uid: int
    direction: Direction


@dataclass
class ValidationMessage:
    result: ValidationResult = ValidationResult.SUCCESS
    error: Union[ValidationError, None] = field(default_factory=list)

    def __str__(self):
        error_str = "\n".join(str(err) for err in self.error)
        error_str = f"Errors {len(self.error)}:\n{error_str}"
        return f"Validation Result: {self.result.value}\n{error_str if len(self.error) > 0 else ''}"

    def __repr__(self):
        return self.__str__()


class Repository:
    def __init__(self) -> None:
        self.patterns = None

    def register_patterns(self, patterns: List[MetaPattern]) -> None:
        self.patterns = patterns

    def validate_patterns(self) -> ValidationMessage:
        message = ValidationMessage()
        for pattern in self.patterns:
            for direction in Direction:
                reverse_direction = reverse_directions[direction]
                direction_neighbours = pattern.rules.get_allowed_neighbors(direction)
                for neighbour in direction_neighbours:
                    if pattern in neighbour.rules.get_allowed_neighbors(
                        reverse_direction
                    ):
                        continue
                    error = ValidationError(
                        pattern_uid=pattern.uid,
                        neighbour_uid=neighbour.uid,
                        direction=direction,
                    )
                    message.error.append(error)
                    message.result = ValidationResult.FAIL
        return message

    def get_all_patterns(self) -> List[MetaPattern]:
        return self.patterns

    def get_patterns_by_special_rule(self, rule: str) -> List[MetaPattern]:
        """Get patterns by a special rule"""
        result = []

        if rule == SpecialRule.ALL.value:
            result = self.patterns

        return result

    def get_patterns_by_tag(self, tag: str) -> List[MetaPattern]:
        """Get patterns by a tag"""
        result = []

        for pattern in self.patterns:
            if tag in pattern.tags:
                result.append(pattern)

        return result

    def handle_text_rule(self, rule: str) -> List[MetaPattern]:
        """Handle text rule: use special rule of just a tag."""
        if rule in SpecialRule:
            return self.get_patterns_by_special_rule(rule=rule)
        return self.get_patterns_by_tag(tag=rule)

    def get_pattern_by_uid(self, uid: List[int]) -> MetaPattern:
        """Find one pattern with uid"""
        result = None

        for pattern in self.patterns:
            if pattern.uid == uid:
                result = pattern
                break

        return result


repository = Repository()
