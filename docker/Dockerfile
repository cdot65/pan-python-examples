FROM python:3.10-alpine

# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------
LABEL name="ghcr.io/cdot65/pan-automation"
LABEL maintainer="cremsburg.dev@gmail.com"
LABEL description="Ansible container to automate Palo Alto Networks products."
LABEL license="Apache 2.0"
LABEL url="https://github.com/cdot65/pan-automation-container"
LABEL build-date="20220927"

# ---------------------------------------------------------------------------
# Add and install python packages
# ---------------------------------------------------------------------------
ADD requirements.txt /var/tmp/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /var/tmp/requirements.txt

# ---------------------------------------------------------------------------
# Install Ansible Galaxy collections
# ---------------------------------------------------------------------------
RUN ansible-galaxy collection install paloaltonetworks.panos

### ---------------------------------------------------------------------------
### Ansible Config
### ---------------------------------------------------------------------------
ENV ANSIBLE_CONFIG /etc/ansible/ansible.cfg

# ---------------------------------------------------------------------------
# Change directory to /home/ansible
# ---------------------------------------------------------------------------
WORKDIR /home/ansible
