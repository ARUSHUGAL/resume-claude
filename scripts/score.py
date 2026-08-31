#!/usr/bin/env python3
"""
ATS Resume Scorer — scores a resume PDF against a job description.

Usage:
    python3 scripts/score.py jobs/palantir_swe_intern_2027/resume.pdf jobs/palantir_swe_intern_2027/job_description.txt

Or just:
    python3 scripts/score.py <resume.pdf> <jd.txt>
"""
import sys
import os

# Add the scorer module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ats_scorer'))

import pdfplumber
from ats_scorer import score_resume_text

def extract_pdf(path):
    with pdfplumber.open(path) as pdf:
        return ''.join(p.extract_text() or '' for p in pdf.pages)

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 scripts/score.py <resume.pdf> <job_description.txt>")
        sys.exit(1)

    resume_path = sys.argv[1]
    jd_path = sys.argv[2]

    if not os.path.exists(resume_path):
        print(f"Error: {resume_path} not found")
        sys.exit(1)
    if not os.path.exists(jd_path):
        print(f"Error: {jd_path} not found")
        sys.exit(1)

    print(f"Scoring: {resume_path}")
    print(f"Against: {jd_path}")
    print()

    resume_text = extract_pdf(resume_path)
    jd_text = open(jd_path).read()

    result = score_resume_text(resume_text, jd_text)

    print("=" * 60)
    print(f"ATS SCORE: {result['total_score']}%")
    print(f"Rating: {result['rating']}")
    print(f"Likelihood: {result['likelihood']}")
    print("=" * 60)

    print(f"\n  Keyword Match (20%):     {result['keyword_score']:.1f}%")
    print(f"  Phrase Match (25%):      {result['phrase_score']:.1f}%")
    print(f"  Weighted Industry (15%): {result['weighted_score']:.1f}%")
    print(f"  Semantic (10%):          {result['semantic_score']:.1f}%")
    print(f"  BM25 (10%):              {result['bm25_score']:.1f}%")
    print(f"  Job Title (10%):         {result['job_title_match']['score']}%")
    print(f"  Skill Recency (5%):      {result['skill_recency']['recency_adjusted_score']:.1f}%")
    print(f"  Graph Centrality (5%):   {result['skill_graph']['graph_score']:.1f}%")

    print(f"\n  Matched Keywords ({len(result['matched_keywords'])}): {', '.join(sorted(result['matched_keywords']))}")
    print(f"  Missing Keywords ({len(result['missing_keywords'])}): {', '.join(sorted(result['missing_keywords']))}")
    print(f"  Matched Phrases ({len(result['matched_phrases'])}): {', '.join(result['matched_phrases'])}")
    print(f"  Missing Phrases ({len(result['missing_phrases'])}): {', '.join(result['missing_phrases'])}")
    print(f"  Penalties: {result.get('penalties', {})}")

if __name__ == '__main__':
    main()
