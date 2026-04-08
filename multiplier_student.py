"""
multiplier_student.py (Starter Code)

STUDENT_NAME = ""
STUDENT_SURNAME = ""
STUDENT_ID = ""

Goal: Implement the core bitwise logic of a 32-bit sequential (shift-add) multiplier.

Rules for this file:
  - Inputs are 32-bit unsigned integers.
  - Output is a 64-bit unsigned integer product.
  - All additions MUST use alu.bitwise_add(...).
  - Standard arithmetic operators are strictly banned here: +, -, *, /, //, %
"""

from __future__ import annotations

from alu import bitwise_add


MASK_32 = 0xFFFFFFFF
MASK_64 = 0xFFFFFFFFFFFFFFFF


def simulate_multiplier(multiplicand: int, multiplier: int) -> int:
    """
    Simulate a 32-cycle hardware sequential multiplier.

    This uses the classic shift-add algorithm:
      - Each cycle examines the multiplier's LSB.
      - If LSB is 1, add the (shifted) multiplicand into the product.
      - Shift multiplicand left, shift multiplier right, repeat for 32 cycles.
    """

    multiplicand &= MASK_32
    multiplier &= MASK_32

    product = 0
    multiplicand = multiplicand & MASK_64

    for cycle in range(32):
        # TODO (Students): Implement the bitwise "clock cycle" logic below.
        #
        # You must NOT use +, -, *, /, //, or % anywhere in this file.
        # You must use bitwise operators (&, |, ^, ~, <<, >>) and comparisons.
        # You must use bitwise_add(...) for any addition.
        #
        # Required steps each cycle:
        #   1) Extract the Least Significant Bit (LSB) of the multiplier.
        #      Hint: lsb = multiplier & 1
        #
        #   2) If LSB is 1, update product by calling:
        #        product = bitwise_add(product, multiplicand, 64)
        #
        #   3) Shift the multiplicand left by 1 bit.
        #      Keep it 64-bit wide using:
        #        multiplicand = (multiplicand << 1) & 0xFFFFFFFFFFFFFFFF
        #
        #   4) Shift the multiplier right by 1 bit (logical shift).
        #      Hint: multiplier >>= 1
        #
        # When you're done, the loop should behave like a real sequential
        # multiplier for 32-bit unsigned inputs.
        _ = cycle  # placeholder so 'cycle' is "used"

    return product & MASK_64

