"""
multiplier_student.py (Starter Code)

STUDENT_NAME = "Hatice"
STUDENT_SURNAME = "Yaşasın"
STUDENT_ID = "2104423"

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
        # 1) Extract the Least Significant Bit (LSB) of the multiplier.
        lsb = multiplier & 1
        
        # 2) If LSB is 1, update product using the ALU function
        if lsb == 1:
            product = bitwise_add(product, multiplicand, 64)
            
        # 3) Shift the multiplicand left by 1 bit.
        #    Keep it 64-bit wide using the predefined constant
        multiplicand = (multiplicand << 1) & MASK_64
        
        # 4) Shift the multiplier right by 1 bit (logical shift).
        multiplier >>= 1

    return product & MASK_64
