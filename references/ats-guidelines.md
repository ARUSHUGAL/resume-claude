# ATS guidelines and scoring rubric

This is the shared reference for ATS (Applicant Tracking System) quality in this workspace. The `/atscheck` skill scores against it, `/jobupdate` uses it for its ATS score, and the LaTeX template is built to pass it. The numbers mirror what public checkers (Resume Worded, Jobscan, Enhancv) report.

## How an ATS reads a resume

An ATS parses the **text layer** of your PDF, not the visual layout. So the test that matters is: run `pdftotext` on the PDF and read what comes out. If a section, a date, or your phone number isn't in that text, the ATS can't see it either.

```
pdftotext -layout path/to/resume.pdf -    # human-readable extraction
pdftotext path/to/resume.pdf -            # raw reading order, closer to ATS parse
```

If `pdftotext` returns little or no text, the resume is image-based and most ATS will reject it. (Resumes built by this workspace are always text-based, so this only bites if someone checks an external PDF.)

## What ATS checkers score (five categories)

### 1. Keyword and skills match against the job description (highest weight)
The ATS matches your resume against the JD: hard skills, tools, certifications, job titles, and industry terms. It looks at whether the term is present, where it appears, and how it's phrased. Use the JD's exact wording for tools you actually use ("PostgreSQL" not "Postgres" if the JD says PostgreSQL). Only ever claim skills the candidate genuinely has.

### 2. Formatting and parseability
Simple single-column layouts with standard section headings parse best. Things that break ATS parsing:
- Tables, text boxes, and multiple columns for content
- Images, logos, icons, charts
- Content inside headers/footers (many ATS strip these)
- Non-standard fonts or heavy graphics
- Skills shown only as bars or ratings instead of words

Safe choices: single column, standard fonts (Arial/Helvetica/Calibri), real text bullets, PDF file type.

### 3. Section completeness
Standard, clearly named sections the ATS expects: Summary, Experience, Education, Skills. Each job needs a title, company, location, and dates. Use conventional headings ("Experience," not "Where I've Made an Impact").

### 4. Content quality
Quantified achievements (numbers, %, $, time saved), strong past-tense action verbs (Built, Led, Shipped, Reduced), and concrete results rather than duties. This is the part a human recruiter also reads, so it counts twice.

### 5. Contact and basics
Email, phone, location, and a LinkedIn URL, all as plain text in the body (not in a header/footer or image).

## Scoring rubric (0 to 100)

When a JD is provided, weight the categories like this:

| Category | Weight |
|---|---|
| Keyword / skills match vs JD | 40 |
| Formatting and parseability | 20 |
| Section completeness | 15 |
| Content quality (quantification, action verbs) | 15 |
| Contact and basics | 10 |

When no JD is provided, drop the keyword weight and spread it across the rest (formatting 30, sections 25, content 30, contact 15), and judge keywords as "are role-relevant skills present and specific" rather than matched to a posting.

## Benchmarks

- **75 to 100**: strong. Well aligned, likely to pass ATS and reach a recruiter.
- **60 to 74**: readable but has gaps. Missing keywords or minor formatting/content issues.
- **Below 60**: likely filtered out before a human sees it. Fix before applying.

## The honesty rule still applies

A high ATS score never justifies adding skills or experience the candidate doesn't have. If the JD wants a keyword that isn't true for them, the score stays lower. Raise it by surfacing real, relevant experience and using the JD's exact terms for things they've actually done, never by inventing matches.

## Why resumes from this workspace already score well

The LaTeX template (`resume/master/resume_template.tex`) is built to pass category 2 by default:
- Single column, standard fonts, real text bullets, text-based PDF
- Standard section headings
- Empty header/footer (no content the ATS would strip)
- Dates, titles, companies as plain text

So the work in `/jobupdate` and `/atscheck` is mostly categories 1, 4, and 5: keywords, quantification, and completeness.

## Further reading and open-source tools

These informed this rubric and are useful if you want to go deeper:

