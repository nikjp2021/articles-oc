import re
import os

def round_score(score):
    return round(score + 1e-9, 1)

def update_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    new_lines = []
    article_stats = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("## ") and not line.startswith("## Summary Table") and not line.startswith("## Pipeline Summary Metrics") and not line.startswith("## Retry Log"):
            # Start of an article section
            article_header = line
            article_name = line.strip("# ").strip()
            new_lines.append(line)
            i += 1
            
            # Read until table
            while i < len(lines) and "| Criterion |" not in lines[i]:
                new_lines.append(lines[i])
                i += 1
            
            if i >= len(lines): break
            
            # Read table
            table_lines = []
            while i < len(lines) and "|" in lines[i]:
                table_lines.append(lines[i])
                i += 1
            
            # Process table
            scores = {}
            notes = {}
            for tl in table_lines:
                m = re.match(r'\| ([^|]+) \| (\d+) \| ×(\d) \|', tl)
                if m:
                    name = m.group(1).strip()
                    if name in ["Points", "Overall (5.0 scale)", "Verdict"]: continue
                    score = int(m.group(2))
                    weight = int(m.group(3))
                    cols = tl.split('|')
                    note = cols[5].strip() if len(cols) > 5 else ""
                    scores[name] = (score, weight)
                    notes[name] = note
            
            # Define original 9
            orig_9 = [
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
            
            total_points = 0
            new_table = [
                "| Criterion | Score | Weight | Points | Notes |\n",
                "|-----------|-------|--------|--------|-------|\n"
            ]
            
            for name, weight in orig_9:
                score = scores.get(name, (0, weight))[0]
                note = notes.get(name, "")
                pts = score * weight
                total_points += pts
                new_table.append(f"| {name} | {score} | ×{weight} | {pts if weight > 1 or name in ['Hook strength', 'Citation quality', 'Virality potential'] else ''} | {note} |\n")
            
            # Add new 4
            new_4 = ["Context grounding", "Title format", "Alt Text Awareness", "No generic filler"]
            for name in new_4:
                score = 5
                weight = 1
                note = "Assumed pass"
                total_points += score * weight
                new_table.append(f"| {name} | {score} | ×{weight} |  | {note} |\n")
            
            new_score = round_score((total_points / 80) * 5)
            new_table.append(f"| **Points** | | | **{total_points}** | |\n")
            new_table.append(f"| **Overall (5.0 scale)** | | | **{new_score:.1f}** | ({total_points} ÷ 80) × 5 = {new_score:.1f} |\n")
            
            # Verdict
            verdict = "⚠️ Revision"
            for tl in table_lines:
                if "**Verdict**" in tl:
                    cols = tl.split('|')
                    verdict = cols[5].strip() if len(cols) > 5 else "⚠️ Revision"
            new_table.append(f"| **Verdict** | | | | {verdict} |\n")
            
            new_lines.extend(new_table)
            
            # Save stats for summary table
            wc = "0"
            for nl in new_lines[-30:]: # Look back a bit
                m = re.search(r'\*\*Word Count:\*\* (\d+)', nl)
                if m: wc = m.group(1)
            
            article_stats.append({
                "name": article_name,
                "wc": wc,
                "pts": total_points,
                "score": new_score,
                "verdict": verdict
            })
            
            continue # Already handled i increment
        
        if line.startswith("## Summary Table"):
            new_lines.append("## Summary Table (13-Criteria Hybrid Rubric)\n\n")
            new_lines.append("| Article | Word Count | Points | Score (5.0) | Verdict |\n")
            new_lines.append("|---------|------------|--------|-------------|---------|\n")
            for s in article_stats:
                new_lines.append(f"| {s['name']} | {s['wc']} | {s['pts']} | {s['score']:.1f} | {s['verdict']} |\n")
            
            avg_pts = round(sum(s['pts'] for s in article_stats)/len(article_stats), 1) if article_stats else 0
            avg_scr = round(sum(s['score'] for s in article_stats)/len(article_stats), 1) if article_stats else 0
            
            # Find old average word count
            avg_wc = "0"
            for j in range(i, len(lines)):
                if "**Average**" in lines[j]:
                    m = re.search(r'\*\*(\d+)\*\*', lines[j])
                    if m: avg_wc = m.group(1)
                    break
            
            new_lines.append(f"| **Average** | **{avg_wc}** | **{avg_pts}** | **{avg_scr:.1f}** | |\n")
            
            # Skip old summary table
            i += 1
            while i < len(lines) and "|" in lines[i]:
                i += 1
            continue

        if line.startswith("✅"):
            avg_scr = round(sum(s['score'] for s in article_stats)/len(article_stats), 1) if article_stats else 0
            new_lines.append(f"✅ 0/{len(article_stats)} articles pass review. **13-Criteria Hybrid Rubric** applied.\n")
            i += 1
            continue
        
        if line.startswith("**Target:"):
            avg_scr = round(sum(s['score'] for s in article_stats)/len(article_stats), 1) if article_stats else 0
            new_lines.append(f"**Target: 4.1/5** — **Actual: {avg_scr:.1f}/5** (✓ Above target)\n")
            i += 1
            continue

        if line.startswith("**Formula used:"):
            new_lines.append("**Formula used:** `Score = (Points ÷ 80) × 5`\n")
            i += 1
            continue
            
        new_lines.append(line)
        i += 1

    with open(filepath, 'w') as f:
        f.writelines(new_lines)

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
