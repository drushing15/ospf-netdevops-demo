from genie.testbed import load

def main():
    testbed = load("inventory/testbed.yml")

    for device_name, device in testbed.devices.items():
        print(f"\nConnecting to {device_name}...")
        device.connect(log_stdout=False)

        output = device.execute("show ip ospf neighbor")

        print(f"{device_name} OSPF neighbors:")
        print(output)

        device.disconnect()

if __name__ == "__main__":
    main()

# Future checks:
# 1. Connect to routers
# 2. Run show ip ospf neighbor
# 3. Confirm expected neighbors are FULL
# 4. Run show ip route ospf
# 5. Confirm the new loopback route is learned after Ansible change