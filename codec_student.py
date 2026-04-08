"""
codec_student.py (Student TODO)

This file defines the "encoder/decoder" for the file-based test format.

Test cases are plain text files with **binary strings**:
  - Inputs:  "a b"  (two unsigned 32-bit binary integers)
  - Outputs: "p"    (one unsigned 64-bit binary integer)

You will implement:
  - decode_u32(token: str) -> int
  - decode_test_case_file(contents: str) -> tuple[int, int]
  - encode_u64(value: int) -> str

Hardware rule:
  - Always mask inputs to 32-bit, outputs to 64-bit.
"""

from __future__ import annotations


MASK_32 = 0xFFFFFFFF
MASK_64 = 0xFFFFFFFFFFFFFFFF


def decode_u32(token: str) -> int:
    """
    TODO: Convert a binary string into an *unsigned 32-bit* value.

    Requirements:
      - The token is a binary integer string (e.g., "0", "101", "0001").
      - You may assume it only contains '0' and '1' characters.
      - You may assume it represents a non-negative value.
      - Return value must be masked to 32 bits (use & MASK_32).
      - Do NOT raise on large numbers; masking is the intended behavior.
    """

    raise NotImplementedError


def decode_test_case_file(contents: str) -> tuple[int, int]:
    """
    TODO: Parse the contents of a test case file and return (a, b).

    File format:
      - One line with two binary strings: "a b"
      - Whitespace-separated

    Requirements:
      - Use decode_u32(...) for both a and b.
      - If the format is wrong, raise ValueError with a helpful message.
    """

    raise NotImplementedError


def encode_u64(value: int) -> str:
    """
    TODO: Convert an integer into the exact output string for the grader.

    Requirements:
      - Output must be a single **64-bit binary** string (exactly 64 characters).
      - Value must be masked to 64 bits (use & MASK_64).
      - Example output: "0000000000000000000000000000000000000000000000000000000000000000"
    """

    raise NotImplementedError

