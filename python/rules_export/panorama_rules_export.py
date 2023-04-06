"""Export security rules and associated Security Profile Groups to a CSV file.

This script will retrieve a list of security rules from Panorama and their
associated Security Profile Groups (if any) and output the data to a CSV file.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

(c) 2023 Calvin Remsburg
"""
# standard library imports
import os
import csv
import logging
from typing import List, Tuple

# third party library imports
from dotenv import load_dotenv

# Palo Alto Networks imports
from panos import panorama
from panos.policies import PreRulebase, PostRulebase, SecurityRule


# ----------------------------------------------------------------------------
# Load environment variables from .env file
# ----------------------------------------------------------------------------
load_dotenv(".env")
PANURL = os.environ.get("PANURL", "panorama.lab.com")
PANUSER = os.environ.get("PANUSER", "automation")
PANPASS = os.environ.get("PANPASS", "mysecretpassword")
OUTPUT_FILE = 'panorama_rules.csv'


# ----------------------------------------------------------------------------
# Connect to Panorama
# ----------------------------------------------------------------------------
pan = panorama.Panorama(PANURL, PANUSER, PANPASS)


# ----------------------------------------------------------------------------
# Function to retrieve security rules and associated Security Profile Groups
# ----------------------------------------------------------------------------
def get_security_rules_and_profiles(pan: panorama.Panorama) -> List[Tuple[str, str]]:
    """
    Retrieve security rules and their associated Security Profile Groups.

    Args:
        pan: An instance of Panorama.

    Returns:
        A list of tuples, each containing the rule name and its associated
        Security Profile Group (or 'N/A' if no group is associated).
    """
    # Create Pre Rulebase and Post Rulebase instances
    pre_rulebase = PreRulebase()
    post_rulebase = PostRulebase()

    # Add Pre Rulebase and Post Rulebase to the Panorama instance
    pan.add(pre_rulebase)
    pan.add(post_rulebase)

    # Retrieve Pre Rules and Post Rules
    pre_rules = SecurityRule.refreshall(pre_rulebase)
    post_rules = SecurityRule.refreshall(post_rulebase)

    # Combine Pre Rules and Post Rules
    rules = pre_rules + post_rules

    # Prepare data
    data = []
    for rule in rules:
        security_profile_group = rule.group
        data.append((rule.name, security_profile_group if security_profile_group else 'N/A'))

    return data


# ----------------------------------------------------------------------------
# Function to save data to a CSV file
# ----------------------------------------------------------------------------
def save_to_csv(data: List[Tuple[str, str]], filename: str) -> None:
    """
    Save the given data to a CSV file.

    Args:
        data: A list of tuples to save to the CSV file.
        filename: The name of the CSV file to save the data to.
    """
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['RuleName', 'SecurityProfileGroup'])
        writer.writerows(data)


# ----------------------------------------------------------------------------
# Function to get the output filepath
# ----------------------------------------------------------------------------
def get_output_filepath(filename: str) -> str:
    """
    Get the output filepath for the given filename.

    Args:
        filename: The name of the file.

    Returns:
        A string representing the output filepath.
    """
    return os.path.join(os.getcwd(), filename)


# ----------------------------------------------------------------------------
# Configure logging
# ----------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')


# ----------------------------------------------------------------------------
# Main execution of our script
# ----------------------------------------------------------------------------
def main() -> None:
    try:
        # Get security rules and associated Security Profile Groups
        data = get_security_rules_and_profiles(pan)
    except Exception as e:
        logging.error(f"Error retrieving security rules: {e}")
        return

    # Get the output filepath
    output_filepath = get_output_filepath(OUTPUT_FILE)

    try:
        # Save the data to a CSV file
        save_to_csv(data, output_filepath)
    except Exception as e:
        logging.error(f"Error saving data to CSV file: {e}")
        return

    logging.info(f'Exported to {output_filepath}')


# ----------------------------------------------------------------------------
# Execute main function
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
