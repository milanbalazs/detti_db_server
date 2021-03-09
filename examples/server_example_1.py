import os
import sys

# Get the path of the directory of the current file.
PATH_OF_FILE_DIR: str = os.path.realpath(os.path.dirname(__file__))

# Append the path of the tools folder to find modules.
sys.path.append(os.path.join(PATH_OF_FILE_DIR, ".."))

import detti_server  # noqa: E402

print("Starting server")
detti_server.run_server()
