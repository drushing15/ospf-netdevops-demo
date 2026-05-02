from genie.testbed import load


EXPECTED_NEIGHBORS = {
    "R1": ["2.2.2.2", "3.3.3.3"],
    "R2": ["1.1.1.1", "4.4.4.4", "5.5.5.5"],
    "R3": ["1.1.1.1"],
    "R4": ["2.2.2.2"],
    "R5": ["2.2.2.2"],
}

EXPECTED_ROUTES = {
    "R1": ["10.30.30.30"],
    "R2": ["10.30.30.30"],
    "R4": ["10.30.30.30"],
    "R5": ["10.30.30.30"]
}

def validate_ospf_neighbors(device_name, ospf_output):
    expected_neighbors = EXPECTED_NEIGHBORS[device_name]

    print(f"\nValidating OSPF neighbors for {device_name}...")

    lines = ospf_output.splitlines()

    for neighbor in expected_neighbors:
        found = False

        for line in lines:
            if neighbor in line:
                found = True
                if "FULL" in line:
                    print(f"PASS: {device_name} has FULL adjacency with {neighbor}")
                else:
                    print(f"FAIL: {device_name} neighbor {neighbor} is not FULL")
                break

        if not found:
            print(f"FAIL: {device_name} is missing neighbor {neighbor}")

def validate_ospf_routes(device_name, route_output):
    print(f"\nValidating OSPF routes for {device_name}...")

    expected_routes = EXPECTED_ROUTES.get(device_name, [])

    if not expected_routes:
        print(f"INFO: {device_name} has no remote OSPF route checks defined")
        return

    for route in expected_routes:
        if route in route_output:
            print(f"PASS: {device_name} learned expected OSPF route {route}")
        else:
            print(f"FAIL: {device_name} is missing expected OSPF route {route}")

def main():
    testbed = load("inventory/testbed.yml")

    for device_name, device in testbed.devices.items():
        print(f"\nConnecting to {device_name}...")
        device.connect(log_stdout=False)

        ospf_output = device.execute("show ip ospf neighbor")

        print(f"{device_name} OSPF neighbors:")
        print(ospf_output)

        validate_ospf_neighbors(device_name, ospf_output)

        route_output = device.execute("show ip route ospf")

        print(f"{device_name} OSPF routes:")
        print(route_output)

        validate_ospf_routes(device_name, route_output)

        device.disconnect()


if __name__ == "__main__":
    main()

# Future checks:
# 1. Connect to routers
# 2. Run show ip ospf neighbor
# 3. Confirm expected neighbors are FULL
# 4. Run show ip route ospf
# 5. Confirm the new loopback route is learned after Ansible change