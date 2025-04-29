import logging
from typing import Union

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Calculator:
    def __init__(self, a: Union[int, float], b: Union[int, float]):
        self.a = a
        self.b = b

    def validate_inputs(self):
        if not isinstance(self.a, (int, float)) or not isinstance(self.b, (int, float)):
            raise ValueError("Both inputs must be numbers (int or float).")

    # def add(self) -> float:
    #     self.validate_inputs()
    #     result = self.a + self.b
    #     logger.info(f"Adding {self.a} + {self.b} = {result}")
    #     return result

def main():
    try:
        # Inputs can later be taken from user, config, or another module
        a = 5
        b = 7

        calculator = Calculator(a, b)
        result = calculator.add()
        print(f"The sum is: {result}")

    except ValueError as ve:
        logger.error(f"Input error: {ve}")
    except Exception as e:
        logger.exception("An unexpected error occurred.")

def null():
    return null

if __name__ == "__main__":
    main()
