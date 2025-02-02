import os
import sys
from datetime import date
from functools import wraps

from src.libs.utils.default import DefaultParameters


def create_tensorboard_log_dir(type_of_algorithm: str = "Test",
                               algorithm_used: str = "Test"):
    """type_of_algorithm: DL or ML
    || algorithm_used: CNN, RNN or transformers for DL or LINEAR or MLP for ML
    || Every parameter are set by default to "Test"."""

    def decorator(function):
        @wraps(function)
        def wrapper(path: str = None, *args):
            if path is None:
                # Relative path from this file to tensorboard log directory
                base_dir_logs = os.path.dirname(os.path.realpath("__file__"))
                print(base_dir_logs)

                # Create a path file name with date and other variables
                experiment_dir_logs = f"{date.today().strftime('%d%m%Y')}" \
                                      f"_bs_{DefaultParameters.batch_size}" \
                                      f"_lr_{DefaultParameters.learning_rate}" \
                                      f"_mom_{DefaultParameters.momentum}" \
                                      f"_hl_{DefaultParameters.num_hidden_layers}" \
                                      f"_nphl_{DefaultParameters.num_neurons_per_hidden_layers}"

                dirs = [f"{base_dir_logs}",
                        f"{base_dir_logs}/{type_of_algorithm}",
                        f"{base_dir_logs}/{type_of_algorithm}/{algorithm_used}",
                        f"{base_dir_logs}/{type_of_algorithm}/{algorithm_used}/{experiment_dir_logs}"]

                # Creating every dirs that doesn't exist yet
                for dir in dirs:
                    if not os.path.isdir(dir):
                        os.mkdir(dir)

            return function(path=dirs[3], *args)

        return wrapper

    return decorator


@create_tensorboard_log_dir(type_of_algorithm="how_to_use")
def how_to_use(path: str = None) -> None:
    print(f"Path created at : {path}")


if __name__ == "__main__":
    how_to_use()
