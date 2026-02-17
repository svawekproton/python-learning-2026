import csv
import os
import json
import argparse

# Constants
DEFAULT_DOMAIN = "gmail.com"


def read_csv_file(filepath):
    """Read CSV and return list of user dictionaries"""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"CSV file not found: {filepath}")

    users = []
    with open(filepath, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if "name" not in row or "email" not in row:
                print(f"Warning: Skipping invalid row: {row}")
                continue
            users.append(row)

    return users


def filter_by_domain(users, domain):
    """Filter users by email domain"""
    if not domain.startswith("@"):
        domain = f"@{domain}"
    return [user for user in users if user["email"].endswith(domain)]


def sort_by_name(users):
    """Sort users alphabetically by name"""
    return sorted(users, key=lambda user: user["name"])


def convert_to_json(data, indent=2):
    """Convert data to formatted JSON string"""
    return json.dumps(data, indent=indent, ensure_ascii=False)


def save_json_to_file(json_string, filepath):
    """Save JSON string to file"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(json_string)


def main(domain=None):
    """Main execution flow"""
    # Setup paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "users.csv")
    output_file = os.path.join(script_dir, "output.json")

    domain = domain or DEFAULT_DOMAIN

    try:
        # Read CSV
        users = read_csv_file(input_file)
        print(f"Read {len(users)} users from CSV")

        # Filter by domain
        filtered_users = filter_by_domain(users, domain)
        print(f"Filtered to {len(filtered_users)} @{domain} users")

        # Sort by name
        sorted_users = sort_by_name(filtered_users)
        print("Sorted users alphabetically")

        # Convert to JSON
        json_output = convert_to_json(sorted_users)

        # Print to console
        print("Filtered and sorted users:")
        print(json_output)

        # Save to file
        save_json_to_file(json_output, output_file)
        print(f"Saved results to {output_file}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CSV processor")
    parser.add_argument(
        "--domain",
        metavar="DOMAIN",
        default=None,
        help="Email domain to filter (e.g., gmail.com, yahoo.com). Default: gmail.com",
    )
    args = parser.parse_args()
    main(args.domain)
