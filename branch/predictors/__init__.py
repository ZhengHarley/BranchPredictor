class Predict:
    NOT_TAKEN = 0
    TAKEN = 1


class AbstractBasePredictor:
    def __init__(self, **kwargs):
        pass

    def predict(self, opcode: str, current_pc: int, target_pc: int) -> Predict:
        raise NotImplementedError

    def update(self, opcode: str, current_pc: int, target_pc: int, result: Predict):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError

    @classmethod
    def name(cls):
        return cls.__name__
