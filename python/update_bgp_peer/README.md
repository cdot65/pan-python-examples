# Example of using pan-os-python to update a BGP peer

This script is meant to serve as an educational tool, teaching operators how to work with the pan-os-python Python SDK.

The lines of code below are meant to be typed into a Python REPL, rather than executing as an actual script.

The intention here is to give you the experience of working within the Python SDK, giving you a better understanding.

We have provided a Docker container to work within; this will not only prevent you from having to worry about maintaing packages within a virtual environment, but it will also provide many features to help you get off the ground faster.

Here is a short list of some of the features of the container:

- auto import fundamental packages like xmltodict, ElementTree, and dot_env
- loads your Palo Alto credientials from `.env` file within this repository
- color context to help visualize objects
- ability to `tab` for autocomplete
- history can be viewed by typing `history`
- ability to upload our Python buffer to a pastbin by typing `pastebin`
  - be careful when working with sensitive data!

Do not call TAC support looking for assistance, they will not understand what you're talking about. Instead, open an Issue on GitHub to get my attention.

## Order of operations

Once you have activated your container's Python REPL, follow these steps to complete your task:

### Create an object to represent our instance of Panorama

```python
pan = Panorama(PANURL, PANUSER, PANPASS)
```

### Create an object to represent the template named "BaseTemplate"

```python
template = Template("BaseTemplate")
```

_optional: Retrieve template information from the live Panorama instance_

```python3
template.refresh()
template.about()
```

### Add our template to the Panorama instance object as a child element

```python
pan.add(template)
```

4. Create an object to represent the virtual router instance named "Blue"
5. Add our virtual router instance object to the template
6. Create an object to represent the BGP configuration data model
7. Add our BGP configuration object to the virtual router
8. Create an object to represent the BGP Peer Group named "WAN"
9. Add our BGP Peer Group object to the BGP configuration object
10. Create an object to represent the BGP peer named "ISP1"
11. Add the BGP peer object to the BGP peer group object
12. Update the name of our BGP peer to "ATT MPLS"
13. Apply the new peer config with the `apply()` method.
14. Commit
