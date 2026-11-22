---
title: Coding Agent Input Modalities (Image, PDF, Video, Voice)
purpose: Cross-vendor comparison of what input coding agents and harnesses document accepting — images, PDF, video and voice — with each cell sourced to the vendor's own docs.
created: 2026-11-22
updated: 2026-11-22
validated_links: 2026-11-22
status: assess
---

**Details:** Every cell was read from the vendor's own docs on 2026-11-22 and re-checked in a
second pass the same day. Nothing here was run. A cell says what the **harness documents**, not
what the underlying model can do: a model that accepts video says nothing about whether a command
line interface (CLI) or integrated development environment (IDE) lets you attach one. "not documented
(checked 2026-11-22)" means the sentence was not found on the vendor pages listed in
[Sources](#sources), not that the feature is absent.

## What It Is

Coding agents differ in how a screenshot, a spec PDF or a screen recording gets to the model. Some
expose a flag or a clipboard shortcut; some only pass files through a read tool; some say nothing.
Rows are the well-known harnesses that already have a profile in this corpus. Claude Code image and
PDF handling is covered in depth in
[Read Tool: PDF & Image Parsing](../../cc-native/plugins-ecosystem/CC-web-scraping-plugins-analysis.md#read-tool-pdf--image-parsing)
and image token cost in
[Claude Code Image Token Economics](../../cc-community/CC-vlm-screen-sharing-landscape.md#claude-code-image-token-economics).

## Input by harness

| Harness | Image | PDF | Video | Voice |
|---|---|---|---|---|
| Claude Code ([CLI reference](../../cc-native/configuration/CC-cli-reference.md)) | Drag and drop, `Ctrl+V` paste (`Alt+V` on Windows and WSL), or a path in the prompt ([workflows][cc-workflows]); the Read tool returns PNG, JPEG, GIF, WebP as visual content ([tools][cc-tools]) | Read tool reads short PDFs whole; over 10 pages, a `pages` range of up to 20 pages, rendered with poppler's `pdftoppm` ([tools][cc-tools]) | not documented (checked 2026-11-22) | `/voice` dictation into the prompt; needs a claude.ai sign-in, not API-key or cloud-provider auth ([voice][cc-voice]) |
| [Codex CLI](codex-cli-analysis.md) | Paste into the composer, or `--image`/`-i` with comma-separated or repeated paths ([image inputs][codex-img], [commands][codex-cmds]) | not documented (checked 2026-11-22) | not documented (checked 2026-11-22) | `/voice` or F8 starts a voice conversation, in a terminal build that supports voice ([commands][codex-cmds]) |
| [Gemini CLI](gemini-cli-analysis.md) | `read_file` "Supports text, images, audio, and PDF"; clipboard image paste not documented (checked 2026-11-22) ([file tools][gemini-fs], [shortcuts][gemini-keys]) | Same `read_file` line ([file tools][gemini-fs]) | not documented (checked 2026-11-22); the same line lists audio, not video | Hold `Space` to speak in Voice Mode ([shortcuts][gemini-keys]) |
| [GitHub Copilot CLI](../agents/github-copilot-cli-analysis.md) | `Alt+V` pastes an image from the clipboard as an attachment; `--attachment PATH` accepts image files if the model and organisation policy allow vision ([CLI reference][copilot-cli]) | not documented (checked 2026-11-22) | not documented (checked 2026-11-22) | `/voice` toggles voice mode and picks the microphone; `Ctrl+Space` toggles dictation ([CLI reference][copilot-cli]) |
| [VS Code Copilot Chat](vscode-copilot-chat-analysis.md) | Attach images such as screenshots or UI mockups as context, with a "Mark Up" crop and draw step ([agent mode][vscode-agent]) | not documented (checked 2026-11-22) | not documented (checked 2026-11-22) | Voice Mode (experimental) listens for follow-ups and reads answers aloud ([agent mode][vscode-agent]) |
| [Cursor](cursor-analysis.md) | Attach, drag and drop into the chat input, or `Cmd+V` paste including screenshots ([prompting][cursor-prompt]); the Read tool also supports image files ([overview][cursor-overview]) | not documented (checked 2026-11-22) | not documented (checked 2026-11-22) | Dictation turns speech into text in the chat input ([voice chat][cursor-voice]) |
| [Cline](cline-analysis.md) | Drag files into chat; images need a multimodal model; paste not documented (checked 2026-11-22) ([working with files][cline-files]) | "images, PDFs, CSVs, and Excel files from your file system" ([working with files][cline-files]) | not documented (checked 2026-11-22) | not documented (checked 2026-11-22) |
| [Aider](aider-analysis.md) | `/add <file>`, `/paste` from the clipboard, or filenames on the command line ([images][aider-img]) | not documented (checked 2026-11-22) | not documented (checked 2026-11-22) | `/voice`, then Enter to stop; transcribed as if typed ([voice][aider-voice]) |
| [OpenCode](opencode-analysis.md) | The Read tool passes PNG, JPEG, GIF and WebP to the model, up to 20 MiB; paste and drag not documented (checked 2026-11-22) ([tools][oc-tools], [TUI][oc-tui]) | Read tool passes PDF, same 20 MiB limit ([tools][oc-tools]) | not documented (checked 2026-11-22) | not documented (checked 2026-11-22) |
| [Amp](amp-analysis.md) | Attachment button, drag into the composer, or paste from the clipboard ([files and attachments][amp-files]) | "Amp can inspect images, PDFs, audio, and video directly" ([files and attachments][amp-files]) | Same line; also lists transcribing or summarising audio and video ([files and attachments][amp-files]) | The Amp apps add "dictation" ([manual][amp-manual]) |
| [Windsurf](windsurf-analysis.md) | not documented (checked 2026-11-22) | not documented (checked 2026-11-22) | not documented (checked 2026-11-22) | Cascade voice input transcribes speech to text ([Cascade][windsurf-cascade]) |
| [Kiro](kiro-analysis.md) | CLI: `/paste`, a path in the prompt, or drag into the terminal; JPEG, PNG, GIF, WebP, under 10 MB, up to 10 per request ([CLI images][kiro-img]) | not documented (checked 2026-11-22) | not documented (checked 2026-11-22) | CLI voice mode: speak prompts instead of typing ([voice][kiro-voice]) |
| [Zed](zed-analysis.md) | Drag from the file system into the Agent Panel, or paste, for providers with vision models ([agent panel][zed-panel]) | not documented (checked 2026-11-22) | not documented (checked 2026-11-22) | not documented (checked 2026-11-22) |
| [Kimi Code](kimi-code-analysis.md) | `Ctrl-V` (`Alt-V` on Windows) pastes images; needs the `image_in` model capability ([interaction][kimi-int]) | not documented (checked 2026-11-22) | Pastes video too, needs `video_in`; the docs call it "a distinctive Kimi Code capability" (vendor claim) ([interaction][kimi-int]) | not documented (checked 2026-11-22) |
| [Antigravity](antigravity-analysis.md) | CLI: `Ctrl+V` pastes PNG, JPEG, GIF, WebP, BMP, TIFF, SVG ([CLI prompting][ag-prompt]); app: camera button adds a browser screenshot ([screenshots][ag-shots]) | not documented (checked 2026-11-22) | CLI: pasted MP4, MOV, WebM, AVI ([CLI prompting][ag-prompt]) | Voice mode: talk to the agent and hear replies, built on Gemini Live ([voice mode][ag-voice]) |

## Notes

- **Three styles of image input.** Claude Code, Codex CLI, Aider, Copilot CLI, Kiro CLI and Antigravity
  CLI give terminal users an explicit path (clipboard shortcut, flag or command). Gemini CLI and
  OpenCode document image handling only at the file-read tool, so an image reaches the model when the
  agent reads a path. Editor-based tools (Cursor, Zed, VS Code, Cline) use drag-and-drop or attach.
- **PDF is the thinnest column.** Only Claude Code, Gemini CLI, Cline, OpenCode and Amp document it,
  and mostly as a file-read behaviour; Claude Code is the one that documents page ranges and a
  rendering dependency.
- **Video is documented by three harnesses.** Amp (audio and video inspected directly), Kimi Code
  (pasted video, gated by `video_in`) and Antigravity CLI (four container formats). Gemini CLI lists
  audio but not video in its file tools.
- **Voice is input to the prompt, not media.** Most rows document dictation or a voice mode; Claude
  Code's needs a claude.ai sign-in, Kiro's is stated to transcribe on the user's machine, and
  Antigravity's and Codex's are conversational.
- **Gating by model and policy.** Copilot CLI, Kimi Code and Cline each say image or video use needs
  a capable model; Copilot CLI adds organisation policy. A documented harness path does not mean the
  selected model will accept the input.
- **Windsurf docs moved.** `docs.windsurf.com` redirects to `docs.devin.ai`; no image page was found
  there, so its image cell stays undocumented rather than inferred.

## Sources

| Source | Established |
|---|---|
| [Claude Code: work with images][cc-workflows] | Drag, paste, path |
| [Claude Code: tools reference][cc-tools] | Read tool images and PDFs |
| [Claude Code: voice dictation][cc-voice] | `/voice`, account requirement |
| [Codex: image inputs][codex-img] | Paste, `--image` |
| [Codex: developer commands][codex-cmds] | `--image` flag, `/voice`, F8 |
| [Gemini CLI: file tools][gemini-fs] | `read_file` text, images, audio, PDF |
| [Gemini CLI: keyboard shortcuts][gemini-keys] | Voice Mode, generic paste |
| [Copilot CLI reference][copilot-cli] | `Alt+V`, `--attachment`, `/voice` |
| [VS Code: agent mode][vscode-agent] | Image attach, Mark Up, Voice Mode |
| [Cursor: prompting][cursor-prompt] | Attach, drag, paste |
| [Cursor: agent overview][cursor-overview] | Read tool image formats |
| [Cursor: voice chat][cursor-voice] | Dictation |
| [Cline: working with files][cline-files] | Drag, images, PDFs |
| [Aider: images and URLs][aider-img] | `/add`, `/paste` |
| [Aider: voice][aider-voice] | `/voice` |
| [OpenCode: tools][oc-tools] | Read tool PNG, JPEG, GIF, WebP, PDF |
| [OpenCode: TUI][oc-tui] | `@` file attach only |
| [Amp: files and attachments][amp-files] | Images, PDFs, audio, video |
| [Amp manual][amp-manual] | Dictation in apps |
| [Windsurf Cascade (Devin docs)][windsurf-cascade] | Voice input |
| [Kiro CLI: images][kiro-img] | Paste, path, drag, limits |
| [Kiro CLI: voice][kiro-voice] | Voice mode |
| [Zed: agent panel][zed-panel] | Drag, paste, vision providers |
| [Kimi Code: interaction][kimi-int] | Image and video paste |
| [Antigravity CLI: prompting][ag-prompt] | Image and video paste, formats |
| [Antigravity: screenshots][ag-shots] | Browser screenshot button |
| [Antigravity: voice mode][ag-voice] | Voice conversation |

[cc-workflows]: https://code.claude.com/docs/en/common-workflows
[cc-tools]: https://code.claude.com/docs/en/tools-reference
[cc-voice]: https://code.claude.com/docs/en/voice-dictation
[codex-img]: https://learn.chatgpt.com/docs/image-inputs
[codex-cmds]: https://learn.chatgpt.com/docs/developer-commands?surface=cli
[gemini-fs]: https://geminicli.com/docs/tools/file-system/
[gemini-keys]: https://geminicli.com/docs/reference/keyboard-shortcuts/
[copilot-cli]: https://docs.github.com/en/copilot/reference/cli-command-reference
[vscode-agent]: https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode
[cursor-prompt]: https://cursor.com/docs/agent/prompting
[cursor-overview]: https://cursor.com/docs/agent/overview
[cursor-voice]: https://cursor.com/docs/agent/voice-chat
[cline-files]: https://docs.cline.bot/core-workflows/working-with-files.md
[aider-img]: https://aider.chat/docs/usage/images-urls.html
[aider-voice]: https://aider.chat/docs/usage/voice.html
[oc-tools]: https://opencode.ai/docs/tools/
[oc-tui]: https://opencode.ai/docs/tui/
[amp-files]: https://ampcode.com/docs/orbs/files-and-attachments
[amp-manual]: https://ampcode.com/manual
[windsurf-cascade]: https://docs.devin.ai/desktop/cascade/cascade
[kiro-img]: https://kiro.dev/docs/cli/chat/images/
[kiro-voice]: https://kiro.dev/docs/cli/voice/
[zed-panel]: https://zed.dev/docs/ai/agent-panel
[kimi-int]: https://moonshotai.github.io/kimi-code/en/guides/interaction.html
[ag-prompt]: https://antigravity.google/docs/cli/prompting/
[ag-shots]: https://antigravity.google/docs/screenshots/
[ag-voice]: https://antigravity.google/docs/voice-mode/
