import sys
from genie.testbed import load


EXPECTED_NEIGHBORS = {
    "R1": ["2.2.2.2", "3.3.3.3"],
    "R2": ["1.1.1.1", "4.4.4.4", "5.5.5.5"],
    "R3": ["1.1.1.1"],
    "R4": ["2.2.2.2"],
    "R5": ["2.2.2.2"],
}

LOOPBACK_ROUTE = "10.30.30.30"
REMOTE_ROUTERS = ["R1", "R2", "R4", "R5"]

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

def validate_ospf_routes(device_name, route_output, mode):
    print(f"\nValidating OSPF routes for {device_name}...")

    if "O" in route_output:
        print(f"PASS: {device_name} has OSPF routes installed")
    else:
        print(f"FAIL: {device_name} has no OSPF routes")

    if device_name not in REMOTE_ROUTERS:
        print(f"INFO: {device_name} is the source router for Loopback30")
        return

    route_exists = LOOPBACK_ROUTE in route_output

    if mode == "pre":
        if not route_exists:
            print(f"PASS: {device_name} does not have {LOOPBACK_ROUTE} before change")
        else:
            print(f"FAIL: {device_name} already has {LOOPBACK_ROUTE} before change")

    elif mode == "post":
        if route_exists:
            print(f"PASS: {device_name} learned expected route {LOOPBACK_ROUTE} after change")
        else:
            print(f"FAIL: {device_name} is missing expected route {LOOPBACK_ROUTE} after change")

def main():

    if len(sys.argv) != 2:

        print("Usage: python3 tests/validate_ospf.py <pre|post>")

        sys.exit(1)

    mode = sys.argv[1]

    if mode not in ["pre", "post"]:

        print("Invalid mode. Use 'pre' or 'post'.")

        sys.exit(1)

    print(f"Running OSPF validation in {mode.upper()} mode")

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

        validate_ospf_routes(device_name, route_output, mode)

        device.disconnect()


if __name__ == "__main__":
    main()

# Future checks:
# 1. Connect to routers
# 2. Run show ip ospf neighbor
# 3. Confirm expected neighbors are FULL
# 4. Run show ip route ospf
# 5. Confirm the new loopback route is learned after Ansible change