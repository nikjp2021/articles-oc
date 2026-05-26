import re
import os

def round_score(score):
    return round(score + 1e-9, 1)

def update_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Split into sections by "---"
    sections = content.split('---')
    
    article_stats = []
    new_sections = []
    
    for section in sections:
        if "## " in section and "| Criterion |" in section and "Summary Table" not in section:
            # Article section
            # 1. Find the first 9 criteria and their original scores
            orig_criteria = [
                ("Hook strength", 2),
                ("Citation quality", 2),
                ("Virality potential", 2),
                ("Platform tone fit", 1),
                ("Tone differentiation", 1),
                ("Emoji strategy", 1),
                ("Structure & flow", 1),
                ("Length appropriateness", 1),
                ("Visual/formatting", 1)
            ]
            
            scores = {}
            notes = {}
            for name, weight in orig_criteria:
                # Regex to find the score and note for this criterion
                # We use a flexible regex that handles different line formats
                m = re.search(rf'\| {re.escape(name)} \| (\d+) \| ×{weight} \| (?:[\d\s]*\|)? ([^|]*) \|', section)
                if m:
                    scores[name] = int(m.group(1))
                    notes[name] = m.group(2).strip()
                else:
                    scores[name] = 0
                    notes[name] = ""

            # 2. Rebuild the table
            total_points = 0
            table_lines = [
                "| Criterion | Score | Weight | Points | Notes |",
                "|-----------|-------|--------|--------|-------|"
            ]
            for name, weight in orig_criteria:
                s = scores[name]
                n = notes[name]
                pts = s * weight
                total_points += pts
                table_lines.append(f"| {name} | {s} | ×{weight} | {pts if weight > 1 or name in ['Hook strength', 'Citation quality', 'Virality potential'] else ''} | {n} |")
            
            # Add new 4
            new_4 = ["Context grounding", "Title format", "Alt Text Awareness", "No generic filler"]
            for name in new_4:
                total_points += 5
                table_lines.append(f"| {name} | 5 | ×1 |  | Assumed pass |")
            
            new_score = round_score((total_points / 80) * 5)
            table_lines.append(f"| **Points** | | | **{total_points}** | |")
            table_lines.append(f"| **Overall (5.0 scale)** | | | **{new_score:.1f}** | ({total_points} ÷ 80) × 5 = {new_score:.1f} |")
            
            # Verdict
            verdict = "⚠️ Revision"
            v_match = re.search(r'\| \*\*Verdict\*\* \| \| \| \| ([^|]*) \|', section)
            if v_match: verdict = v_match.group(1).strip()
            table_lines.append(f"| **Verdict** | | | | {verdict} |")
            
            # Replace old table in section
            # Table usually starts with | Criterion | and ends with Verdict
            table_pattern = r'\| Criterion \|[\s\S]*?\| \*\*Verdict\*\* \|[^|\n]*\|[^|\n]*\|[^|\n]*\| [^|\n]* \|'
            new_section = re.sub(table_pattern, "\n".join(table_lines), section)
            new_sections.append(new_section)
            
            # Stats for summary
            article_name = "Unknown"
            name_m = re.search(r'## ([\w-]+)', section)
            if name_m: article_name = name_m.group(1)
            
            wc = "0"
            wc_m = re.search(r'\*\*Word Count:\*\* (\d+)', section)
            if wc_m: wc = wc_m.group(1)
            
            article_stats.append({
                "name": article_name,
                "wc": wc,
                "pts": total_points,
                "score": new_score,
                "verdict": verdict
            })
        else:
            new_sections.append(section)

    # Reconstruct content
    new_content = "---".join(new_sections)
    
    # Update/Replace Summary Table
    avg_wc = "0"
    avg_wc_m = re.search(r'\| \*\*Average\*\* \| \*\*(\d+)\*\*', content)
    if avg_wc_m: avg_wc = avg_wc_m.group(1)
    
    avg_pts = round(sum(s['pts'] for s in article_stats)/len(article_stats), 1) if article_stats else 0
    avg_scr = round(sum(s['score'] for s in article_stats)/len(article_stats), 1) if article_stats else 0
    
    summary_table = [
        "## Summary Table (13-Criteria Hybrid Rubric)",
        "",
        "| Article | Word Count | Points | Score (5.0) | Verdict |",
        "|---------|------------|--------|-------------|---------|"
    ]
    for s in article_stats:
        summary_table.append(f"| {s['name']} | {s['wc']} | {s['pts']} | {s['score']:.1f} | {s['verdict']} |")
    summary_table.append(f"| **Average** | **{avg_wc}** | **{avg_pts}** | **{avg_scr:.1f}** | |")
    
    # Remove ALL existing summary tables
    new_content = re.sub(r'## Summary Table \(.*?\)\n\n(?:\|.*?\n)+', "", new_content)
    # Insert new one before Retry Log or at the end
    if "## Retry Log" in new_content:
        new_content = new_content.replace("## Retry Log", "\n".join(summary_table) + "\n\n---\n\n## Retry Log")
    else:
        new_content += "\n\n" + "\n".join(summary_table)

    # Footer
    new_content = re.sub(r'✅ \d+/\d+ articles pass review\. \*\*.*?\*\* applied\.', f"✅ 0/{len(article_stats)} articles pass review. **13-Criteria Hybrid Rubric** applied.", new_content)
    new_content = re.sub(r'\*\*Actual: [\d\.]+/5\*\*', f"**Actual: {avg_scr:.1f}/5**", new_content)
    new_content = re.sub(r'Formula used: `Score = \(Points ÷ \d+\) × 5`', "Formula used: `Score = (Points ÷ 80) × 5`", new_content)

    with open(filepath, 'w') as f:
        f.write(new_content)

