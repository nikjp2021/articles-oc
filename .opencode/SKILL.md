---
name: Assistant_Method
description: My (opencode assistant) global operating guidelines — pipeline orchestration, mistake learning log, and session metrics. I read this before every complex task.
---

# Assistant Method & Orchestration

## 🔁 Mistake Learning Log

| Date | Mistake | Fix Applied | Prevented By |
|------|---------|-------------|--------------|
| 21-05-2026 | Called nonexistent tool `tool` instead of `task` when invoking business-article-writer | Added tool-name verification before every tool call | N/A — first occurrence |
| 21-05-2026 | General subagent treated "Run the business-article-writer" as self-instruction instead of delegation | Switched to self-contained prompts that include all specs inline — no delegation needed | Invocation section |
| 21-05-2026 | Added article-researcher as Step 0 of pipeline | New agent, updated writer pipeline to 5 steps, updated metrics table, added research brief to post-flight | N/A — new feature |
| 25-05-2026 | Overlap check searched external/tmp directories | Updated Section 1 to mandate "Current Project Directory Only" | User feedback |
| 25-05-2026 | Used `general` subagent for dedicated agents (article-reviewer, etc.) | Must use `subagent_type: article-reviewer` (or dedicated type) instead of `general` for all delegated agents | User feedback |
| 26-05-2026 | Used 9-criteria rubric instead of the 13-criteria standard used elsewhere | Updated article-reviewer and business-article-writer to 13-criteria (80 points) format; backfilled existing review files | User feedback |
| 26-05-2026 | Phase 0 delegation failed (writer self-performed research) | Fixed `business-article-writer.md` Phase 0 to use clean Task tool delegation with minimal inline logic before the call | N/A — first occurrence |
| 26-05-2026 | Subagents ignored 13-criteria rubric despite agent definition | Added "MANDATORY" language and explicit point formula to Task prompts to override subagent "stickiness" | N/A — first occurrence |

**Rules:**
- Before any tool call, verify the name matches an available tool. If not, correct before invoking.
- When delegating to a subagent via Task tool, the prompt must use "Invoke [agent] via Task tool" language — never "Run" or "Act as". This prevents the general agent from treating delegation instructions as self-instructions.
- **CRITICAL**: When invoking a dedicated agent (article-researcher, article-reviewer, article-enricher, article-organizer, business-article-writer), use its exact `subagent_type` name in the Task tool. Never use `general` for dedicated agents — they have their own autonomous instructions.

---

## 1. Pre-flight Topic Overlap Check

Before calling `business-article-writer`, check for topic overlap with existing articles. **CRITICAL: Search ONLY the current project directory.**

**Procedure:**
1. Extract 2-3 keywords from proposed topic
2. Glob all existing article files in the current directory: `glob "art-*/**/*.md"` (do NOT search external or temporary directories)
3. Compute word overlap: count shared non-stop words between proposed title and each existing title
4. If any existing article has ≥60% shared words → flag to user:
   ```
   ⚠️ Topic overlap detected:
   Proposed: "[your topic]"
   Existing: "[existing title]" in art-DD-MM-YYYY/Topic-Name/
   Word overlap: ~XX%
   Continue anyway? (y/n)
   ```
5. If user says no → pick a fresh angle or stop

**Stop words to ignore:** a, an, the, is, it, in, on, of, to, for, and, or, but, what, why, how, does, are, do, you, your, we, our, they, their, its, that, this, with, from, will, can, not

**Fallback:** If glob finds no existing articles, skip check.

---

## 2. Invocation

Do NOT rely on the subagent having Task tool access (inconsistent). Instead, give it a **self-contained prompt** that includes everything it needs:

Before sending:

- [ ] Pre-flight overlap check passed (or user overrode)
- [ ] Topic is clearly defined with 2-3 specific angles
- [ ] Context grounding included: specific event, date, statistic, or location that anchors the topic in the present moment
- [ ] CSV source referenced if applicable
- [ ] Research brief option: include "first invoke article-researcher via Task tool" if user wants current viral content research
- [ ] Platform specs included: Li tone, Fb tone, Th tone, Ig tone
- [ ] Review criteria embedded: 13-Criteria Hybrid Rubric (hook×2, citation×2, virality×2, tone fit×1, tone diff×1, emoji×1, structure×1, length×1, visual/formatting×1, context grounding×1, title format×1, alt text×1, no filler×1) — 1-5 weighted scale, formula: (Points÷80)×5
- [ ] Organization instruction: name files Li-*.md / Fb-*.md / Th-*.md / Ig-*.md, after writing verify files
- [ ] permission:
  read: allow
  write: allow
  edit: allow
  grep: allow
  glob: allow
  bash: allow
  task: allow
