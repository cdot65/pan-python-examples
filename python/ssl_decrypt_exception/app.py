import requests

hostname = "panorama.redtail.com"
new_entry = "<entry name='*.asdf.com'><exclude>yes</exclude><description>This is a test</description></entry>"
xpath = "/config/devices/entry[@name='localhost.localdomain']/template/entry[@name='Network']/config/shared/ssl-decrypt/ssl-exclude-cert"

endpoint = (
    f"https://{hostname}/api/?type=config&action=set&xpath={xpath}&element={new_entry}"
)

headers = {
    "X-PAN-KEY": "MYSUPERSECRETAPITOKEN",
}

response = requests.request("GET", endpoint, headers=headers, verify=False)

print(response.text)