- [Resume Worded — ATS resume guide](https://resumeworded.com/ats-resume)
- [Jobscan — resume scanner](https://www.jobscan.co/resume-scanner)
- [Enhancv — ATS resume checker](https://enhancv.com/resources/resume-checker/)
- [srbhr/Resume-Matcher](https://github.com/srbhr/Resume-Matcher) — open-source ATS matcher (spaCy/NLTK, semantic similarity)
- [xitanggg/open-resume](https://github.com/xitanggg/open-resume) — open-source resume parser, good for testing ATS readability
- [miteshgupta07/ATS-Scoring-System](https://github.com/miteshgupta07/ATS-Scoring-System) — keyword-based scoring example
- [jananthan30/Resume-Builder](https://github.com/jananthan30/Resume-Builder) — 8-component ATS + 6-factor HR scorer, local Python, free tier

## Real ATS scoring algorithm (8 weighted components)

Based on testing with the Resume-Builder open-source engine (same logic as Workday/Taleo/Greenhouse filters):

| Component | Weight | What it measures |
|-----------|--------|------------------|
| Phrase Match | 25% | Multi-word industry phrases from the JD (exact match). 10.6x callback increase for exact phrase matches. |
| Keyword Match | 20% | Lemmatized single keywords with synonym expansion. |
| Weighted Industry Terms | 15% | Domain-specific terminology with recency decay. |
| Semantic Similarity | 10% | SBERT vector cosine similarity between resume text and JD text. |
| BM25 Score | 10% | Probabilistic relevance ranking (same algorithm search engines use). |
| Job Title Match | 10% | Whether the JD's exact job title appears in your resume header or summary. |
| Graph Centrality | 5% | Infers related skills from a skill graph (NetworkX). |
| Skill Recency | 5% | Exponential decay: recent experience weighted higher than old. |

Key insight: **Phrase Match (25%) is the single highest-weight component.** If the JD says "distributed systems" and your resume doesn't have that exact two-word phrase together, you lose a quarter of your score even if you have both words separately.

## Proven tactics that move the score (from real testing)

These changes moved a resume from 57.8% to 88.9% against a Backend SWE Intern JD:

1. **Mirror exact multi-word phrases from the JD.** "system design", "distributed systems", "REST API", "CI/CD pipeline" must appear as-is, not paraphrased. This alone moved Phrase Match from 40% to 100%.
2. **Every single keyword in the JD must appear somewhere on your resume.** Missing even one "nice to have" keyword costs you. Put them in Skills if you can't fit them in bullets.
3. **Put skills in TWO places:** the Skills section (for keyword list matching) AND inside experience bullets (for contextual matching, which ranks higher).
4. **Use a dedicated Skills subsection for Cloud/DevOps.** Listing AWS, GCP, Azure, Docker, CI/CD in one line catches all cloud keywords regardless of which the JD asks for.
5. **Add the JD's job title verbatim to your Summary.** If the JD says "Software Engineer Intern - Backend", your summary should say "backend software engineering internship" or similar.
6. **Soft skills count.** "teamwork", "communication", "agile" are keywords too. Weave them into team-lead bullets naturally.

## What kills your score (from real testing)

- **FontAwesome or icon fonts in LaTeX.** They extract as `(cid:XXX)` garbage and corrupt nearby text. The ATS sees gibberish instead of your phone number and email. This dropped a resume from parseable to 35.9%. Never use `\faPhone`, `\faEnvelope`, `\faLinkedin`, etc.
- **Word concatenation in PDF extraction.** Dense LaTeX spacing can cause `pdftotext` to merge words: "ComputerSciencestudent" instead of "Computer Science student". The ATS can't match keywords it can't parse. Test with `pdftotext resume.pdf -` and check for merged words.
- **Readability penalty.** Overly complex sentences (Dale-Chall > 10) get penalized. Keep bullets to one clear sentence each.
- **Missing "nice to have" keywords.** Even optional requirements cost points. If you have any exposure at all, mention it.

## Template comparison (tested August 2025)

| Template | ATS Score | Issue |
|----------|-----------|-------|
| Custom (this workspace's template) | 88.9% | Clean extraction, no icons, single column |
| Jake's Resume (fontawesome5) | 35.9% | Icons extract as CID codes, words concatenate, phrase match drops to 0% |

The workspace template is ATS-optimal. Do not switch to icon-based templates.
