"""Search for instances of address objects.

This script will locate all instances of an AddressObject within
the firewall's configuration.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

(c) 2022 Calvin Remsburg
"""
# standard library imports
import os

# third party library imports
import argparse
import pandas as pd
from tabulate import tabulate
from dotenv import load_dotenv

# Palo Alto Networks imports
from panos.panorama import Panorama, DeviceGroup
from panos.objects import AddressObject, AddressGroup

# ----------------------------------------------------------------------------
# Look in our .env file on our computer to locate our credientials
# ----------------------------------------------------------------------------
load_dotenv(".env")
PANURL = os.environ.get("PANURL", "panorama.lab")
PANUSER = os.environ.get("PANUSER", "automation")
PANPASS = os.environ.get("PANPASS", "mysecretpassword")
pan = Panorama(PANURL, PANUSER, PANPASS)


# ----------------------------------------------------------------------------
# Function to grab Panorama configuration objects
# ----------------------------------------------------------------------------
def grab_config():
    """
    Description: collect configuration objects from Panorama.
    Workflow:
        1. Pull in various components of a Panorama configuration.
            - Device Groups
            - Address Groups
            - Address Objects
        2. Identify all address objects and append them to "address_objects"
        3. Identify all address groups and append them to "address_groups"
        4. Loop over device groups and perform steps 2 & 3 again.
    Return:
        - name: address_groups
          type: tuple
        - name: address_objects
          type: tuple
    """

    # load Panorama configuration objects
    pan_address_objects = AddressObject.refreshall(pan)
    pan_address_groups = AddressGroup.refreshall(pan)

    # create empty placeholders
    address_objects = []
    address_groups = []

    # append shared config address objects
    for each in pan_address_objects:
        address_objects.append(("Shared", each.name, each.value, each.type))

    # append shared config address groups
    for each in pan_address_groups:
        if each.static_value:
            if not each.description:
                each.description = ""
            address_groups.append(
                ("Shared", each.name, each.description, each.static_value)
            )

    # pull down list of device groups
    device_groups = DeviceGroup.refreshall(pan)

    # loop over device groups and perform the same actions
    for dg in device_groups:

        # start with address objects
        dg_address_objects = AddressObject.refreshall(dg)
        for each in dg_address_objects:
            address_objects.append((dg.name, each.name, each.value, each.type))

        # finish with address groups
        dg_address_groups = AddressGroup.refreshall(dg)
        for each in dg_address_groups:
            if each.static_value:
                if not each.description:
                    each.description = ""
                address_groups.append(
                    (dg.name, each.name, each.description, each.static_value)
                )

    # return our address_groups and address_objects to the main function
    return address_groups, address_objects


# ----------------------------------------------------------------------------
# Function to map associations between address objects and their parent groups
# ----------------------------------------------------------------------------
def find_matches(address_groups, address_objects, search):
    """
    Description: Find all associations of an address object.
    Workflow:
        1. Loop over our address_objects and update `match` when the prefix is matched.
        2. Use the match's object name to see if it resides in an address_group object.
        3. Repeat for of the address group name to see if it's nested in another group.
    Return:
        - name: associations
          type: list
    """

    # create a placeholder for our potential match
    match = {}

    # loop over the address objects, update our match object if value is found
    for each in address_objects:
        if search in each:
            match["source"] = each[0]
            match["name"] = each[1]

    # if no match was found, return message to user
    if "name" in match:

        # create a placeholder for our potential groups
        associations = []

        # loop over the address groups
        for each in address_groups:

            # if there is a positive match, then update our associations object
            if match["name"] in each[3]:
                associations.append(each)

        # let's finally loop over our associations object to see if a group is nested
        for each in associations:

            # loop over our address_groups object again, looking to find a match
            for group in address_groups:

                # append when we see the name of our address group matched in another address group
                if each[1] in group[3]:
                    associations.append(group)

        return associations

    else:
        return None


# ----------------------------------------------------------------------------
# Main execution of our script
# ----------------------------------------------------------------------------
def main():
    """
    Description: Main execution of our script.
    Workflow:
        1. Retrieve the prefix passed as an argument from the user
        2. Call the `grab_config` function to retrieve configuration objects
        3. Pass our prefix and lists objects into `find_matches`
        4. Print result to console
    """
    # create instance of argparse, asking for `--prefix` to be passed at run
    parser = argparse.ArgumentParser()
    parser.add_argument("--prefix", type=str, required=True)
    args = parser.parse_args()

    # inform user that a search is taking place
    print(f"Searching for instances of {args.prefix}")

    # pull in our configuration objects
    address_groups, address_objects = grab_config()

    # find all associations of the prefix
    associations = find_matches(address_groups, address_objects, args.prefix)

    # determine if the search was successful
    if associations:
        # create a pandas dataframe and print to the console.
        df = pd.DataFrame(associations)
        print(tabulate(df, headers="keys", tablefmt="fancy_outline"))
    else:
        print(f"no match was found for {args.prefix}")


# ----------------------------------------------------------------------------
# Execute main function
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
