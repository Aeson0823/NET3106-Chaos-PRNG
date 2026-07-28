import sys
import os

# Make sure Python can find the randomness_testsuite package
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "randomness_testsuite-master"))

from FrequencyTest import FrequencyTest as ft
from RunTest import RunTest as rt
from Matrix import Matrix as mt
from Spectral import SpectralTest as st
from TemplateMatching import TemplateMatching as tm
from Universal import Universal as ut
from Complexity import ComplexityTest as ct
from Serial import Serial as serial
from ApproximateEntropy import ApproximateEntropy as aet
from CumulativeSum import CumulativeSums as cst


def read_bits_as_string(path):
    """NIST test suite functions expect a plain string of '0'/'1' characters."""
    with open(path, "r") as f:
        return f.read().strip()


def run_all_tests(binary_data, label, log_lines):
    """
    Run all 14 NIST SP 800-22 tests on a bit string and return a list of
    (test_name, p_value, verdict) tuples. verdict is 'PASS' or 'FAIL'.
    Every printed line is also appended to log_lines so it can be saved to file.
    """
    results = []

    def emit(line):
        print(line)
        log_lines.append(line)

    def add(name, outcome):
        # outcome is (p_value, bool) or (p_value, bool, error_msg)
        p_value = outcome[0]
        passed = outcome[1]
        verdict = "PASS" if passed else "FAIL"
        results.append((name, p_value, verdict))
        emit(f"  [{label}] {name:35s} p={p_value:.6f}  {verdict}")

    emit(f"\nRunning NIST SP 800-22 suite on: {label}  ({len(binary_data)} bits)")

    add("01 Frequency (Monobit)", ft.monobit_test(binary_data))
    add("02 Block Frequency", ft.block_frequency(binary_data))
    add("03 Runs", rt.run_test(binary_data))
    add("04 Longest Run of Ones", rt.longest_one_block_test(binary_data))
    add("05 Binary Matrix Rank", mt.binary_matrix_rank_text(binary_data))
    add("06 DFT (Spectral)", st.spectral_test(binary_data))
    add("07 Non-overlapping Template", tm.non_overlapping_test(binary_data))
    add("08 Overlapping Template", tm.overlapping_patterns(binary_data))
    add("09 Maurer Universal", ut.statistical_test(binary_data))
    add("10 Linear Complexity", ct.linear_complexity_test(binary_data))

    serial_result = serial.serial_test(binary_data)
    # serial_test returns ((p1, bool1), (p2, bool2)) -- report the first p-value
    add("11 Serial", serial_result[0])

    add("12 Approximate Entropy", aet.approximate_entropy_test(binary_data))

    add("13 Cumulative Sums (forward)", cst.cumulative_sums_test(binary_data, mode=0))
    add("14 Cumulative Sums (reverse)", cst.cumulative_sums_test(binary_data, mode=1))

    n_pass = sum(1 for _, _, v in results if v == "PASS")
    emit(f"  -> {label}: {n_pass}/14 tests passed")

    return results


def build_comparison_table(results_a, label_a, results_b, label_b):
    lines = []
    lines.append(f"\n{'Test':35s} {label_a+' p':>12s} {label_a:>6s}  {label_b+' p':>12s} {label_b:>6s}")
    lines.append("-" * 90)
    for (name, pa, va), (_, pb, vb) in zip(results_a, results_b):
        lines.append(f"{name:35s} {pa:12.6f} {va:>6s}  {pb:12.6f} {vb:>6s}")
    return lines


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 part_d_nist_tests.py <source_A.txt> <source_B.txt> [--validate]")
        sys.exit(1)

    path_a, path_b = sys.argv[1], sys.argv[2]
    validate_mode = "--validate" in sys.argv

    label_a = "GOOD/benchmark" if validate_mode else "STRONG"
    label_b = "WEAK/benchmark" if validate_mode else "WEAK"

    data_a = read_bits_as_string(path_a)
    data_b = read_bits_as_string(path_b)

    log_lines = []

    results_a = run_all_tests(data_a, label_a, log_lines)
    results_b = run_all_tests(data_b, label_b, log_lines)

    table_lines = build_comparison_table(results_a, label_a, results_b, label_b)
    for line in table_lines:
        print(line)
    log_lines.extend(table_lines)

    # Save everything to a results file, in the same folder as this script
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_name = "nist_results_validation.txt" if validate_mode else "nist_results.txt"
    out_path = os.path.join(out_dir, out_name)

    with open(out_path, "w") as f:
        f.write("\n".join(log_lines) + "\n")

    print(f"\nResults saved to: {out_path}")
