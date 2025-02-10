from . import AbstractBasePredictor, Predict


class Custom(AbstractBasePredictor):
    """
    Implement your own branch predictor. It can be as simple or complex as you'd like, either novel (your own idea) or
    taken from a research paper (must be cited). Justify the logic of the implementation and provide results compared
    to the others. Why does it work or not work? What are there tradeoffs your predictor has compared to the others
    (size, complexity, accuracy, etc...)?

    -------------
    Describe your logic here (cite if necessary) and implement below. Be sure to discuss your predictor in your write-up
    -------------
    """
    def __init__(self, **kwargs):
        super().__init__()
        raise NotImplementedError("You must implement this predictor's initialization behavior")  # TODO

    def predict(self, opcode: str, current_pc: int, target_pc: int) -> Predict:
        raise NotImplementedError("You must implement this predictor's predict behavior")  # TODO

    def update(self, opcode: str, current_pc: int, target_pc: int, result: Predict):
        raise NotImplementedError("You must implement this predictor's update behavior")  # TODO

    def reset(self):
        raise NotImplementedError("You must implement this predictor's reset behavior")  # TODO
