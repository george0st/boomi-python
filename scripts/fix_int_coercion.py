#!/usr/bin/env python3
"""Add int() coercion to response_status_code and number_of_results assignments.

XML API responses return these fields as strings. The SDK models declare them as
int but never coerce the incoming value, so downstream code that does arithmetic
or comparisons against an int can break silently.

This script wraps the bare assignments with int() casts:
    self.response_status_code = response_status_code
    ->  self.response_status_code = int(response_status_code)

    self.number_of_results = number_of_results
    ->  self.number_of_results = int(number_of_results)

Targets: all *_async_response.py files, async_operation_token_result.py,
and release_integration_pack_status.py in src/boomi/models/.
"""

import glob
import os
import re

MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'src', 'boomi', 'models')


def fix_file(filepath):
    """Add int() casts to response_status_code and number_of_results assignments.

    Returns 'modified', 'already_fixed', or 'skipped'.
    """
    with open(filepath, 'r') as f:
        content = f.read()

    original = content

    # Idempotency guard: skip if int() casts are already present
    if 'int(response_status_code)' in content or 'int(number_of_results)' in content:
        return 'already_fixed'

    # Check if the file has any of the target assignments
    has_rsc = re.search(
        r'^ +self\.response_status_code = response_status_code$',
        content,
        flags=re.MULTILINE,
    )
    has_nor = re.search(
        r'^ +self\.number_of_results = number_of_results$',
        content,
        flags=re.MULTILINE,
    )

    if not has_rsc and not has_nor:
        return 'skipped'

    # Wrap response_status_code assignment with int()
    content = re.sub(
        r'^( +)(self\.response_status_code) = response_status_code$',
        r'\1\2 = int(response_status_code)',
        content,
        flags=re.MULTILINE,
    )

    # Wrap number_of_results assignment with int()
    content = re.sub(
        r'^( +)(self\.number_of_results) = number_of_results$',
        r'\1\2 = int(number_of_results)',
        content,
        flags=re.MULTILINE,
    )

    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        return 'modified'
    return 'skipped'


def main():
    modified = []
    already_fixed = []
    skipped = []
    errors = []

    # 1. Fix all *_async_response.py files
    pattern = os.path.join(MODEL_DIR, '*_async_response.py')
    files = sorted(glob.glob(pattern))
    print(f"Found {len(files)} async response files")

    for filepath in files:
        basename = os.path.basename(filepath)
        try:
            result = fix_file(filepath)
            if result == 'modified':
                print(f"  Fixed: {basename}")
                modified.append(basename)
            elif result == 'already_fixed':
                print(f"  Already fixed: {basename}")
                already_fixed.append(basename)
            else:
                print(f"  Skipped (no match): {basename}")
                skipped.append(basename)
        except Exception as e:
            print(f"  Error: {basename}: {e}")
            errors.append(basename)

    # 2. Fix AsyncOperationTokenResult
    extra_files = [
        os.path.join(MODEL_DIR, 'async_operation_token_result.py'),
        os.path.join(MODEL_DIR, 'release_integration_pack_status.py'),
    ]
    for filepath in extra_files:
        if not os.path.exists(filepath):
            continue
        basename = os.path.basename(filepath)
        try:
            result = fix_file(filepath)
            if result == 'modified':
                print(f"  Fixed: {basename}")
                modified.append(basename)
            elif result == 'already_fixed':
                print(f"  Already fixed: {basename}")
                already_fixed.append(basename)
            else:
                print(f"  Skipped (no match): {basename}")
                skipped.append(basename)
        except Exception as e:
            print(f"  Error: {basename}: {e}")
            errors.append(basename)

    print(f"\nSummary:")
    print(f"  Modified: {len(modified)}")
    print(f"  Already fixed: {len(already_fixed)}")
    print(f"  Skipped: {len(skipped)}")
    print(f"  Errors: {len(errors)}")


if __name__ == '__main__':
    main()