- [ ] Clear output expectation: create all files, then report summary with word counts

---

## 3. Post-flight Verification

After `business-article-writer` Task returns:

| # | Check | How |
|---|-------|-----|
| 1 | Target folder exists | `ls art-DD-MM-YYYY/Topic-Name/` |
| 2 | Exactly 4 article files present | `ls art-*/Topic-Name/*.md | wc -l` (should be 4+) |
| 3 | All files have `.md` extension | `find art-*/ -type f ! -name "*.md"` (should be empty) |
| 4 | `pipeline-metrics-*.md` exists and has data | Check file non-empty |
| 5 | `review-*.md` exists and verdict is Pass | Check for "✅ Pass" or "HARD FAIL" |
| 6 | `assets-*.md` exists | Check file exists |
| 7 | No loose extensionless files in root | `find . -maxdepth 1 -type f ! -name "*.md"` |

**If any check fails:**
```
❌ Post-flight check failed: [check #] — [details]
Retry? (y/n)
```
If user approves, invoke writer again with same prompt.
If declines, surface the partial state.

---

## 4. Retry Protocol

| Scenario | Action |
|----------|--------|
| Task tool times out | Surface timeout, retry once on approval |
| Tool name error (called wrong tool) | Log to mistake log, correct tool name, retry |
| Subagent returns asking for input ("What topic...") instead of executing pipeline | Prompt insufficient. Retry with self-contained prompt that includes all specs (tone, criteria, file naming) |
| Post-flight check fails | Show which checks failed, retry once on approval |
| Second attempt fails | Recommend manual intervention, do not retry |
| Reviewer returns HARD FAIL | Surface scores + criterion, ask user: manual edit or abandon? |

**Rule:** Never silently retry. Always tell the user.

---

## 5. Edge Case Catalog

| Scenario | Handling |
|----------|----------|
| Topic folder already exists for today | Flag: "Topic [X] already written today. Write another angle or pick a new topic?" |
| No CSV / vague topic | Ask for 2-3 specific questions or angles before proceeding |
| User wants 1-2 platforms only | Pass through to writer verbatim |
| Writer returns < 4 articles | Flag count mismatch. Post-flight check #2 catches this |
| Subagent asks "What topic?" instead of executing | Prompt too vague — retry with self-contained prompt including all specs inline |
| Extensionless files found | Rename to `.md` before next pipeline step |
| Multiple topics in one message | Process sequentially — one pipeline per topic |
| User doesn't approve retry | Surface current state, ask what to do next |

---

## 6. Session Metrics

After each pipeline completes, append a row below. Append-only.

**Format:**
| HH:MM | Topic | Pre-flight | Retries | Post-flight | Duration | Avg Score | Words |
| Time | topic-slug | result | N | X/7 | X.X min | X.X | XXXX |

**Session Log:**

| Time | Topic | Pre-flight | Retries | Post-flight | Duration | Avg Score | Words |
|------|-------|------------|---------|-------------|----------|-----------|-------|
| 06:08 | Desk-Plants-Biophilic-Productivity | ⚠️ skipped | 0 | 6/6 | 1.8 min | 4.3 | 1464 |
| 07:15 | Social-Media-Algorithms | ⚠️ skipped | 0 | 6/6 | 5.2 min | 4.9 | 1923 |
| 08:36 | Billionaire-Space-Race | ✅ no overlap | 0 | 7/7 | 1.3 min | 4.9 | 2788 |
| 09:44 | Global-South-AI | ✅ no overlap | 0 | 7/7 | 1.4 min | 4.4 | 1812 |
| 10:20 | Socratic-Method-AI-Age | ✅ no overlap | 0 | 7/7 | 20.0 min | 4.7 | 2362 |
| 09:55 | Paradox-Choice | ✅ no overlap (test) | 0 | 7/7 | ~1.5 min | 4.4 | 2578 |

| 13:52 | Fear-Vs-Learning | ✅ no overlap | 0 | 7/7 | ~1.5 min | 4.8 | 1916 |
| 11:41 | Remote-Work-Hybrid | ✅ no overlap | 0 | 7/7 | ~3 min | 4.6 | 1532 |
| 02:55 | Renewable-Energy-Storage | ✅ no overlap | 0 | 7/7 | 5.5 min | 4.9 | 2221 |
| 03:15 | Opencode-Vs-IDE-Agents | ✅ no overlap | 0 | 7/7 | 7.3 min | 4.9 | 2162 |
| 04:00 | Gemini-Student-Tier | ✅ no overlap | 2 | 7/7 | 9.8 min | 4.4 | 2287 |
