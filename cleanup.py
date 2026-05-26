import re
import os

def update_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Remove the duplicated old summary table if it exists
    # It usually starts with | Article | Word Count | and is followed by Average
    # But specifically looking for the one that has the old values (approx 40-50 pts)
    
    pattern = r'\n\| Article \| Word Count \| Points \| Score \(5\.0\) \| Verdict \|[\s\S]*?\| \*\*Average\*\* \|[\s\S]*?\n\n---\n\n## Summary Table'
    content = re.sub(pattern, "\n\n---\n\n## Summary Table", content)

    # Also remove any triple dashes followed by empty space then another triple dash
    content = re.sub(r'---\n\n\n\n---', "---\n", content)
    content = re.sub(r'---\n\n\s*\n\n---', "---\n", content)
    
    # Fix the duplicated summary table specifically for the format I saw
    content = re.sub(r'\| Article \| Word Count \| Points \| Score \(5\.0\) \| Verdict \|[\s\S]*?\| \*\*Average\*\* \|[\s\S]*?\n\n---\n\n## Summary Table', "## Summary Table", content)

    # Let's try a very specific one for the duplication I saw
    bad_table_pattern = r'\| Article \| Word Count \| Points \| Score \(5\.0\) \| Verdict \|---------[\s\S]*?\| \*\*Average\*\* \| \*\*506\*\* \| \*\*50\.3\*\* \| \*\*4\.2\*\* \| \|'
    content = re.sub(bad_table_pattern, "", content)

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
