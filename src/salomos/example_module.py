class ExampleModule:
    @staticmethod
    def greet(name):
        return f"Hello, {name}!"

    class MathOperations:
        @staticmethod
        def multiply(*args):
            result = 1
            for arg in args:
                result *= float(arg)
            return result
