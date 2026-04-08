import ast
import os
import re
import sys


BANNED_BINOPS = (
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
)


def _op_name(op: ast.AST) -> str:
    if isinstance(op, ast.Add):
        return "+"
    if isinstance(op, ast.Sub):
        return "-"
    if isinstance(op, ast.Mult):
        return "*"
    if isinstance(op, ast.Div):
        return "/"
    if isinstance(op, ast.FloorDiv):
        return "//"
    if isinstance(op, ast.Mod):
        return "%"
    return op.__class__.__name__


class BannedOperatorVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.violations: list[tuple[str, int]] = []

    def visit_BinOp(self, node: ast.BinOp) -> None:
        if isinstance(node.op, BANNED_BINOPS):
            self.violations.append((_op_name(node.op), getattr(node, "lineno", -1)))
        self.generic_visit(node)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        if isinstance(node.op, BANNED_BINOPS):
            self.violations.append((_op_name(node.op), getattr(node, "lineno", -1)))
        self.generic_visit(node)


_STUDENT_RE = re.compile(
    r"^\s*(STUDENT_NAME|STUDENT_SURNAME|STUDENT_ID)\s*=\s*([\"'])(.*?)\2\s*$",
    re.MULTILINE,
)


def _extract_student_info(source: str) -> dict[str, str]:
    info: dict[str, str] = {}
    for key, _quote, value in _STUDENT_RE.findall(source):
        info[key] = value.strip()
    return info


MASK_64 = 0xFFFFFFFFFFFFFFFF
MASK_32 = 0xFFFFFFFF


def _decode_u64_bin(text: str) -> int:
    s = text.strip()
    if s == "":
        raise ValueError("empty output")
    if any(ch not in "01" for ch in s):
        raise ValueError("output contains non-binary characters")
    return int(s, 2) & MASK_64


def _encode_u64_bin(value: int) -> str:
    return format(value & MASK_64, "064b")


def _decode_u32_bin(token: str) -> int:
    s = token.strip()
    if s == "":
        raise ValueError("empty token")
    if any(ch not in "01" for ch in s):
        raise ValueError("token contains non-binary characters")
    return int(s, 2) & MASK_32


def _decode_test_case(contents: str) -> tuple[int, int]:
    parts = contents.strip().split()
    if len(parts) != 2:
        raise ValueError("expected exactly two binary integers")
    a = _decode_u32_bin(parts[0])
    b = _decode_u32_bin(parts[1])
    return a, b


def main() -> None:
    target = "multiplier_student.py"

    try:
        with open(target, "r", encoding="utf-8") as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Error: {target} not found.")
        sys.exit(1)

    student = _extract_student_info(source)
    print("Student Info:")
    print(f"  Name: {student.get('STUDENT_NAME', '')}")
    print(f"  Surname: {student.get('STUDENT_SURNAME', '')}")
    print(f"  ID: {student.get('STUDENT_ID', '')}")

    tree = ast.parse(source, filename=target)
    visitor = BannedOperatorVisitor()
    visitor.visit(tree)

    if visitor.violations:
        # If static analysis fails, the submission receives 0/100 by policy.
        test_dir = "test_cases"
        total = 0
        if os.path.isdir(test_dir):
            total = len([f for f in os.listdir(test_dir) if f.endswith(".txt")])

        for op, line in visitor.violations:
            print(f"Banned operator '{op}' at line {line}")
        print("Static Analysis Failed: Banned Operators Detected")
        if total > 0:
            print(f"Passed: 0/{total}")
        print("Score: 0.00/100.00")
        sys.exit(1)

    print("Static Analysis Passed. Running student solution and grading...")

    test_dir = "test_cases"
    expected_dir = "expected_outputs"

    if not os.path.isdir(test_dir):
        print(f"Error: missing '{test_dir}/' folder")
        sys.exit(1)
    if not os.path.isdir(expected_dir):
        print(f"Error: missing '{expected_dir}/' folder")
        sys.exit(1)
    try:
        from multiplier_student import simulate_multiplier
    except Exception as e:
        print("Error: could not import simulate_multiplier from multiplier_student.py")
        print(str(e))
        print("Passed: 0/0")
        print("Score: 0.00/100.00")
        sys.exit(1)

    cases = sorted(f for f in os.listdir(test_dir) if f.endswith(".txt"))
    if not cases:
        print(f"Error: no test cases found in '{test_dir}/'")
        sys.exit(1)

    total = len(cases)
    passed = 0
    per_test = 100.0 / float(total)

    mismatches: list[str] = []
    runtime_errors: list[str] = []

    for case_file in cases:
        base = os.path.splitext(case_file)[0]
        expected_path = os.path.join(expected_dir, base + ".out")
        case_path = os.path.join(test_dir, case_file)

        if not os.path.isfile(expected_path):
            print(f"Error: missing expected output '{expected_path}'")
            sys.exit(1)

        with open(expected_path, "r", encoding="utf-8") as f:
            try:
                expected = _encode_u64_bin(_decode_u64_bin(f.read()))
            except ValueError:
                print(f"Error: bad expected output format in '{expected_path}'")
                sys.exit(1)
        with open(case_path, "r", encoding="utf-8") as f:
            try:
                a, b = _decode_test_case(f.read())
            except ValueError as e:
                print(f"Error: bad test case format in '{case_path}' ({e})")
                sys.exit(1)

        try:
            got_value = simulate_multiplier(a, b)
            got = _encode_u64_bin(got_value)
        except Exception:
            runtime_errors.append(base)
            got = ""

        if got == expected:
            passed += 1
        else:
            mismatches.append(base)

    score = passed * per_test

    print(f"Passed: {passed}/{total}")
    print(f"Score: {score:.2f}/100.00")

    if runtime_errors:
        print(f"Runtime errors ({len(runtime_errors)}): " + ", ".join(runtime_errors[:10]) + (" ..." if len(runtime_errors) > 10 else ""))
    if mismatches:
        print(f"Mismatched outputs ({len(mismatches)}): " + ", ".join(mismatches[:10]) + (" ..." if len(mismatches) > 10 else ""))

    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()

