import re
import os
import sys

def update_file(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r') as f:
        content = f.read()

    if "13-Criteria" in content or "÷ 80" in content:
        print(f"Skipping {filepath} (already updated)")
        return

    # 1. Update individual article tables
    # Find all tables and their following points/score
    # We look for the last row of the table which is usually Visual/formatting
    
    new_criteria = [
        "| Context grounding | 5 | ×1 | 5 | Assumed pass |",
        "| Title format | 5 | ×1 | 5 | Assumed pass |",
        "| Alt Text Awareness | 5 | ×1 | 5 | Assumed pass |",
        "| No generic filler | 5 | ×1 | 5 | Assumed pass |"
    ]
    new_criteria_str = "\n".join(new_criteria) + "\n"

    # Pattern to find the end of the table before "Points"
    # Looking for: | Visual/formatting | ... |
    # then inserting new criteria before | **Points** |
    content = content.replace("| Visual/formatting |", "| Visual/formatting |") # just a marker
    
    parts = re.split(r'(\| \*\*Points\*\* \|)', content)
    if len(parts) > 1:
        new_content_parts = []
        new_content_parts.append(parts[0])
        for i in range(1, len(parts), 2):
            # parts[i] is "| **Points** |"
            # parts[i+1] contains the points value and the score
            
            # Insert new criteria before "| **Points** |"
            # But we need to make sure we are adding it to the end of the previous table
            # parts[i-1] ends with the last row of the table
            
            # Find the points value
            points_match = re.search(r'\*\*(\d+)\*\*', parts[i+1])
            if points_match:
                old_points = int(points_match.group(1))
                new_points = old_points + 20
                parts[i+1] = parts[i+1].replace(f"**{old_points}**", f"**{new_points}**")
                
                # Update score
                # | **Overall (5.0 scale)** | | | **4.0** | (48 ÷ 60) × 5 = 4.0 |
                score_pattern = r'\| \*\*Overall \(5\.0 scale\)\*\* \| \| \| \*\*([\d\.]+)\*\* \| \((\d+) ÷ 60\) × 5 = ([\d\.]+) \|'
                def score_replace(m):
                    new_score = round((new_points / 80) * 5, 1)
                    return f"| **Overall (5.0 scale)** | | | **{new_score:.1f}** | ({new_points} ÷ 80) × 5 = {new_score:.1f} |"
                
                parts[i+1] = re.sub(score_pattern, score_replace, parts[i+1])
            
            # Add new criteria to parts[i-1]
            last_pipe = parts[i-1].rfind('|')
            if last_pipe != -1:
                # Find the start of the last line
                last_newline = parts[i-1].rfind('\n', 0, last_pipe)
                parts[i-1] = parts[i-1][:last_newline+1] + new_criteria_str + parts[i-1][last_newline+1:]

            new_content_parts.append(parts[i])
            new_content_parts.append(parts[i+1])
        content = "".join(new_content_parts)

    # 2. Update Summary Table
    content = content.replace("Summary Table (9-Criteria Hybrid Rubric)", "Summary Table (13-Criteria Hybrid Rubric)")
    
    # Find the summary table rows
    summary_table_pattern = r'(\| Article \| Word Count \| Points \| Score \(5\.0\) \| Verdict \|[\s\S]+?)(?=\n\n|---|\Z)'
    summary_match = re.search(summary_table_pattern, content)
    if summary_match:
        table = summary_match.group(1)
        rows = table.split('\n')
        new_rows = []
        scores = []
        for row in rows:
            if '| Article |' in row or '|---------|' in row:
                new_rows.append(row)
                continue
            cols = row.split('|')
            if len(cols) >= 6:
                # Article | Word Count | Points | Score (5.0) | Verdict
                article = cols[1].strip()
                if article == "**Average**":
                    # We'll recalculate average later
                    continue
                
                try:
                    old_pts = int(cols[3].strip())
                    new_pts = old_pts + 20
                    new_score = round((new_pts / 80) * 5, 1)
                    cols[3] = f" {new_pts} "
                    cols[4] = f" {new_score:.1f} "
                    scores.append(new_score)
                    new_rows.append("|".join(cols))
                except ValueError:
                    new_rows.append(row)
        
        if scores:
            avg_score = round(sum(scores) / len(scores), 1)
            # Find average word count from old table if possible
            avg_word_count = ""
            for row in rows:
                if "**Average**" in row:
                    m = re.search(r'\*\*(\d+)\*\*', row)
                    if m:
                        avg_word_count = m.group(1)
            
            new_rows.append(f"| **Average** | **{avg_word_count}** | **{round(sum([int(r.split('|')[3].strip()) for r in new_rows if '|' in r and 'Article' not in r and '---' not in r])/len(scores), 1)}** | **{avg_score:.1f}** | |")
        
        new_table = "\n".join(new_rows)
        content = content.replace(table, new_table)

    # 3. Update footer
    content = content.replace("**9-Criteria Hybrid Rubric** applied.", "**13-Criteria Hybrid Rubric** applied.")
    content = content.replace("Formula used: `Score = (Points ÷ 60) × 5`", "Formula used: `Score = (Points ÷ 80) × 5`")
    
    # Update Actual Score in footer
    actual_score_match = re.search(r'\*\*Actual: ([\d\.]+)/5\*\*', content)
    if actual_score_match and scores:
        avg_score = round(sum(scores) / len(scores), 1)
        content = content.replace(f"**Actual: {actual_score_match.group(1)}/5**", f"**Actual: {avg_score:.1f}/5**")

    with open(filepath, 'w') as f:
        f.write(content)
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
