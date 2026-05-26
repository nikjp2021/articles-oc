# Multi-Agent Content Pipeline (2026 Edition)

A professional, industrial-grade social media content production pipeline powered by specialized AI agents. This system is optimized for **accuracy**, **citation fidelity**, and **platform-native engagement**.

## 🚀 The Pipeline Architecture (6-Phase Antigenic Flow)

The pipeline follows a strict sequential flow to ensure zero-loss context transfer:

1.  **Phase 0: Research (SHARP Handoff)** - `article-researcher` conducts a 3-minute budgeted search and produces a **Typed Citation Schema** (C1, C2...).
2.  **Phase 1: Write** - `business-article-writer` consumes the research brief using **Dual-Anchor Prompting** to produce 4 platform-optimized articles (LinkedIn, Facebook, Threads, Instagram).
3.  **Phase 2: Organize** - `article-organizer` packages the articles and research brief into dated topic folders.
4.  **Phase 3: Enrich** - `article-enricher` generates platform-specific AI image prompts with alt text.
5.  **Phase 4: Review** - `article-reviewer` performs a **Citation Audit** and **Slop Detection** against the 13-Criteria Hybrid Rubric.
6.  **Phase 5: Metrics** - Final performance and timing data are logged.

## 📄 The "Standard 8" File Structure

Every successful pipeline run produces exactly 8 files in a topic-specific folder:

1.  **Li-[Topic].md**: LinkedIn (Authoritative/Thought Leadership)
2.  **Fb-[Topic].md**: Facebook (Relatable/Community)
3.  **Th-[Topic].md**: Threads (Raw/Authentic)
4.  **Ig-[Topic].md**: Instagram (Educational Carousel)
5.  **Research-Brief-[Topic].md**: The "Source of Truth" with the Citation Schema.
6.  **assets-[Date].md**: AI Image Prompts & Alt Text.
7.  **review-[Date].md**: Editorial Audit & Rubric Scores.
8.  **pipeline-metrics-[Date].md**: Execution timing and word counts.

## 🛠 The SHARP Handoff Protocol

To solve the "vague citation" problem common in AI pipelines, this system implements the **SHARP (Structured Handoff for Accurate Research Preservation)** protocol:
*   **Typed Schema**: Research is passed as a table, not prose.
*   **Dual-Anchoring**: The writer is anchored to the schema at both the top and bottom of the context window.
*   **Citation Audit**: The reviewer cross-references every claim against the research ID (C1, C2).

## 🤖 Specialized Agents (located in `.opencode/agents/`)

*   **`article-researcher`**: Web-retrieval and data-structuring specialist.
*   **`business-article-writer`**: Platform-tone expert and copywriter.
*   **`article-organizer`**: Content operations and file management specialist.
*   **`article-enricher`**: Visual strategist and prompt engineer.
*   **`article-reviewer`**: Quality control and factual consistency auditor.

## 📝 Usage

To trigger the pipeline, provide a topic to the system:
*"Execute the full 6-phase pipeline for the topic: [Your Topic]"*

---
*Powered by opencode.*
