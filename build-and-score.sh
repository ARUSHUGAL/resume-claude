#!/usr/bin/env bash
# Build all resumes AND score each tailored one against its JD.
# Usage: bash build-and-score.sh
# Or for a single job: bash build-and-score.sh jobs/palantir_swe_intern_2027
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"

# First, build everything
echo "=== BUILDING ==="
bash "$ROOT/build.sh"
echo

# Then score each tailored resume that has a job_description.txt
echo "=== SCORING ==="
echo

if [ "$#" -ge 1 ]; then
    # Score a specific job folder
    FOLDERS=("$1")
else
    # Score all active job folders (skip _archive)
    shopt -s nullglob
    FOLDERS=("$ROOT"/jobs/*/)
    shopt -u nullglob
fi

SCORED=0
for job_dir in "${FOLDERS[@]}"; do
    job_name="$(basename "$job_dir")"
    [ "$job_name" = "_archive" ] && continue

    jd_file="$job_dir/job_description.txt"
    pdf_file="$job_dir/${job_name}_resume.pdf"

    # Fall back to resume.pdf if renamed version doesn't exist
    if [ ! -f "$pdf_file" ]; then
        pdf_file="$job_dir/resume.pdf"
    fi

    if [ -f "$jd_file" ] && [ -f "$pdf_file" ]; then
        echo "--- $job_name ---"
        python3 "$ROOT/scripts/score.py" "$pdf_file" "$jd_file" 2>/dev/null | grep -E "ATS SCORE|Rating|Likelihood|Keyword Match|Phrase Match|Missing"
        echo
        SCORED=$((SCORED + 1))
    fi
done

if [ "$SCORED" -eq 0 ]; then
    echo "No jobs found with both a resume PDF and job_description.txt."
    echo "Create a job folder with both files, or run: bash build-and-score.sh jobs/<folder>"
fi

echo "=== DONE ($SCORED resumes scored) ==="
