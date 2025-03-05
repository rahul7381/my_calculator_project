import importlib
import pkgutil
import logging
from abc import ABC, abstractmethod
from dotenv import load_dotenv
import os

# ✅ Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")

# ✅ Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Logs to a file
        logging.StreamHandler()  # Logs to console
    ]
)

logger = logging.getLogger(__name__)
logger.info("Calculator application started.")

# ✅ Command Interface
class Command(ABC):
    @abstractmethod
    def execute(self, *args):
        pass

# ✅ Concrete Command Classes
class AddCommand(Command):
    def execute(self, *args):
        try:
            if not args:
                return 0  # ✅ Fix for empty input case
            result = sum(float(num) for num in args)
            logger.info(f"Executed AddCommand with args {args}, result: {result}")
            return result
        except ValueError:
            logger.error(f"Invalid input for addition: {args}")
            return "Error: Invalid input"

class SubtractCommand(Command):
    def execute(self, *args):
        try:
            if not args:
                return "Error: Invalid input"  # ✅ Fix for empty input case
            numbers = list(map(float, args))
            result = numbers[0] - sum(numbers[1:])
            logger.info(f"Executed SubtractCommand with args {args}, result: {result}")
            return result
        except ValueError:
            logger.error(f"Invalid input for subtraction: {args}")
            return "Error: Invalid input"

class MultiplyCommand(Command):
    def execute(self, *args):
        try:
            if not args:
                return 1  # ✅ Fix for empty input case
            result = 1.0
            for num in map(float, args):
                result *= num
            logger.info(f"Executed MultiplyCommand with args {args}, result: {result}")
            return result
        except ValueError:
            logger.error(f"Invalid input for multiplication: {args}")
            return "Error: Invalid input"

class DivideCommand(Command):
    def execute(self, *args):
        try:
            if not args:
                return "Error: Invalid input"  # ✅ Fix for empty input case
            numbers = list(map(float, args))
            if len(numbers) == 1:
                return "Error: Division requires at least two numbers"
            result = numbers[0]
            for num in numbers[1:]:
                if num == 0:
                    logger.error("Division by zero attempted")
                    return "Error: Division by zero"
                result /= num
            logger.info(f"Executed DivideCommand with args {args}, result: {result}")
            return result
        except ValueError:
            logger.error(f"Invalid input for division: {args}")
            return "Error: Invalid input"

# ✅ Plugin Loader
class PluginLoader:
    def __init__(self, plugin_package):
        self.plugin_package = plugin_package
        self.commands = {}
        self.load_plugins()

    def load_plugins(self):
        """Dynamically loads plugins from the plugins directory."""
        try:
            package = importlib.import_module(self.plugin_package)
            for _, module_name, _ in pkgutil.iter_modules(package.__path__):
                module = importlib.import_module(f"{self.plugin_package}.{module_name}")
                if hasattr(module, "COMMANDS"):
                    self.commands.update(module.COMMANDS)
                    logger.info(f"Loaded plugin: {module_name}")
        except ModuleNotFoundError:
            logger.warning(f"Plugin package '{self.plugin_package}' not found.")
        except Exception as e:
            logger.error(f"Error loading plugins: {e}")

# ✅ Load Plugins
def load_dynamic_commands():
    plugin_loader = PluginLoader("plugins")
    return plugin_loader.commands

# ✅ Command Dictionary
commands = {
    "add": AddCommand(),
    "subtract": SubtractCommand(),
    "multiply": MultiplyCommand(),
    "divide": DivideCommand(),
}

# ✅ Integrate dynamic commands
commands.update(load_dynamic_commands())

# ✅ REPL Function
def repl():
    print("Welcome to the Command Pattern Calculator! Type 'menu' to see available commands, or 'exit' to quit.")
    while True:
        try:
            user_input = input("Enter command: ").strip().split()
            if not user_input:
                continue  # ✅ Fix for empty input case (100% test coverage)

            command_name = user_input[0]
            args = user_input[1:]

            if command_name == "exit":
                print("Exiting calculator. Goodbye!")
                logger.info("User exited the calculator.")
                break
            elif command_name == "menu":
                print("Available commands:", ", ".join(sorted(commands.keys())))
            elif command_name in commands:
                print("Result:", commands[command_name].execute(*args))
            else:
                print("Invalid command. Type 'menu' to see available commands.")
        except KeyboardInterrupt:
            print("\nExiting calculator. Goodbye!")
            logger.info("Calculator exited via KeyboardInterrupt.")
            break

# ✅ Main Execution
if __name__ == "__main__":
    repl()

