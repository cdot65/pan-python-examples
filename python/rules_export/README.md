# Panorama Rules Exporter 🚀

This project retrieves a list of security rules from Panorama and their associated Security Profile Groups (if any) and exports the data to a CSV file.

## Table of Contents 📚

- [Panorama Rules Exporter 🚀](#panorama-rules-exporter-)
  - [Table of Contents 📚](#table-of-contents-)
  - [Overview 🌐](#overview-)
  - [Execution ⚙️](#execution-️)
    - [Run Script Locally 🖥️](#run-script-locally-️)
    - [Run Script with Docker 🐳](#run-script-with-docker-)
    - [Examle Output 📄](#examle-output-)
  - [Scheduled Execution 📅](#scheduled-execution-)
  - [Technical Deep Dive 🔎](#technical-deep-dive-)

## Overview 🌐

The Panorama Rules Exporter script connects to a Palo Alto Networks Panorama device, retrieves security rules and their associated Security Profile Groups, and exports the data to a CSV file.

## Execution ⚙️

### Run Script Locally 🖥️

1. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

2. Create a `.env` file in the project directory, using the `.env.example` file as a template. Fill in your Panorama credentials and URL.

3. Run the script:

    ```bash
    python main.py
    ```

### Run Script with Docker 🐳

1. Build the Docker image:

    ```bash
    docker build -t panorama-rules-exporter .
    ```

2. Create a `.env` file in the directory where you want to store the output CSV file. Use the `.env.example` file as a template, and fill in your Panorama credentials and URL.

3. Run the Docker container:

    ```bash
    docker run --rm --env-file /path/to/host/directory/.env -v /path/to/host/directory:/app/output panorama_rules_export
    ```

Replace `/path/to/host/directory` with the path to the directory containing the `.env` file and where you want to save the output CSV file.

### Examle Output 📄

The following is an example of the output CSV file:

| Rule Name                | Security Profile Group |
| ------------------------ | ---------------------- |
| Block Quic               | N/A                    |
| Block Gaming URLs        | ['Outbound']           |
| AD servers               | N/A                    |
| Allow DNS                | N/A                    |
| SSH                      | N/A                    |
| Network Services         | N/A                    |
| Active Directory Inbound | N/A                    |
| k8s api                  | N/A                    |
| k8s nodeports            | N/A                    |
| Ansible EDA permit       | N/A                    |
| LAN Outbound             | ['Outbound']           |
| DMZ Outbound             | ['Outbound']           |

## Scheduled Execution 📅

To set up a scheduled execution using a cron job, follow these steps:

1. Open your crontab file for editing:

    ```bash
    crontab -e
    ```

2. Add a new line to the file, specifying the desired schedule and command to run the script. For example, to run the script every day at midnight, add the following line (replace `/path/to/panorama_rules_export.py` with the actual path to the script file.):

    ```cron
    0 0 * * * /usr/bin/python3 /path/to/panorama_rules_export.py
    ```

3. Save the file and exit the editor.

## Technical Deep Dive 🔎

The Panorama Rules Exporter script consists of the following steps:

1. Load the Panorama credentials and URL from the `.env` file.

2. Connect to the Panorama device.

3. Retrieve the security rules and their associated Security Profile Groups using the `group` attribute.

4. Save the data to a CSV file.

For more details, please refer to the comments within the `panorama_rules_export.py` script file.
