import json
import os
import subprocess
import sys
from distutils.util import strtobool

KAGGLE_DIR_NAME = "notebook-deep-learning"
KAGGLE_DIR_SUBMISSION = "./kaggle/working/submission.csv"
KAGGLE_COMPETITION_NAME = "goodreads-books-reviews-290312"
KAGGLE_MESSAGE = "Submission"


def read_json(path):
    with open(path) as f:
        return json.load(f)


def to_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True)


def run_shell(command, verbose=True):
    print("Executing:", command)
    p = subprocess.Popen(
        [command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    stdout, stderr = p.communicate()

    stdout = stdout.decode("utf-8")
    stderr = stderr.decode("utf-8")  # stderr contains warnings

    if p.returncode != os.EX_OK:
        print("Return code:", p.returncode)
        print(stdout)
        print(stderr)
        raise sys.exit(p.returncode)

    if verbose:
        if stdout != "":
            print(stdout)

        if stderr != "":
            print(stderr)

    return p.returncode


def is_empty(x):
    return x.strip() == ""


def is_comment(x):
    return x.lstrip().startswith("#")


def get_action_input(name):
    # NOTE: When `default` is not given in `action.yml`,
    # action input value will be "" (empty string)
    return os.getenv(f"INPUT_{name.upper()}")


def to_list(s):
    return [x for x in s.strip().split("\n") if not is_empty(x) and not is_comment(x)]


def to_bool(s):
    return strtobool(s) == 1


def get_input_schema():
    return {
        "metadata_file": str,
        "id": str,
        "title": str,
        "code_file": str,
        "language": str,
        "kernel_type": str,
        "is_private": to_bool,
        "enable_gpu": to_bool,
        "enable_internet": to_bool,
        "dataset_sources": to_list,
        "competition_sources": to_list,
        "kernel_sources": to_list,
    }


def parse_action_inputs(input_schema):
    inputs = {}

    for key, cast in input_schema.items():
        val = get_action_input(key)
        inputs[key] = cast(val)

    return inputs


def main():
    action_inputs = parse_action_inputs(get_input_schema())
    meta_file = action_inputs.pop("metadata_file")
    use_meta = meta_file != ""
    meta = read_json(meta_file) if use_meta else action_inputs

    if use_meta:
        for key, val in action_inputs.items():
            if (val == "") or (key in meta):
                continue

            meta.update({key: val})

    code_file = meta["code_file"]
    file_name = os.path.basename(code_file)

    if use_meta:
        # `code_file` is a relative path from the directory where `meta_file` exists
        meta_dir = os.path.dirname(meta_file)
        code_file = os.path.join(meta_dir, file_name)
    else:
        meta["code_file"] = file_name

    # Push the kernel to Kaggle.
    run_shell(f"kaggle kernels push")
    run_shell(f'kaggle kernels status {KAGGLE_DIR_NAME}')
    #run_shell(f'kaggle competitions submit -c {KAGGLE_COMPETITION_NAME} -f {KAGGLE_DIR_SUBMISSION} -m {KAGGLE_MESSAGE}')


if __name__ == "__main__":
    main()
