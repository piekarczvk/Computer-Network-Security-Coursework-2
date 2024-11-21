import ipaddress
import sys


class Firewall:
    def __init__(self):
        self.rules = []

    def add_rule(self, rule_num=None, direction="both", addr=None):
        if addr is None:
            print("Error: Address or range must be specified.")
            return

        try:
            if '-' in addr:
                start, end = addr.split('-')
                addr_range = (ipaddress.IPv4Address(start), ipaddress.IPv4Address(end))
            else:
                addr_range = (ipaddress.IPv4Address(addr), ipaddress.IPv4Address(addr))
        except ipaddress.AddressValueError:
            print("Error: Invalid IP address or range.")
            return

        # Check for duplicate rule
        for rule in self.rules:
            if rule["direction"] == direction and rule["addr"] == addr_range:
                print("Error: Duplicate rule.")
                return

        # If no rule number is provided, default to 1
        if rule_num is None:
            rule_num = 1

        # Increment rule numbers of existing rules below the new one
        for rule in self.rules:
            if rule["rule_num"] >= rule_num:
                rule["rule_num"] += 1

        # Add the new rule at the specified position
        new_rule = {"rule_num": rule_num, "direction": direction, "addr": addr_range}
        self.rules.append(new_rule)

        # Sort rules by rule number to maintain correct priority
        self.rules.sort(key=lambda x: x["rule_num"])

        print(f"Rule added: {new_rule}")


    def remove_rule(self, rule_num, direction=None):
        

        for i, rule in enumerate(self.rules):
            if rule["rule_num"] == rule_num:
                if direction and rule["direction"] != "both":
                    if rule["direction"] == direction:
                        self.rules.pop(i)
                        print(f"Rule {rule_num} for direction {direction} removed.")
                        return
                    else:
                        print(f"Error: No rule {rule_num} for direction {direction}.")
                        return
                elif direction:
                    rule["direction"] = "out" if direction == "in" else "in"
                    print(f"Direction {direction} removed from rule {rule_num}.")
                    return
                else:
                    self.rules.pop(i)
                    print(f"Rule {rule_num} removed.")
                    return
        print(f"Error: Rule {rule_num} not found.")

    def list_rules(self, rule_num=None, direction=None, addr=None):
        # check if there are any rules
        if not self.rules:
            print("No rules found.")
            return

        found = False  # check if any rules match
        for rule in self.rules:
            if rule_num and rule["rule_num"] != rule_num:
                continue
            if direction and rule["direction"] != direction and rule["direction"] != "both":
                continue
            if addr:
                try:
                    if '-' in addr:
                        start, end = addr.split('-')
                        target_range = (ipaddress.IPv4Address(start), ipaddress.IPv4Address(end))
                    else:
                        target_range = (ipaddress.IPv4Address(addr), ipaddress.IPv4Address(addr))
                except ipaddress.AddressValueError:
                    print("Error: Invalid IP address or range.")
                    return

                rule_range = rule["addr"]
                if not (rule_range[0] <= target_range[1] and rule_range[1] >= target_range[0]):
                    continue
            found = True
            print(f"Rule {rule['rule_num']}: Direction: {rule['direction']}, Address Range: {rule['addr'][0]}-{rule['addr'][1]}")

        if not found:
            print("No matching rules found.")

  

    def execute(self, command):
        args = command.split()
        if not args:  # check if args is empty
            print("Error: No command entered.")
            return

        if args[0] == "add":
            rule_num = 1
            direction = "both"
            addr = None

            if len(args) < 2:
                print("Error: Insufficient arguments for add command.")
                return

            if args[1].isdigit():
                rule_num = int(args[1])
                args = args[2:]
            else:
                args = args[1:]

            if "-in" in args:
                direction = "in"
                args.remove("-in")
            elif "-out" in args:
                direction = "out"
                args.remove("-out")

            if args:
                addr = args[0]

            self.add_rule(rule_num, direction, addr)

        elif args[0] == "remove":
            if len(args) < 2 or not args[1].isdigit():
                print("Error: Invalid rule number.")
                return

            rule_num = int(args[1])
            direction = None

            if "-in" in args:
                direction = "in"
            elif "-out" in args:
                direction = "out"

            self.remove_rule(rule_num, direction)

        elif args[0] == "list":
            rule_num = None
            direction = None
            addr = None

            if len(args) > 1 and args[1].isdigit():
                rule_num = int(args[1])
                args = args[2:]
            else:
                args = args[1:]

            if "-in" in args:
                direction = "in"
            elif "-out" in args:
                direction = "out"

            for arg in args:
                if arg not in ["-in", "-out"]:
                    addr = arg

            self.list_rules(rule_num, direction, addr)
        else:
            print("Error: Invalid command.")


# Program Main Runner
if __name__ == "__main__":
    fw = Firewall()
    while True:
        try:
            command = input("Enter command: ").strip()
            if command.lower() in ["exit", "quit"]:
                print("Exiting program.")
                break
            fw.execute(command)
        except KeyboardInterrupt:
            print("\nExiting program.")
            break
