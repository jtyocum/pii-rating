#!/usr/bin/env python3
"""PII Rating Tool

This module processes a list of files with their associated PII (Personally Identifiable
Information) types and calculates risk ratings based on a configurable rating scheme.

The input file should contain one entry per line in the format:
    /path/to/file: ["PII_TYPE1", "PII_TYPE2", ...]
    /path/to/notfound: NOTFOUND

The tool outputs the aggregated risk rating counts for each file in JSON format.
"""

import argparse
import json
import tomllib
import sys
from collections import Counter
from pathlib import Path


def lookup_rating(entity_type: str) -> str:
    """Look up the risk rating for a given PII entity type.

    Args:
        entity_type: A string representing the PII entity type (e.g., "US_SSN", "EMAIL_ADDRESS").

    Returns:
        The risk rating as a string ("HIGH", "MEDIUM", "LOW", or "UNKNOWN" if not found).

    The function reads the entity-rating.toml configuration file which maps PII types
    to their risk ratings. If the entity type is not found in the configuration,
    "UNKNOWN" is returned.
    """
    with open("entity-rating.toml", "rb") as f:
        data = tomllib.load(f)

    try:
        return(data['entity_types'][entity_type])
    except:
        return('UNKNOWN')


def main():
    """Process a list of files and output their PII risk ratings.

    This function parses command-line arguments to get the input file path, then
    processes each line to extract file paths and their associated PII types.
    It calculates risk rating counts for each file and prints the results.

    Command-line Arguments:
        list_file: Path to a file containing newline-separated entries with
                   file paths and PII data in JSON format.

    The function handles three cases for each entry:
        1. NOTFOUND: The file was not found during scanning
        2. Empty PII list: No PII was detected in the file
        3. PII types present: Calculates and displays aggregated risk rating counts

    Output format:
        - For NOTFOUND: "{file_path}: NOTFOUND"
        - For no PII: "{file_path}: NONE"
        - For PII found: "{file_path}: {JSON with rating counts}"
        - For errors: "{file_path}: ERROR - {message}"
    """
    parser = argparse.ArgumentParser(
        description="Rate the identified PII types for a list of prescanned files."
    )

    parser.add_argument("list_file", help="Path to a file containing a newline‑separated list of files and their associated PII types")
    args = parser.parse_args()

    try:
        list_path = Path(args.list_file)
        if not list_path.is_file():
            raise FileNotFoundError(f"{list_path} does not exist")
    except Exception as e:
        print(f"Exception: {e}");
        sys.exit(1)

    with open(list_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Split on the first colon to separate file path from PII data
            parts = line.split(': ', 1)
            if len(parts) != 2:
                continue

            file_path, pii_data = parts

            # Check if file was not found
            if pii_data == "NOTFOUND":
                print(f"{file_path}: NOTFOUND")
                continue

            # Parse the JSON list of PII types
            try:
                pii_types = json.loads(pii_data)

                # Handle empty list (no PII found)
                if not pii_types:
                    print(f"{file_path}: NONE")
                    continue

                # Lookup ratings for each PII type and count them
                ratings = [lookup_rating(pii_type) for pii_type in pii_types]
                rating_counts = Counter(ratings)

                # Print the result
                print(f"{file_path}: {json.dumps(dict(rating_counts))}")

            except json.JSONDecodeError:
                print(f"{file_path}: ERROR - Could not parse PII data")

if __name__ == "__main__":
    main()
