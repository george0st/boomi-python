#!/usr/bin/env python3
"""BUG-09 extension: Make required positional args optional in async response models.

BUG-09 fixed PersistedProcessPropertiesAsyncResponse, but 12+ other models have
the same vulnerability: `response_status_code: int` as a required positional arg
that crashes on sparse API payloads. This script applies the same fix pattern.

Also fixes AsyncOperationTokenResult which has two required positional args.
"""

import glob
import re
import os

MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'src', 'boomi', 'models')


def fix_async_response_file(filepath):
    """Fix standard *_async_response.py files.

    Pattern: response_status_code: int, -> response_status_code: int = SENTINEL,
    Plus: self.response_status_code = response_status_code -> guarded assignment
    """
    with open(filepath, 'r') as f:
        content = f.read()

    original = content

    # Skip already-fixed files (have = SENTINEL on response_status_code)
    if re.search(r'response_status_code: int = SENTINEL', content):
        return False

    # Skip files that don't have the required positional pattern
    if not re.search(r'response_status_code: int[,)]', content):
        return False

    # 1. Add = SENTINEL default to response_status_code in __init__ signature
    content = re.sub(
        r'response_status_code: int,',
        'response_status_code: int = SENTINEL,',
        content,
    )
    # Handle case where it's the last param before **kwargs (no trailing comma before newline)
    content = re.sub(
        r'response_status_code: int\)',
        'response_status_code: int = SENTINEL)',
        content,
    )

    # 2. Wrap unconditional self.response_status_code = ... in guard
    # Variant A: plain assignment
    content = re.sub(
        r'^( {8})(self\.response_status_code = response_status_code)\n',
        r'\1if response_status_code is not SENTINEL:\n\1    \2\n',
        content,
        flags=re.MULTILINE,
    )
    # Variant B: int() wrapping (seen in ListenerStatusAsyncResponse)
    content = re.sub(
        r'^( {8})self\.response_status_code = int\(response_status_code\)\n',
        r'\1if response_status_code is not SENTINEL:\n\1    self.response_status_code = response_status_code\n',
        content,
        flags=re.MULTILINE,
    )

    # 3. Update docstrings
    content = re.sub(
        r':param response_status_code: (.*)\n( *):type response_status_code: int\n',
        r':param response_status_code: \1, defaults to None\n\2:type response_status_code: int, optional\n',
        content,
    )

    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False


def fix_async_operation_token_result(filepath):
    """Fix AsyncOperationTokenResult which has two required positional args:
    async_token: AsyncToken and response_status_code: int.
    """
    with open(filepath, 'r') as f:
        content = f.read()

    original = content

    # Skip if already fixed
    if 'SENTINEL' in content:
        return False

    # 1. Add SENTINEL import
    content = content.replace(
        'from .utils.base_model import BaseModel',
        'from .utils.base_model import BaseModel\nfrom .utils.sentinel import SENTINEL',
    )

    # 2. Fix __init__ signature - make both args optional
    content = re.sub(
        r'def __init__\(self, async_token: AsyncToken, response_status_code: int, \*\*kwargs\)',
        'def __init__(self, async_token: AsyncToken = SENTINEL, response_status_code: int = SENTINEL, **kwargs)',
        content,
    )

    # 3. Wrap unconditional assignments in guards
    content = re.sub(
        r'^( {8})(self\.async_token = self\._define_object\(async_token, AsyncToken\))\n',
        r'\1if async_token is not SENTINEL:\n\1    \2\n',
        content,
        flags=re.MULTILINE,
    )
    content = re.sub(
        r'^( {8})(self\.response_status_code = response_status_code)\n',
        r'\1if response_status_code is not SENTINEL:\n\1    \2\n',
        content,
        flags=re.MULTILINE,
    )

    # 4. Update docstrings
    content = re.sub(
        r':param async_token: (.*)\n( *):type async_token: AsyncToken\n',
        r':param async_token: \1, defaults to None\n\2:type async_token: AsyncToken, optional\n',
        content,
    )
    content = re.sub(
        r':param response_status_code: (.*?)(?:, defaults to None)?\n( *):type response_status_code: int(?:, optional)?\n',
        r':param response_status_code: \1, defaults to None\n\2:type response_status_code: int, optional\n',
        content,
    )

    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False


def main():
    # 1. Fix all *_async_response.py files
    pattern = os.path.join(MODEL_DIR, '*_async_response.py')
    files = sorted(glob.glob(pattern))
    print(f"Found {len(files)} async response files")

    modified = 0
    for filepath in files:
        basename = os.path.basename(filepath)
        if fix_async_response_file(filepath):
            print(f"  Fixed: {basename}")
            modified += 1
        else:
            print(f"  Skipped (already fixed or no match): {basename}")

    # 2. Fix AsyncOperationTokenResult
    token_result = os.path.join(MODEL_DIR, 'async_operation_token_result.py')
    if os.path.exists(token_result):
        if fix_async_operation_token_result(token_result):
            print(f"  Fixed: async_operation_token_result.py")
            modified += 1
        else:
            print(f"  Skipped: async_operation_token_result.py")

    # 3. Fix ReleaseIntegrationPackStatus (same pattern as async responses)
    release_status = os.path.join(MODEL_DIR, 'release_integration_pack_status.py')
    if os.path.exists(release_status):
        if fix_async_response_file(release_status):
            print(f"  Fixed: release_integration_pack_status.py")
            modified += 1
        else:
            print(f"  Skipped: release_integration_pack_status.py")

    print(f"\nModified {modified} files total")


if __name__ == '__main__':
    main()
