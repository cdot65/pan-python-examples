"""
------------------------------------------------------------------------------
Example of using pan-os-python to update a BGP peer.
------------------------------------------------------------------------------

This script is meant to serve as an educational tool, teaching operators how
to work with the pan-os-python Python SDK.

The lines of code below are meant to be typed into a Python REPL, rather than
executing as an actual script. The intention here is to give you the
experience of working within the Python SDK, giving you a better understanding.

We have provided a Docker container to work within; this will not only prevent
you from having to worry about maintaing packages within a virtual environment,
but it will also provide many features to help you get off the ground faster.

Here is a short list of some of the features of the container:

- auto import fundamental packages like xmltodict, ElementTree, and dot_env
- loads your Palo Alto credientials from `.env` file within this repository
- color context to help visualize objects
- ability to `tab` for autocomplete
- history can be viewed by typing `history`
- ability to upload our Python buffer to a pastbin by typing `pastebin`
  - be careful when working with sensitive data!

Do not call TAC support looking for assistance, they will not understand
what you're talking about. Instead, open an Issue on GitHub to get my
attention.

(c) 2022 Calvin Remsburg
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

from panos.panorama import Panorama, Template, PanoramaCommit, PanoramaCommitAll
from panos.network import VirtualRouter, Bgp, BgpPeerGroup, BgpPeer


pan = Panorama(PANURL, PANUSER, PANPASS)

template = Template("BaseTemplate")
pan.add(template)
template.refresh()
template.about()

vr = VirtualRouter("Blue")
template.add(vr)
vr.refresh()
vr.about()

bgp = Bgp()
vr.add(bgp)
bgp.refresh()
bgp.about()

pg = BgpPeerGroup("WAN")
bgp.add(pg)
pg.refresh()
pg.about()

peer = BgpPeer("ISP1")
pg.add(peer)
peer.refresh()
peer.about()
peer.name = "ATT MPLS"
peer.apply()

pan_commit = PanoramaCommit("updated fron pan-os-docker", ["automation"])
commit_job = pan.commit(cmd=pan_commit)

# create a object called 'job_complete' and set it to False for now
job_complete = False

# while the job_complete object is set to False (default), perform this task
while not job_complete:
    # check in on the status of our job, storing the XML byte response
    response = pan.op(cmd=f'show jobs id "{commit_job}"', xml=True)
    # convert the XML byte response object to a Python dictionary
    job_as_dict = xmltodict.parse(response)
    job = job_as_dict["response"]["result"]["job"]
    # check in on status of commit job, report back to screen
    if job["id"] == str(commit_job):
        if job["type"] == "Commit":
            if job["progress"] == "100":
                if job["status"] == "FIN":
                    if job["result"] == "OK":
                        print("[DEBUG] Job Finished, 100 Percent and Results are OK")
                        job_complete = True
                        break
                    else:
                        print(
                            "[DEBUG] Job Finished, 100 Percent and Results are not OK: %s "
                            % job["result"]
                        )
                else:
                    print(
                        "[DEBUG] Job progress is 100 Percent but status is not FIN: %s "
                        % job["status"]
                    )
            else:
                print(
                    "[DEBUG] Job progress is not 100 Percent yet ... %s "
                    % job["progress"]
                )
        else:
            print("[DEBUG] Job is not a COMMIT job : %s " % job["type"])
    if not job_complete:
        time.sleep(5)

    job = job_as_dict["result"]["job"]

old_peer = BgpPeer("ISP1")
pg.add(old_peer)
old_peer.delete()

# create a commit object with our description and admin user as a list
pan_commit = PanoramaCommit("pushed from pan-os-docker", ["automation"])

# pass our commit object into the commit method of our panorama instance
commit_job = pan.commit(cmd=pan_commit)

# create a object called 'job_complete' and set it to False for now
job_complete = False

# while the job_complete object is set to False (default), perform this task
while not job_complete:
    # check in on the status of our job, storing the XML byte response
    response = pan.op(cmd=f'show jobs id "{commit_job}"', xml=True)
    # convert the XML byte response object to a Python dictionary
    job_as_dict = xmltodict.parse(response)
    job = job_as_dict["response"]["result"]["job"]
    # check in on status of commit job, report back to screen
    if job["id"] == str(commit_job):
        if job["type"] == "Commit":
            if job["progress"] == "100":
                if job["status"] == "FIN":
                    if job["result"] == "OK":
                        print("[DEBUG] Job Finished, 100 Percent and Results are OK")
                        job_complete = True
                        break
                    else:
                        print(
                            "[DEBUG] Job Finished, 100 Percent and Results are not OK: %s "
                            % job["result"]
                        )
                else:
                    print(
                        "[DEBUG] Job progress is 100 Percent but status is not FIN: %s "
                        % job["status"]
                    )
            else:
                print(
                    "[DEBUG] Job progress is not 100 Percent yet ... %s "
                    % job["progress"]
                )
        else:
            print("[DEBUG] Job is not a COMMIT job : %s " % job["type"])
    if not job_complete:
        time.sleep(5)

    job = job_as_dict["result"]["job"]

# create an empty list and beging to iterate over our device groups
jobs = []
for dg in ["branch", "headquarters"]:
    # create a commit object, passing in the style and device group name
    dg_commit = PanoramaCommitAll("device group", dg)
    # send our commit operation to Panorama and store the job id
    job_id = pan.commit(cmd=dg_commit)
    # append our job id to the `jobs` list created above.
    jobs.append(job_id)

print(jobs)

# create a commit object with our description and admin user as a list
pan_commit = PanoramaCommit("pushed from pan-os-docker", ["automation"])

# pass our commit object into the commit method of our panorama instance
commit_job = pan.commit(cmd=pan_commit)

# create a object called 'job_complete' and set it to False for now
job_complete = False

# while the job_complete object is set to False (default), perform this task
while not job_complete:
    # check in on the status of our job, storing the XML byte response
    response = pan.op(cmd=f'show jobs id "{commit_job}"', xml=True)
    # convert the XML byte response object to a Python dictionary
    job_as_dict = xmltodict.parse(response)
    job = job_as_dict["response"]["result"]["job"]
    # check in on status of commit job, report back to screen
    if job["id"] == str(commit_job):
        if job["type"] == "Commit":
            if job["progress"] == "100":
                if job["status"] == "FIN":
                    if job["result"] == "OK":
                        print("[DEBUG] Job Finished, 100 Percent and Results are OK")
                        job_complete = True
                        break
                    else:
                        print(
                            "[DEBUG] Job Finished, 100 Percent and Results are not OK: %s "
                            % job["result"]
                        )
                else:
                    print(
                        "[DEBUG] Job progress is 100 Percent but status is not FIN: %s "
                        % job["status"]
                    )
            else:
                print(
                    "[DEBUG] Job progress is not 100 Percent yet ... %s "
                    % job["progress"]
                )
        else:
            print("[DEBUG] Job is not a COMMIT job : %s " % job["type"])
    if not job_complete:
        time.sleep(5)

    job = job_as_dict["result"]["job"]

# create an empty list and beging to iterate over our device groups
jobs = []
for dg in ["branch", "headquarters"]:
    # create a commit object, passing in the style and device group name
    dg_commit = PanoramaCommitAll("device group", dg)
    # send our commit operation to Panorama and store the job id
    job_id = pan.commit(cmd=dg_commit)
    # append our job id to the `jobs` list created above.
    jobs.append(job_id)

print(jobs)

# create an empty list and beging to iterate over our device groups
jobs = []
for dg in ["branch", "headquarters"]:
    # create a commit object, passing in the style and device group name
    dg_commit = PanoramaCommitAll("device group", dg)
    # send our commit operation to Panorama and store the job id
    job_id = pan.commit(cmd=dg_commit)
    # append our job id to the `jobs` list created above.
    jobs.append(job_id)

print(jobs)
response = pan.op(cmd=f'show jobs id "{jobs[0]}"', xml=True)
job_as_dict = xmltodict.parse(response)
job = job_as_dict["response"]["result"]["job"]
job
response = pan.op(cmd=f'show jobs id "{jobs[0]}"', xml=True)
job_as_dict = xmltodict.parse(response)
job = job_as_dict["response"]["result"]["job"]
job
response = pan.op(cmd=f'show jobs id "{jobs[1]}"', xml=True)
job_as_dict = xmltodict.parse(response)
job = job_as_dict["response"]["result"]["job"]
job
