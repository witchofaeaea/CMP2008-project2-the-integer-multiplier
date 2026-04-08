import os
import sys

from multiplier_student import simulate_multiplier

from codec_student import MASK_64, decode_test_case_file, encode_u64


def main() -> None:
    test_dir = "test_cases"
    out_dir = "student_outputs"

    if not os.path.isdir(test_dir):
        print(f"Error: missing '{test_dir}/' folder")
        sys.exit(1)

    os.makedirs(out_dir, exist_ok=True)

    cases = sorted(f for f in os.listdir(test_dir) if f.endswith(".txt"))
    if not cases:
        print(f"Error: no test cases found in '{test_dir}/'")
        sys.exit(1)

    for filename in cases:
        case_path = os.path.join(test_dir, filename)
        with open(case_path, "r", encoding="utf-8") as f:
            contents = f.read()
        try:
            tc = decode_test_case_file(contents)
        except ValueError as e:
            print(f"Bad test case format: {case_path} ({e})")
            sys.exit(1)

        a, b = tc
        product = simulate_multiplier(a, b) & MASK_64

        out_name = os.path.splitext(filename)[0] + ".out"
        out_path = os.path.join(out_dir, out_name)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(encode_u64(product) + "\n")

    print(f"Wrote {len(cases)} output files to '{out_dir}/'")


if __name__ == "__main__":
    main()

