# Securing your secrets

Please make sure to manage your sensative information carfully.

While the modules support the ability to pass in secret information in clear text, this should never be done in a production environment.

Below are some safer alternatives to storing sensative information.

## Manage your credientials as an environmentals

```sh
export PANOS_USERNAME=bigbird
export PANOS_PASSWORD=sesamestree123
export PANORAMA_API_TOKEN=supersecrettoken123
```

## Using Ansible Vault

Create a file to store your secret information, this will serve as our Ansible Vault.

! The file name does not need to be called `vault.yaml`, like in my example. Feel free to name it what you will, but it should be in a YAML data structure.

`$ vim vault.yaml`

```yaml
panos_username: bigbird
panos_password: sesamestree123
panorama_api_token: supersecrettoken123
```

### Working with your Ansible Vault

An Ansible Vault is a regular YAML file that is encrypted after it was created in clear text.

To perform the encryption, type in the following:

```bash
ansible-vault encrypt vault.yaml
```

To view the encrypted file contents, type in this command and follow it with your password when prompted:

```bash
ansible-vault view vault.yaml
```

If you would like to edit the encrypted file contents, type in this command; the file will automatically encrypt once it is saved.

```bash
ansible-vault edit vault.yaml
```

If you would like to decrypt a file, simply type the following:

```bash
ansible-vault decrypt vault.yaml
```

### Bringing your Ansible Vault into your playbook

Ansible will not magically guess when a new secrets file has created for your playbook, so you have three methods of getting your vault used by your playbook.

#### Import your vault file into the play

Update your playbook to import your vault with `vars_files` argument. This needs to happen at the play level, not within the tasks.

```yaml
---
- hosts: localhost
  vars_files:
    - vault.yml
  tasks:
    ...
```

#### Storing your vault in `group_vars`

If your Ansible vault lives within the directory of `group_vars`, Ansible will automatically import it at runtime. Simple and effective.

```bash
$ tree -C
.
├── ansible
│   ├── ansible.cfg
│   ├── group_vars
│   │   └── all
│   │       └── vault.yaml
│   └── hello.yaml
...
```

### Running your playbook with Ansible Vault

Make sure to always throw the `--ask-vault-pass` flag when calling your playbook.

```bash
ansible-playbook --ask-vault-pass test.yaml
```
