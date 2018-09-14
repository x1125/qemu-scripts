QEMU-Scripts for mouse/keyboard attach/detach
=============================================

# Install
* Copy to /opt/qemu-scripts
* Create python virtual env within qemu-scripts (python3 -m venv venv)
* Install systemd service (cp qemu-scripts.service /etc/systemd/system/multi-user.target.wants)
* Start/enable service (systemctl {start,enable} qemu-scripts)

# Config
Set vendor and product id in keyboard.xml and mouse.xml.

# Usage
Visit http://localhost:8000/ and use the buttons to attach or detach devices.
Use the host ip address when within guest vm.
