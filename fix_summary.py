import re
import os

def round_score(score):
    return round(score + 1e-9, 1)

def update_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Find all article points and scores from the body
    article_points = re.findall(r'\| \*\*Points\*\* \| \| \| \*\*(\d+)\*\* \|', content)
    article_scores = re.findall(r'\| \*\*Overall \(5\.0 scale\)\*\* \| \| \| \*\*([\d\.]+)\*\* \|', content)
    
    if not article_points:
        return

    pts = [int(p) for p in article_points]
    scr = [float(s) for s in article_scores]
    avg_pts = round(sum(pts) / len(pts), 1)
    avg_scr = round(sum(scr) / len(scr), 1)

    # Update Summary Table
    summary_table_match = re.search(r'## Summary Table \(13-Criteria Hybrid Rubric\)\n\n\| Article \| Word Count \| Points \| Score \(5\.0\) \| Verdict \|\n\|---------\|------------\|--------\|-------------\|---------\|\n((?:\|.*?\n)+)', content)
    if summary_table_match:
        rows = summary_table_match.group(1).split('\n')
        new_rows = []
        for i, row in enumerate(rows):
            if not row.strip() or "**Average**" in row:
                continue
            cols = row.split('|')
            if len(cols) >= 6:
                cols[3] = f" {pts[i]} "
                cols[4] = f" {scr[i]:.1f} "
                new_rows.append("|".join(cols))
        
        # Get average word count
        avg_wc = "0"
        wc_match = re.search(r'\| \*\*Average\*\* \| \*\*(\d+)\*\*', content)
        if wc_match: avg_wc = wc_match.group(1)
        
        new_rows.append(f"| **Average** | **{avg_wc}** | **{avg_pts}** | **{avg_scr:.1f}** | |")
        new_table_body = "\n".join(new_rows)
        content = content.replace(summary_table_match.group(1), new_table_body + "\n")

    # Update Footer
    content = re.sub(r'\*\*Actual: [\d\.]+/5\*\*', f"**Actual: {avg_scr:.1f}/5**", content)
    content = content.replace("Formula used: `Score = (Points ÷ 60) × 5`", "Formula used: `Score = (Points ÷ 80) × 5`")
    content = content.replace("Formula used: `Score = (Points ÷ 88) × 5`", "Formula used: `Score = (Points ÷ 80) × 5`")

    with open(filepath, 'w') as f:
        f.write(content)

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
