from genie.testbed import load


EXPECTED_NEIGHBORS = {
    "R1": ["2.2.2.2", "3.3.3.3"],
    "R2": ["1.1.1.1", "4.4.4.4", "5.5.5.5"],
    "R3": ["1.1.1.1"],
    "R4": ["2.2.2.2"],
    "R5": ["2.2.2.2"],
}


def validate_ospf_neighbors(device_name, ospf_output):
    expected_neighbors = EXPECTED_NEIGHBORS[device_name]

    print(f"\nValidating OSPF neighbors for {device_name}...")

    for neighbor in expected_neighbors:
        if neighbor in ospf_output and "FULL" in ospf_output:
            print(f"PASS: {device_name} has FULL adjacency with {neighbor}")
        else:
            print(f"FAIL: {device_name} is missing FULL adjacency with {neighbor}")


def main():
    testbed = load("inventory/testbed.yml")

    for device_name, device in testbed.devices.items():
        print(f"\nConnecting to {device_name}...")
        device.connect(log_stdout=False)

        ospf_output = device.execute("show ip ospf neighbor")

        print(f"{device_name} OSPF neighbors:")
        print(ospf_output)

        validate_ospf_neighbors(device_name, ospf_output)

        device.disconnect()


if __name__ == "__main__":
    main()

# Future checks:
# 1. Connect to routers
# 2. Run show ip ospf neighbor
# 3. Confirm expected neighbors are FULL
# 4. Run show ip route ospf
# 5. Confirm the new loopback route is learned after Ansible change