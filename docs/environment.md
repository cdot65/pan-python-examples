# Setting up your environment

There are two paths you can go down to set up your environment:

1. Using Docker containers.
2. Using Python Virtual Environments.

## Using Docker containers

If you are unsure if Docker is installed on your computer, then it's probably safe to suggest that it's not. If you're interested in learning more about the product, I encourage you to read a few blogs on the topic. A personal recommendation would be [digital ocean](https://www.digitalocean.com/community/tutorial_collections/how-to-install-and-use-docker).

Some of the goodies placed in the `docker` folder are not relevant to our use case with Python. Feel free to delete them as you see fit, I simply wanted to share with you my Docker build process for all automation projects (including those based on Ansible). The world is your oyster and I won't judge you on whatever direction you take.

### Invoke

If you have [invoke](https://pypi.org/project/invoke/) installed, you can use these two commands to build the container and run the playbook.

### Build the container

If you have [invoke](https://pypi.org/project/invoke/) installed, you can use these two commands to build the container and jump into an instance of the container image.

```bash
invoke build
invoke shell
```

#### Execute the playbook within the running container

This playbook is expected to be ran in Ansible AWX, so many of the elements in the playbook are stored as variables. We will need to pass in values for these objects when we run our playbook

```bash
ansible-playbook hello.yaml'
```

### Without Invoke

```bash
docker build -t automation:paloalto docker/
docker run -it \
    --rm \
    --env-file $(pwd)/docker/.env \
    -v $(pwd)/ansible/:/home/ansible \
    -w /home/ansible/ \
    automation:paloalto ansible-playbook hello.yaml \
    -i inventory.yaml \
    -e device_name=Richmond-fw1
```

## Using Python Virtual Environments

### With Poetry installed

I have included a `poetry`_ file for anyone saavy enough to take advantage. For the uninitiated, Poetry helps replicate Python environments between users with a single file. You'll need to have [Poetry installed on your machine](https://python-poetry.org/docs/), for most users that will be solved with `pip install poetry`.

Create your Python virtual environment:

```bash
poetry install
```

Activate your Python virtual environment:

```bash
poetry shell
```

### Without Poetry installed

Always, always, always strive to use virtual environments when working with Python. If you're needing a quick overview or refresher on Python virtual environments:

[Digital Ocean (macOS)](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-macos)
[Digital Ocean (Windows 10)](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-windows-10)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r docker/requirements.txt
```

### Install Palo Alto Networks's Ansible Collection

This is a one-time setup and should be skipped in additional playbook executions.

We will change into the directory containing our Ansible files, run our Ansible Galaxy install command to install the Ansible modules from Galaxy.

```bash
ansible-galaxy collection install paloaltonetworks.panos
```

### Execute playbook

Execute the playbook, making sure to reference the inventory file for our environment in another directory.

```bash
ansible-playbook hello.yaml
```

## Inventory

Our inventory is found at `ansible/inventory.yaml`, please update to reflect your own environment

```yaml
---
all:
  children:
    firewalls:
      hosts:
        hdq-vfw-01:
        aus-vfw-01:
```

There is a top level group called `all`, which we will be calling in our playbook.

We create our own group called `firewalls`, and embed the hosts `hdq-vfw-01` and `aus-vfw-01` within it.

You can bypass DNS resolution by declaring `ansible_host` key with the value of the static IP at the host level.

```yaml
---
all:
  children:
    firewalls:
      hosts:
        hdq-vfw-01:
          ansible_host: "10.0.0.1"
        aus-vfw-01:
```
