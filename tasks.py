"""Tasks for use with Invoke.

(c) 2021 Calvin Remsburg
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
from invoke import task

# ---------------------------------------------------------------------------
# DOCKER PARAMETERS
# ---------------------------------------------------------------------------
DOCKER_IMG = "ghcr.io/cdot65/pan-os-docker"
DOCKER_TAG = "python"


# ---------------------------------------------------------------------------
# SYSTEM PARAMETERS
# ---------------------------------------------------------------------------
PWD = os.getcwd()


# ---------------------------------------------------------------------------
# DOCKER CONTAINER SHELL
# ---------------------------------------------------------------------------
@task
def shell(context):
    """Access the bash shell within our container."""
    context.run(
        f"docker run -it --rm \
            -v {PWD}/python:/home/python \
            -w /home/python/ \
            {DOCKER_IMG}:{DOCKER_TAG} /bin/sh",
        pty=True,
    )


# ---------------------------------------------------------------------------
# PYTHON REPL
# ---------------------------------------------------------------------------
@task
def python(context):
    """Access the Python REPL within the container."""
    context.run(
        f"docker run -it --rm \
            -v {PWD}/python:/home/python \
            -w /home/python/ \
            {DOCKER_IMG}:{DOCKER_TAG} ipython --profile=paloalto",
        pty=True,
    )
