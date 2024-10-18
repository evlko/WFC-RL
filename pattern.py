class Pattern:
    def __init__(self, id: int, image_path: str, name: str, weight: int):
        self.id = id
        self.image_path = image_path
        self.name = name
        self.weight = weight
        self.rule_set = None

    def set_rule_set(self, rule_set) -> None:
        self.rule_set = rule_set
