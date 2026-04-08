# Project 2 — 32-bit Sequential Integer Multiplier (Python)

## Overview

In this project you will implement the **core clock-cycle logic** of a **32-bit unsigned** hardware-style sequential multiplier (shift-and-add).

You are **not** allowed to use normal arithmetic operators for addition/subtraction/multiplication/division in your submission file. This forces you to implement the same bit-level behavior real hardware uses.

## Learning objectives

- Understand how multiplication can be performed via **repeated shifting and conditional addition**
- Practice **bit masking** and fixed-width arithmetic (32-bit inputs, 64-bit product)
- Understand why hardware needs an ALU and how a clocked datapath works

## What you are given

- **`alu.py`** (instructor-provided): contains `bitwise_add(a, b, width=64)` which performs addition using only bitwise logic.
- **`multiplier_student.py`** (you edit only the TODO block): contains the loop that represents **32 clock cycles**.
- **`test_cases/`**: input files (one test per file)
- **`expected_outputs/`**: correct outputs (one per test)
- **`run_student.py`**: runs your implementation on all tests and writes your answers to `student_outputs/`
- **`run_grader.py`**: checks for banned operators, then **runs your `simulate_multiplier`** and scores it vs expected outputs

## Your task (what you must implement)

Edit **only** the `# TODO` block inside:

- `simulate_multiplier(multiplicand, multiplier)` in `multiplier_student.py`

The clock-cycle loop runs **exactly 32 cycles**, and your job is to implement the bitwise logic that updates:

- `product` (64-bit)
- `multiplicand` (shifted left each cycle, kept to 64-bit)
- `multiplier` (shifted right each cycle, logical shift)

## Input/Output rules

- **Inputs** are **32-bit unsigned integers**: \(0 \le a,b \le 2^{32}-1\)
- **Output** is a **64-bit unsigned integer**: \(0 \le a\times b \le 2^{64}-1\)
- Your function must return a value masked to **64 bits**

## Encoding / decoding (IMPORTANT)

All test case files use **binary strings** (base-2).

The encode/decode logic is part of your tasks and is implemented in **`codec_student.py`**.

### Test case format (`test_cases/case_XXX.txt`)

Each file contains **one line**:

```
a b
```

where `a` and `b` are **32-bit binary strings** (exactly 32 characters each) representing **unsigned 32-bit values**.

### Expected output format (`expected_outputs/case_XXX.out`)

Each file contains **one line**:

```
product
```

where `product` is a **64-bit binary string** (exactly 64 characters) representing the **unsigned 64-bit product**.

### Internal fixed-width decoding (hardware behavior)

Even though Python integers are unbounded, you must simulate hardware widths:

- Convert inputs to 32-bit unsigned using masking:
  - `multiplicand &= 0xFFFFFFFF`
  - `multiplier &= 0xFFFFFFFF`
- Keep the shifting multiplicand to 64-bit:
  - `multiplicand = (multiplicand << 1) & 0xFFFFFFFFFFFFFFFF`
- Keep the final product to 64-bit:
  - `return product & 0xFFFFFFFFFFFFFFFF`

## Forbidden operators (static analysis)

In **`multiplier_student.py`**, these operators are banned and will cause **automatic failure**:

- `+  -  *  /  //  %`
- also banned: `+=  -=  *=  /=  //=  %=`

Bitwise operators are allowed:

- `&  |  ^  ~  <<  >>`

Comparisons and control flow are allowed:

- `== != < <= > >=`, `if`, `for`, etc.

## Student identification (required)

At the top of `multiplier_student.py`, fill in:

- `STUDENT_NAME`
- `STUDENT_SURNAME`
- `STUDENT_ID`

The grader prints these values to the terminal when grading.

## How to run

### 1) Generate your outputs

```bash
python3 run_student.py
```

This creates `student_outputs/case_XXX.out` for every test case.

This step is optional for grading (it is useful for debugging your encoder/decoder and output format).

### 2) Grade (score out of 100)

```bash
python3 run_grader.py
```

Scoring:

- If there are \(N\) tests, each test is worth \(100/N\) points.
- Your score is the number of matching outputs times that value.

## Submission checklist

- You only changed `multiplier_student.py`
- You filled in `STUDENT_NAME`, `STUDENT_SURNAME`, `STUDENT_ID`
- You can run `python3 run_student.py` without errors
- `python3 run_grader.py` prints your score

