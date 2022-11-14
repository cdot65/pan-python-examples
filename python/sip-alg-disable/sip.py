from panos.firewall import Firewall

"""
CLI command: set shared alg-override application sip alg-disabled yes
XML payload:
    <config>
        <shared>
            <alg-override>
                <application>
                    <entry name="sip">
                        <alg-disabled>yes</alg-disabled>
                    </entry>
                </application>
            </alg-override>
        </shared>
    </config>
"""


INVENTORY = ["hdq-vfw-01", "aus-vfw-01"]
PAN_USER = "myusername"
PAN_PASS = "my-super-secret-password"

if __name__ == "__main__":
    pan_user = PAN_USER
    pan_pass = PAN_PASS
    payload = '<entry name="sip"><alg-disabled>yes</alg-disabled></entry>'
    for each in INVENTORY:
        fw = Firewall(each, pan_user, pan_pass)
        fw.xapi.set("/config/shared/alg-override/application", payload)
        fw.commit()
