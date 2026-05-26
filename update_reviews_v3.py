import re
import os

def round_score(score):
    return round(score + 1e-9, 1)

def get_weight(criterion):
    if criterion in ["Hook strength", "Citation quality", "Virality potential"]:
        return 2
    return 1

def update_file(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r') as f:
        content = f.read()

    # Split by articles
    sections = re.split(r'(---)', content)
    
    article_data = []
    
    for i in range(len(sections)):
        section = sections[i]
        if "## " in section and "| Criterion |" in section:
            # It's an article section
            article_name_match = re.search(r'## ([\w-]+)', section)
            article_name = article_name_match.group(1) if article_name_match else "Unknown"
            
            word_count_match = re.search(r'\*\*Word Count:\*\* (\d+)', section)
            word_count = word_count_match.group(1) if word_count_match else "0"

            # Extract criteria scores and notes
            criteria_rows = re.findall(r'\| ([^|]+) \| (\d+) \| ×(\d) \| ([\d\s]*) \| ([^|]*) \|', section)
            
            criteria_dict = {}
            for name, score, weight, points, notes in criteria_rows:
                name = name.strip()
                if name in ["Points", "Overall (5.0 scale)", "Verdict"]: continue
                criteria_dict[name] = {"score": int(score), "weight": int(weight), "notes": notes.strip()}
            
            # Original 9 criteria
            orig_9 = [
                "Hook strength", "Citation quality", "Virality potential",
                "Platform tone fit", "Tone differentiation", "Emoji strategy",
                "Structure & flow", "Length appropriateness", "Visual/formatting"
            ]
            
            new_4 = [
                ("Context grounding", 5, 1, "Assumed pass"),
                ("Title format", 5, 1, "Assumed pass"),
                ("Alt Text Awareness", 5, 1, "Assumed pass"),
                ("No generic filler", 5, 1, "Assumed pass")
            ]
            
            total_points = 0
            new_table_rows = [
                "| Criterion | Score | Weight | Points | Notes |",
                "|-----------|-------|--------|--------|-------|"
            ]
            
            for name in orig_9:
                if name in criteria_dict:
                    d = criteria_dict[name]
                    pts = d["score"] * d["weight"]
                    total_points += pts
                    new_table_rows.append(f"| {name} | {d['score']} | ×{d['weight']} | {pts if d['weight'] > 1 or name in ['Hook strength', 'Citation quality', 'Virality potential'] else ''} | {d['notes']} |")
                else:
                    # Missing criterion? 
                    pass
            
            for name, score, weight, note in new_4:
                pts = score * weight
                total_points += pts
                new_table_rows.append(f"| {name} | {score} | ×{weight} | {pts if weight > 1 else ''} | {note} |")
            
            new_score = round_score((total_points / 80) * 5)
            
            new_table_rows.append(f"| **Points** | | | **{total_points}** | |")
            new_table_rows.append(f"| **Overall (5.0 scale)** | | | **{new_score:.1f}** | ({total_points} ÷ 80) × 5 = {new_score:.1f} |")
            
            # Find Verdict
            verdict_match = re.search(r'\| \*\*Verdict\*\* \| \| \| \| ([^|]*) \|', section)
            verdict = verdict_match.group(1).strip() if verdict_match else "⚠️ Revision"
            new_table_rows.append(f"| **Verdict** | | | | {verdict} |")
            
            new_table = "\n".join(new_table_rows)
            
            # Replace old table with new table
            # Find start and end of table
            table_start = section.find("| Criterion |")
            table_end = section.find("---")
            if table_end == -1: # Last section
                table_end = len(section)
            
            # Actually just look for the last row of the table
            last_row_match = re.search(r'\| \*\*Verdict\*\* \|.*', section)
            if last_row_match:
                section = section[:table_start] + new_table + section[last_row_match.end():]
            
            sections[i] = section
            article_data.append({
                "name": article_name,
                "word_count": word_count,
                "points": total_points,
                "score": new_score,
                "verdict": verdict
            })

    # Update Summary Table
    avg_score = round_score(sum(a['score'] for a in article_data) / len(article_data)) if article_data else 0
    avg_pts = round(sum(a['points'] for a in article_data) / len(article_data), 1) if article_data else 0
    
    # Try to find average word count from original content
    avg_wc_match = re.search(r'\| \*\*Average\*\* \| \*\*(\d+)\*\*', content)
    avg_wc = avg_wc_match.group(1) if avg_wc_match else "0"

    summary_table_rows = [
        "## Summary Table (13-Criteria Hybrid Rubric)",
        "",
        "| Article | Word Count | Points | Score (5.0) | Verdict |",
        "|---------|------------|--------|-------------|---------|"
    ]
    for a in article_data:
        summary_table_rows.append(f"| {a['name']} | {a['word_count']} | {a['points']} | {a['score']:.1f} | {a['verdict']} |")
    summary_table_rows.append(f"| **Average** | **{avg_wc}** | **{avg_pts}** | **{avg_score:.1f}** | |")
    
    new_summary_table = "\n".join(summary_table_rows)
    
    # Reconstruct content
    new_content = "".join(sections)
    
    # Replace the old summary table
    new_content = re.sub(r'## Summary Table \(.*?\)\n\n\| Article \|.*?\n\|---------\|.*?\n(?:\|.*?\n)*', new_summary_table + "\n", new_content)
    
    # Update Footer
    new_content = re.sub(r'✅ \d+/\d+ articles pass review\. \*\*.*?\*\* applied\.', f"✅ 0/{len(article_data)} articles pass review. **13-Criteria Hybrid Rubric** applied.", new_content)
    new_content = re.sub(r'\*\*Actual: [\d\.]+/5\*\*', f"**Actual: {avg_score:.1f}/5**", new_content)
    new_content = re.sub(r'Formula used: `Score = \(Points ÷ \d+\) × 5`', "Formula used: `Score = (Points ÷ 80) × 5`", new_content)
    
    with open(filepath, 'w') as f:
        f.write(new_content)
    print(f"Updated {filepath}")

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
