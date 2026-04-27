# GenericAgent

<div align="center">
<img src="assets/images/bar.jpg" width="880"/>

<a href="https://trendshift.io/repositories/25944" target="_blank"><img src="https://trendshift.io/api/badge/repositories/25944" alt="lsdefine%2FGenericAgent | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>

</div>

<p align="center">
  <a href="#english">English</a> | <a href="#chinese">中文</a> | 📄 Technical Report:&nbsp;<a href="https://arxiv.org/abs/2604.17091"><img src="https://img.shields.io/badge/arXiv-2604.17091-b31b1b?logo=arxiv&logoColor=white" alt="arXiv" height="18"/></a>&nbsp;<a href="assets/GenericAgent_Technical_Report.pdf"><img src="https://img.shields.io/badge/-PDF-EA4335?logo=adobeacrobatreader&logoColor=white" alt="Technical Report PDF" height="18"/></a>&nbsp;<a href="https://github.com/JinyiHan99/GA-Technical-Report"><img src="https://img.shields.io/badge/-Code%20%26%20Data-181717?logo=github&logoColor=white" alt="Experiments & Reproduction Repo" height="18"/></a> | 📘 <a href="https://datawhalechina.github.io/hello-generic-agent/">教程</a>
</p>

---
<a name="english"></a>
## 🌟 Overview

**GenericAgent** is a minimal, self-evolving autonomous agent framework. Its core is just **~3K lines of code**. Through **9 atomic tools + a ~100-line Agent Loop**, it grants any LLM system-level control over a local computer — covering browser, terminal, filesystem, keyboard/mouse input, screen vision, and mobile devices (ADB).

Its design philosophy: **don't preload skills — evolve them.**

Every time GenericAgent solves a new task, it automatically crystallizes the execution path into an skill for direct reuse later. The longer you use it, the more skills accumulate — forming a skill tree that belongs entirely to you, grown from 3K lines of seed code.

> **🤖 Self-Bootstrap Proof** — Everything in this repository, from installing Git and running `git init` to every commit message, was completed autonomously by GenericAgent. The author never opened a terminal once.

> **📝 Personal Note** — I'm using this fork primarily to experiment with Gemini integration and to study the self-evolution mechanism. The skill crystallization approach is particularly interesting to me.
>
> **🔧 My Setup** — Running with `gemini-2.5-pro` as the primary model. I've found it handles multi-step browser tasks well. Will document findings as I go.
>
> **📊 Gemini Observations so far:**
> - `gemini-2.5-pro` works well for reasoning-heavy tasks but can be slower on simple ones
> - `gemini-2.0-flash` is a good fallback for speed-sensitive tasks — roughly 3–4x faster
> - Skill reuse rate noticeably improves after ~20 tasks; the skill tree starts paying off

## 📋 Core Features
- **Self-Evolving**: Automatically crystallizes each task into an skill. Capabilities grow with every use, forming your personal skill tree.
- **Minimal Architecture**: ~3K lines of core code. Agent Loop is ~100 lines. No complex dependencies, zero deployment overhead.
- **Strong Execution**: Injects into a real browser (preserving login sessions). 9 atomic tools take direct control of the system.
- **High Compatibility**: Supports Claude / Gemini / Kimi / MiniMax and other major models. Cross-platform.
- **Token Efficient**: <30K context window — a fraction of the 200K–1M other agents consume. 