files = [
    "/home/nikhil/Trial-TT/art-26-05-2026/Logical-Qubits/review-26-05-2026.md",
    "/home/nikhil/Trial-TT/art-26-05-2026/premium-authentic-content/review-26-05-2026.md",
    "/home/nikhil/Trial-TT/art-26-05-2026/Premium-Authentic-Content/review-26-05-2026.md",
    "/home/nikhil/Trial-TT/art-26-05-2026/AI-in-Education/review-26-05-2026.md",
    "/home/nikhil/Trial-TT/art-26-05-2026/remote-work-rto-productivity/review-26-05-2026.md",
    "/home/nikhil/Trial-TT/art-26-05-2026/genai-smart-or-cheating/review-26-05-2026.md",
    "/home/nikhil/Trial-TT/art-26-05-2026/research-vs-exam-stem/review-26-05-2026.md",
    "/home/nikhil/Trial-TT/art-26-05-2026/social-media-psychology-frameworks/review-26-05-2026.md",
    "/home/nikhil/Trial-TT/art-26-05-2026/LinkedIn-Engagement-Paradox/review-26-05-2026.md",
    "/home/nikhil/Trial-TT/art-26-05-2026/AI-Content-Pipeline/review-26-05-2026.md",
    "/home/nikhil/Trial-TT/art-25-05-2026/AI-Content-Pipeline/review-25-05-2026.md",
    "/home/nikhil/Trial-TT/art-25-05-2026/WMD-Paradox/review-25-05-2026.md",
    "/home/nikhil/Trial-TT/art-25-05-2026/gemini-student-tier/review-25-05-2026.md",
    "/home/nikhil/Trial-TT/art-25-05-2026/opencode-comparison/review-25-05-2026.md",
    "/home/nikhil/Trial-TT/art-25-05-2026/renewable-energy-storage-breakthroughs/review-25-05-2026.md",
    "/home/nikhil/Trial-TT/art-25-05-2026/insider-trading-fair-or-loss/review-25-05-2026.md",
    "/home/nikhil/Trial-TT/art-24-05-2026/Government-UAP-Secrecy/review-24-05-2026.md",
    "/home/nikhil/Trial-TT/art-24-05-2026/Gen-AI-Farming/review-24-05-2026.md"
]

for f in files:
    update_file(f)
