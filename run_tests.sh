#!/usr/bin/env bash
# Compile and run every bundled testcase, diffing against its recorded
# expected output and expected semantic errors.
#
#   ./run_tests.sh            # all testcases
#   ./run_tests.sh T1 S3      # only the named ones

set -uo pipefail
cd "$(dirname "$0")"

CASES_DIR="Tests/phase3_tester/test/testcases"
PY="${PYTHON:-python3}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

if [ "$#" -gt 0 ]; then
    cases=("$@")
else
    cases=()
    for d in "$CASES_DIR"/*/; do cases+=("$(basename "$d")"); done
fi

pass=0; fail=0; failed=()
for t in "${cases[@]}"; do
    d="$CASES_DIR/$t"
    if [ ! -f "$d/input.txt" ]; then
        echo "  SKIP $t (no input.txt)"; continue
    fi

    if ! "$PY" compile_and_exec.py -i "$d/input.txt" \
            -o "$TMP/$t.out" -e "$TMP/$t.err" >"$TMP/$t.log" 2>&1; then
        echo "  FAIL $t (compiler exited non-zero)"
        sed 's/^/        /' "$TMP/$t.log"
        fail=$((fail + 1)); failed+=("$t")
        continue
    fi

    ok=1
    # Programs that should run: compare VM output.
    if [ -f "$d/expected.txt" ] && ! diff -qwB "$d/expected.txt" "$TMP/$t.out" >/dev/null 2>&1; then
        ok=0
    fi
    # Programs with semantic errors: compare the diagnostics.
    if [ -f "$d/semantic_errors.txt" ] && ! diff -qwB "$d/semantic_errors.txt" semantic_errors.txt >/dev/null 2>&1; then
        ok=0
    fi

    if [ "$ok" -eq 1 ]; then
        echo "  PASS $t"; pass=$((pass + 1))
    else
        echo "  FAIL $t"; fail=$((fail + 1)); failed+=("$t")
    fi
done

echo
echo "$pass passed, $fail failed"
if [ "$fail" -gt 0 ]; then
    echo "failed: ${failed[*]}"
    exit 1
fi
