---
title: Coding Agents and Harnesses Compared
purpose: "Coding agents and harnesses compared from their own docs: input, media processing, configuration and policy, billing, compaction; each cell sourced and dated."
created: 2026-11-22
updated: 2026-11-27
validated_links_on: 2026-11-22
status: assess
---

**Details:** Every cell was read from the vendor's own docs on 2026-11-22 and re-checked in a
second pass the same day; sections added later carry their own read date. Nothing here was run. A cell says what the **harness documents**, not
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
| Claude Code ([CLI reference](../../cc-native/configuration/CC-cli-reference.md)) | Drag and drop, `Ctrl+V` paste (`Alt+V` on Windows and WSL), or a path in the prompt ([workflows][cc-workflows]); the Read tool returns PNG, JPEG, GIF, WebP as visual content ([tools][cc-tools]) | Read tool reads PDFs, with page ranges for long ones ([tools][cc-tools]; detail in [Read Tool: PDF & Image Parsing](../../cc-native/plugins-ecosystem/CC-web-scraping-plugins-analysis.md#read-tool-pdf--image-parsing)) | not documented (checked 2026-11-22) | `/voice` dictation into the prompt; needs a claude.ai sign-in, not API-key or cloud-provider auth ([voice][cc-voice]) |
| [Codex CLI](codex-cli-analysis.md) | Paste into the composer, or `--image`/`-i` with comma-separated or repeated paths ([image inputs][codex-img], [commands][codex-cmds]) | not documented (checked 2026-11-22) | not documented (checked 2026-11-22) | `/voice` or F8 starts a voice conversation, in a terminal build that supports voice ([commands][codex-cmds]) |
| [Gemini CLI](gemini-cli-analysis.md) | `read_file` "Supports text, images, audio, and PDF"; clipboard image paste not documented (checked 2026-11-22) ([file tools][gemini-fs], [shortcuts][gemini-keys]) | Same `read_file` line ([file tools][gemini-fs]) | not documented (checked 2026-11-22); the same line lists audio, not video, though the code accepts video (see [Where media is processed](#where-media-is-processed)) | Hold `Space` to speak in Voice Mode ([shortcuts][gemini-keys]) |
| [GitHub Copilot CLI](../agents/github-copilot-cli-analysis.md) | JPEG, PNG, GIF, WebP, HEIC and HEIF by `@path`, drag-and-drop or clipboard paste (`Alt+V`), with a model that supports image input ([using Copilot CLI][copilot-cli-use]); `--attachment PATH` in the [CLI reference][copilot-cli] | PDF attachments the same ways ([using Copilot CLI][copilot-cli-use]) | not documented (checked 2026-11-22) | `/voice` toggles voice mode and picks the microphone; `Ctrl+Space` toggles dictation ([CLI reference][copilot-cli]) |
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

## Input notes

- **Three styles of image input.** Claude Code, Codex CLI, Aider, Copilot CLI, Kiro CLI and Antigravity
  CLI give terminal users an explicit path (clipboard shortcut, flag or command). Gemini CLI and
  OpenCode document image handling only at the file-read tool, so an image reaches the model when the
  agent reads a path. Editor-based tools (Cursor, Zed, VS Code, Cline) use drag-and-drop, paste or an
  attach control; see each row for which. A file-read tool counts as documented only for the file types
  its own page names, which is why Cursor's PDF cell stays undocumented.
- **PDF is the thinnest column.** Only Claude Code, Copilot CLI, Gemini CLI, Cline, OpenCode and Amp document it,
  and mostly as a file-read behaviour; Claude Code is the one that documents page ranges.
- **Video is documented by three harnesses.** Amp (audio and video inspected directly), Kimi Code
  (pasted video, gated by `video_in`) and Antigravity CLI (four container formats). Gemini CLI lists
  audio but not video in its file tools.
- **Voice is input to the prompt, not media.** Most rows document dictation or a voice mode; Claude
  Code's needs a claude.ai sign-in, Kiro's is stated to run on the user's machine by default, and
  Antigravity's and Codex's are conversational.
- **Gating by model and policy.** Copilot CLI, Kimi Code, Cline and Zed each say image or video use
  needs a capable model. Copilot CLI's two pages differ on policy: the CLI reference says `--attachment` needs
  the model "and organization policy to allow vision input", while the usage page says attachments
  are "enabled by default, with no policy required". A documented harness path does not mean the
  selected model will accept the input.
- **Windsurf docs moved.** `docs.windsurf.com` redirects to `docs.devin.ai`; no image page was found
  there, so its image cell stays undocumented rather than inferred.

## Where media is processed

[Input by harness](#input-by-harness) and [Input notes](#input-notes) say what each harness accepts.
This section says where the work happens: on the user's machine before the request, or at the model
provider. Evidence is the harness source at a named release tag for the open-source rows, and
first-party docs for the rest, each read 2026-11-27. Nothing was run.

| Harness | Local step (package) | Sent to the model API | PDF handling | Source |
|---|---|---|---|---|
| Claude Code (closed source) | Resizes and recompresses large images before sending (package not documented); for PDFs over 10 pages, renders page ranges with `pdftoppm` from `poppler-utils` | Image blocks; PDF as a document block is not documented for Claude Code | Short PDFs read whole; longer ones in page ranges of up to 20 pages, rendered locally by `pdftoppm`; the API itself, given a PDF, extracts text and renders page images server-side | [Tools reference][cc-tools] (read 2026-11-27); [Claude API: PDF support][claude-pdf] |
| Codex CLI (`rust-v0.172.0`) | Rust `image` crate 0.25.9 (JPEG, PNG, GIF, WebP). PNG, JPEG and WebP within the limits keep their original bytes; GIF is re-encoded to PNG; larger images are resized with a triangle filter to 2048 px longest edge and 2,500 32-pixel patches by default (6000 px and 10,000 patches for "original" detail). The `view_image` tool returns the original bytes as a `data:` URL and leaves resizing to the history step | An image content item (`input_image`) carrying the data URL | No local reader for user PDF files found; `pdf` appears in a PDF artifact plugin and in the web-search tool (screenshots of PDF pages it opens online), not in the file-upload path. The model-info type has no document or video modality (`Text`, `Image`, `Audio` among its input modalities) | `codex-rs/utils/image/Cargo.toml` and `src/lib.rs`; `codex-rs/core/src/tools/handlers/view_image.rs`; `codex-rs/protocol/src/openai_models.rs`, `codex-rs/core-plugins/src/artifact_operation.rs`, `codex-rs/codex-api/src/search.rs` ([release][codex-rel]) |
| Gemini CLI (`v0.71.1`) | None for media: `read_file` reads the bytes, base64-encodes them and takes the MIME type from the `mime` package (file extension) for images, PDF and video, while audio uses an extension allowlist and an unsupported audio file returns an error; no resize | One `inlineData` part (base64 data plus MIME type) for image, PDF, audio and video | Not parsed locally: no PDF package in `packages/core/package.json`; the model API reads the PDF | `packages/core/src/utils/fileUtils.ts`; [release][gemini-rel] |
| OpenCode (`v1.19.6`) | Two read tools in the tree. The one in `packages/opencode` base64-encodes PNG, JPEG, GIF, WebP and PDF into a `data:` attachment with no resize. A newer `packages/core` read tool normalizes images through an image service whose resizer package is the `photon-node` WebAssembly build (`@silvia-odwyer/photon-node`); which tool the shipped binary uses was not traced | A file attachment with a data URL | Passed as an attachment, not parsed locally | `packages/opencode/src/tool/read.ts`; `packages/core/src/tool/read.ts`; `packages/core/src/image.ts` ([release][oc-rel]) |
| Aider (`v0.86.0`) | Reads the file and base64-encodes it, no resize found in the paths read; Pillow is imported in `aider/models.py` and `aider/commands.py` (`ImageGrab` in the `/paste` command); the `models.py` use was not traced | An `image_url` message part with a data URL, only if the model is marked as supporting images or PDFs | Sent as an `image_url` part with a data URL plus a text part naming the PDF file, if the model metadata says it takes PDFs; not parsed locally | `aider/coders/base_coder.py`, `aider/utils.py`, `aider/models.py`, `aider/commands.py`, `requirements/requirements.in` ([release][aider-rel]) |

Cline was not read at source; its row stays in [Input by harness](#input-by-harness).

Model side (read 2026-11-27):

- **GPT-6.2 Astra** (Codex's model in this corpus; see [Codex CLI](codex-cli-analysis.md)): the model
  page lists input "Text, Image", output "Text", and Audio and Video as "Not supported"
  ([GPT-6.2 Astra][oai-astra]). So, on OpenAI's own page, Astra does not take video input; only this model page was checked,
  not whether OpenAI uses the name Astra for another product.
- **OpenAI API, PDFs:** the Responses API extracts text and page images from a PDF and sends both
  to models that take images; other documents get text only ([file inputs][oai-files]).
- **Claude API:** a PDF reaches the model as extracted text plus a page image per page
  ([PDF support][claude-pdf]); images over the model's size limits are downscaled by the API
  ([vision][claude-vision]). Image token numbers are in
  [Claude Code Image Token Economics](../../cc-community/CC-vlm-screen-sharing-landscape.md#claude-code-image-token-economics).
  Neither page lists video.
- **Gemini API:** documents take up to 1,000 PDF pages inline or via the Files API ([document
  processing][gem-doc]); video is a separate input type ([video understanding][gem-vid]). Which model
  Gemini CLI uses by default is not settled by its code: `models.ts` at `v0.71.1` names several
  (`gemini-2.5-pro` as `DEFAULT_GEMINI_MODEL`, `gemini-3.5-flash` as the stable flash tier), so no
  single default-model cell is given.

Findings from the table:

- **Of the open-source harnesses read, Codex CLI is the one with a confirmed local resize path (Rust
  `image` crate), applied to images over its limits.** Gemini CLI and Aider (in the paths read) ship the raw bytes as base64, as does the older OpenCode read
  tool; any downscaling for those happens at the provider API (not verified per provider).
- **PDF parsing is not done locally by any open-source harness read here.** Gemini CLI, OpenCode and
  Aider pass the file through; Codex CLI has no local reader for user PDF files in what was read. The one documented local PDF
  step is Claude Code's page rendering with `pdftoppm`, and only for page-range reads.
- **Gemini CLI's code accepts video, its docs do not.** `fileUtils.ts` at `v0.71.1` classifies `video`
  alongside `image` and `pdf` and sends it as `inlineData`; the [file tools page][gemini-fs] lists audio
  but not video, so the "not documented" cell in [Input by harness](#input-by-harness) understates the code.
- **Inference (ours):** the Claude Code claim in
  [Read Tool: PDF & Image Parsing](../../cc-native/plugins-ecosystem/CC-web-scraping-plugins-analysis.md#read-tool-pdf--image-parsing)
  that cites an issue and system-prompt extracts for `poppler-utils` is only partly backed by Claude Code's own
  tools reference: that doc described poppler as used for text extraction (now corrected there), while the
  tools reference names `pdftoppm`, which renders page images, for page-range reads; the whole-file path for short PDFs has no
  first-party description of where parsing happens.

## Configuration and policy by harness

Where each harness keeps its settings, which layer wins, which environment variables the docs name, what an
administrator can enforce, and how a project overrides the user's defaults. Cells come from each vendor's own
docs page, each read 2026-11-27; nothing was run. "Not documented on the pages read" means the sentence was not
on the pages in [Sources](#sources), not that the feature is absent. MDM is mobile device management; MCP is the Model Context Protocol (MCP), see the [glossary](../../glossary.md). The 11 rows are the harnesses whose configuration pages were read; Kiro, Zed, Kimi Code and Antigravity were not read for this section. Two tables with the same rows keep the cells
readable. Instruction files (`AGENTS.md` and relatives) are summarized in the second table; for Claude Code, Codex
CLI, Gemini CLI and OpenCode the
[cross-harness matrix](../../cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md#which-patterns-each-harness-shows)
row "1 Persistent instruction file" is the fuller view.

### Settings files, precedence and environment variables

| Harness | Settings files and precedence | Environment variables |
|---|---|---|
| Claude Code ([settings][cfg-cc-settings]) | See the Claude Code docs in this corpus instead of a copy here: [CC-managed-settings-fleet-analysis.md](../../cc-native/configuration/CC-managed-settings-fleet-analysis.md) (managed layer and fleet scope), [CC-cli-reference.md](../../cc-native/configuration/CC-cli-reference.md) | [CC-env-vars-reference.md](../../cc-native/configuration/CC-env-vars-reference.md) |
| Codex CLI ([analysis](codex-cli-analysis.md)) | Highest first: CLI flags and `--config`, project `.codex/config.toml` (closest wins, trusted projects only), `--profile` files `~/.codex/<name>.config.toml`, user `~/.codex/config.toml`, cloud-managed defaults, system `/etc/codex/config.toml`, built-ins; an untrusted project's `.codex/` layers are skipped ([config basics][cfg-codex-basic], read 2026-11-27) | `CODEX_HOME` moves the state directory (default `~/.codex`) ([advanced config][cfg-codex-adv]); the [config reference][cfg-codex-ref] also names variables for provider keys and MCP servers, not listed here |
| Gemini CLI ([analysis](gemini-cli-analysis.md)) | Lowest to highest: defaults, system defaults file, user `~/.gemini/settings.json`, project `.gemini/settings.json`, system settings file (overrides all settings files), environment variables (may come from `.env`), command-line arguments; system files live in `/etc/gemini-cli/` (Linux), `C:\ProgramData\gemini-cli\` (Windows) or `/Library/Application Support/GeminiCli/` (macOS) ([configuration][cfg-gem-ref], read 2026-11-27) | Documented on the same page, among them `GEMINI_API_KEY`, `GEMINI_MODEL`, `GEMINI_CLI_HOME`, `GEMINI_CLI_SYSTEM_SETTINGS_PATH` and `GEMINI_CLI_SYSTEM_DEFAULTS_PATH` |
| GitHub Copilot CLI ([analysis](../agents/github-copilot-cli-analysis.md)) | Later overrides earlier: built-in defaults, MDM managed settings, user `~/.copilot/settings.json`, repository `.github/copilot/settings.json`, local `.github/copilot/settings.local.json`, environment variables, flags; it also reads `.claude/settings.json` for a shared subset of keys ([config directory][cfg-cop-dir], read 2026-11-27) | `COPILOT_HOME` relocates the user directory; `COPILOT_PROVIDERS_CONFIG` relocates `providers.json`; legacy `COPILOT_PROVIDER_*` variables are used when that file declares nothing (same page) |
| VS Code Copilot Chat ([analysis](vscode-copilot-chat-analysis.md)) | VS Code scopes, later overrides earlier: defaults, user, remote, workspace (`.vscode/settings.json`), workspace folder, language-specific variants, then policy settings, which always override; application-wide update and security settings cannot be set per workspace ([settings][cfg-vsc-set], read 2026-11-27) | Not documented on the pages read |
| Cursor ([analysis](cursor-analysis.md)) | Editor: a deployed policy overrides the setting at every level ([deployment patterns][cfg-cur-dep]); the user-level editor settings file is not described on the pages read. CLI: global `~/.cursor/cli-config.json`, project `<project>/.cursor/cli.json` for `permissions` only ([CLI configuration][cfg-cur-cli]). `sandbox.json` merges `~/.cursor/` and `<workspace>/.cursor/`, repo values winning ([sandbox reference][cfg-cur-sbx]) | CLI: `CURSOR_CONFIG_DIR`, and `XDG_CONFIG_HOME` on Linux and BSD (CLI configuration page) |
| Cline ([analysis](cline-analysis.md)) | Global `~/.cline/` (settings under `~/.cline/data/settings/`, shared by IDE, CLI and SDK) and project `.cline/`; which scope wins for a setting is not stated on the page read ([config][cfg-cline-cfg], read 2026-11-27) | `CLINE_DIR`, `CLINE_DATA_DIR`, `CLINE_HOOKS_DIR`, `CLINE_LOG_PATH` and others (same page) |
| Aider ([analysis](aider-analysis.md)) | `.aider.conf.yml` read from the home directory, the git root, then the current directory, later files winning; `--config` loads only that file ([YAML config][cfg-aider-yml]). A `.env` file follows the same three places plus `--env-file` ([dotenv][cfg-aider-env]) | Each option has an `AIDER_*` variable, for example `AIDER_MODEL` ([options reference][cfg-aider-opt]) |
| OpenCode ([analysis](opencode-analysis.md)) | Lowest to highest: global `~/.config/opencode/opencode.json(c)`, project files found from the current directory up to the filesystem root (`.opencode/` files after direct ones), then the system directory (`/etc/opencode`, macOS `/Library/Application Support/opencode`, Windows `%ProgramData%\opencode`) ([config][cfg-oc-cfg], read 2026-11-27) | Config values can read variables with `{env:NAME}`; `OPENCODE_DB` is named on the [CLI page][cfg-oc-cli]; no full list on the pages read |
| Amp ([analysis](amp-analysis.md)) | User `~/.config/amp/settings.json(c)`, workspace `.amp/settings.json(c)` searched upward, `--settings-file` for a custom user file; workspace overrides user, except keys such as `amp.url`, `amp.proxy` and `amp.dangerouslyAllowAll`, which are ignored there ([configuration][cfg-amp-set], read 2026-11-27) | `AMP_SKIP_UPDATE_CHECK`, `AMP_DISABLE_AMP_THREAD_TRAILER`, `AMP_FORCE_BEL` (same page); standard Node proxy and certificate variables for corporate networks |
| Windsurf, now Devin Desktop ([analysis](windsurf-analysis.md)) | Documented per feature, not as one settings file: MCP servers in project `.devin/mcp_config.json`, gitignored `.devin/mcp_config.local.json` and user `~/.config/devin/mcp_config.json`; permission rules at project, user or organization level ([customizations][cfg-ws-cust], [permissions][cfg-ws-perm], read 2026-11-27) | Not documented on the pages read |

### Managed policy, project overrides and instruction files

| Harness | Managed or enterprise policy | Project overrides and instruction files |
|---|---|---|
| Claude Code | [CC-managed-settings-fleet-analysis.md](../../cc-native/configuration/CC-managed-settings-fleet-analysis.md) | [Matrix row 1](../../cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md#which-patterns-each-harness-shows) |
| Codex CLI | `requirements.toml` constrains what users may set. Local layers, lowest to highest: system `/etc/codex/requirements.toml` (Windows `%ProgramData%\OpenAI\Codex\`), Agent Security cloud policy, legacy `managed_config.toml` fields, macOS MDM (`com.openai.codex`); legacy `managed_config.toml` supplies defaults the user can change ([managed configuration][cfg-codex-mgd], read 2026-11-27) | Project `.codex/config.toml` (trusted projects only); `AGENTS.override.md` or `AGENTS.md` per directory, concatenated root-down, 32 KiB cap by default ([AGENTS.md][cfg-codex-agents]); [matrix row 1](../../cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md#which-patterns-each-harness-shows) |
| Gemini CLI | The system settings file overrides user and project files; it can set tool allowlists and policy-engine rules, and a wrapper script can pin its path. The page says this is meant to prevent accidental misuse, not to stop a local administrator ([enterprise][cfg-gem-ent], read 2026-11-27) | Project `.gemini/settings.json`; `GEMINI.md` ([matrix row 1](../../cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md#which-patterns-each-harness-shows)) |
| GitHub Copilot CLI | MDM plist `com.github.copilot` (macOS), registry `HKLM\SOFTWARE\Policies\GitHubCopilot` (Windows) or `managed-settings.json` files (`/Library/Application Support/GitHubCopilot/`, `%ProgramFiles%\GitHubCopilot\`, `/etc/github-copilot/`), plus server-managed settings; for most keys users can override the baseline, but managed sandbox values are a floor and `permissions.disableBypassPermissionsMode = "disable"` always wins; deny rules beat ask and allow across managed sources ([config directory][cfg-cop-dir]) | `.github/copilot/settings.json` and `.local.json`; `.github/copilot-instructions.md`, `.github/instructions/**/*.instructions.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, extra directories in `COPILOT_CUSTOM_INSTRUCTIONS_DIRS`, plus personal files under `~/.copilot/` ([custom instructions][cfg-cop-instr]) |
| VS Code Copilot Chat | VS Code enterprise policies: Windows Group Policy (ADMX templates, registry), macOS configuration profiles, Linux `/etc/vscode/policy.json` from v1.106; computer-level beats user-level on Windows; the policy reference lists chat and agent policies such as `chat.agent.enabled` and sandbox settings ([policies][cfg-vsc-ent], read 2026-11-27) | `.vscode/settings.json`; `.github/copilot-instructions.md` or `AGENTS.md`, `CLAUDE.md`, `*.instructions.md` ([custom instructions][cfg-vsc-instr]) |
| Cursor | MDM policies on Windows (Group Policy), macOS (configuration profiles) and Linux (JSON, from Cursor 2.0); documented policies include allowed team IDs and allowed extensions ([deployment patterns][cfg-cur-dep], read 2026-11-27). Team and Enterprise plans add dashboard Team Rules, which take precedence over other rules ([rules][cfg-cur-rules]), and enterprise team-admin policies that layer over `sandbox.json` (sandbox reference); Enterprise also has enterprise-managed hooks ([hooks][cfg-cur-hooks]) | `.cursor/rules/*.mdc`, user rules, `AGENTS.md` (rules page); CLI project file `.cursor/cli.json` for permissions only |
| Cline | Remote configuration from the hosted admin console, applied when a member signs in: rules and workflows, skills, allowed providers, MCP controls and telemetry, with support differing by product (VS Code and JetBrains most, CLI rules and workflows only, Cline Desktop none of the listed controls); written into `.cline/remote-config/` or `.cline/enterprise/` in the workspace ([remote configuration][cfg-cline-ent], read 2026-11-27) | `.cline/` (rules, workflows, skills, hooks), older `.clinerules/`, `AGENTS.md` at the project root, `~/.agents/AGENTS.md` globally; workspace rules take precedence over global rules when they conflict ([config][cfg-cline-cfg], [rules][cfg-cline-rules]) |
| Aider | Not documented on the pages read | `.aider.conf.yml` at the git root or current directory; conventions are an ordinary file such as `CONVENTIONS.md` loaded with `--read` or `read:` in the YAML ([conventions][cfg-aider-conv]); no `AGENTS.md` mention on the pages read |
| OpenCode | System directory and macOS managed preferences (domain `ai.opencode.managed`, user profile replaces machine-wide) have the highest precedence; a `policies` array allows or denies providers, tools, MCP servers, skills and plugins, never prompts, and can also arrive from a connected OpenCode Console workspace ([config][cfg-oc-cfg], [policies][cfg-oc-pol], read 2026-11-27) | `opencode.json(c)` or `.opencode/opencode.json(c)` per directory; `AGENTS.md`, with a `CLAUDE.md` fallback ([instructions][cfg-oc-instr]; our [OpenCode doc](opencode-analysis.md)), [matrix row 1](../../cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md#which-patterns-each-harness-shows) |
| Amp | `managed-settings.json` in `/etc/ampcode/` (macOS `/Library/Application Support/ampcode/`, Windows `%ProgramData%\ampcode\`) beats the workspace Managed Settings document, which beats local settings; lists combine workspace-first and objects merge with workspace values winning; clients refresh in about 10 minutes ([configuration][cfg-amp-set], read 2026-11-27). Enterprise admins also set allowed models ([allowed models][cfg-amp-models]) | `.amp/settings.json(c)`; `AGENTS.md` read from the project and from `~/.config/amp/`, `~/.config/`, and `/etc/ampcode/` (macOS and Windows equivalents) ([AGENTS.md][cfg-amp-agents]) |
| Windsurf, now Devin Desktop | Enterprise admins set a root-level baseline and per-organization overrides from Settings, Enterprise, Devin Desktop (permissions, sandbox, MCP, models, and more); enterprise-enforced rules always outrank user and project configuration; an override replaces list values instead of merging; changes take up to 15 minutes ([local agent controls][cfg-ws-ctrl], read 2026-11-27). Organization overrides are "being rolled out gradually" per that page. Device policies (MDM) are enforced by the OS and "cannot be changed from inside the editor": Windows Group Policy (`Software\Policies\Windsurf\Devin`), a macOS configuration profile, or `/etc/vscode/policy.json` on Linux; system-level files live under `/etc/devin/` on Linux and WSL (same page) | `AGENTS.md`, `AGENTS.local.md`, `.devin/rules/*.md`, `.devin/global_rules.md`, user copies under `~/.devin/`; legacy `.windsurf/` rules are still imported ([customizations][cfg-ws-cust]) |

Findings from the tables:

- **Most harnesses have a user file, a project file and a machine-wide layer.** In Gemini CLI (below environment
  variables and flags), OpenCode and Amp the machine-wide file overrides the other files, and VS Code, Cursor and
  Windsurf policies override user settings; Codex CLI's `requirements.toml` constrains what the other layers
  may set instead. Copilot CLI differs: its managed layer is the lowest and most keys can be overridden, except
  the floors named above.
- **A documented machine-level file or MDM route exists for** Codex CLI, Gemini CLI (system files, no MDM
  named on the pages read), Copilot CLI, VS Code, Cursor, OpenCode, Amp and Windsurf (Devin Desktop device policies). Cline's documented
  route is a hosted console, and Aider documents none (on the pages read).
- **Project config is gated or limited in several harnesses**: Codex skips untrusted projects' `.codex/` layers,
  Amp ignores listed keys in workspace settings, and Cursor's CLI takes only `permissions` at project level. Amp's page gives the reason
  (anyone who can change a repository could otherwise choose those values for the user); Codex's says "for
  security"; the Cursor page read gives none.
- **Gemini CLI's status.** Its docs site carried a banner (read 2026-11-27) saying the unpaid tier and Google One
  users moved to Antigravity CLI on 2026-06-18; the settings above describe the CLI as documented, and which
  accounts can still use it was not checked here.

## Model access and billing

Same 15 rows, a different question: can you pay a model provider directly, can you point the harness
at another endpoint, what does the vendor say it charges, and which cost controls its docs name.
Headless and scripted billing is covered in
[Other Coding CLIs: Headless Sign-In and Billing](../../cc-native/ci-remote/CC-web-auth-setup-analysis.md#other-coding-clis-headless-sign-in-and-billing)
and is not repeated here. How a gateway works, and which products to put in front of a harness, is in
[LLM Gateway / Proxy Configuration](../../cc-native/configuration/CC-model-provider-configuration.md#llm-gateway--proxy-configuration)
and the [routers and gateways landscape](../infrastructure/llm-routers-gateways-landscape.md).
Prices and allowances are vendor claims as read on 2026-11-22 and change; "not documented
(checked 2026-11-22)" means the pages listed in [Sources](#sources) were silent.

### Access and billing by harness

| Harness | Bring your own key (BYOK) / direct API | Custom base URL or gateway | Vendor pricing model | Cost controls documented |
|---|---|---|---|---|
| Claude Code | `ANTHROPIC_API_KEY` for "direct Anthropic API access" with a Console key; also Amazon Bedrock, Google Cloud's Agent Platform and Microsoft Foundry ([auth][cc-auth]) | `ANTHROPIC_BASE_URL`; "Any gateway that exposes a" supported API format works, but Anthropic "doesn't support routing Claude Code to non-Claude models through any gateway" ([gateway][cc-gw]) | "Claude Code charges by API token consumption"; subscription plans are priced separately ([costs][cc-costs]) | `/usage` shows session tokens and a cost computed locally at list price, plus a prompt-cache line; `/model`, `/effort`; Console workspace spend limits ([costs][cc-costs]) |
| [Codex CLI](codex-cli-analysis.md) | Sign in with an API key for "usage-based access" ([auth][codex-auth]) | A model provider is "base URL, wire API, authentication, and optional HTTP headers"; the built-in provider can point at a proxy or router; `--oss` runs Ollama or LM Studio ([advanced config][codex-cfg]); OpenAI models via Amazon Bedrock ([Bedrock][codex-bedrock]) | Plan allowance plus credits; "API-key sessions use separate API pricing, not your ChatGPT allowance" ([pricing][codex-pricing]) | `/status` in a session and a usage dashboard ([pricing][codex-pricing]); API-key usage bills the OpenAI Platform account ([auth][codex-auth]), whose spend-limits guide documents organization and project hard limits but does not mention Codex ([spend limits][oai-spend]) |
| [Gemini CLI](gemini-cli-analysis.md) | `GEMINI_API_KEY` from Google AI Studio, or Vertex AI by ADC, service-account key or Cloud API key ([auth][gemini-auth]) | `GOOGLE_GEMINI_BASE_URL` and `GOOGLE_VERTEX_BASE_URL` override the endpoints; HTTPS unless localhost ([configuration][gemini-cfg]) | "Your authentication method affects your quotas, pricing" ([auth][gemini-auth]); the page also says Antigravity CLI replaced Gemini CLI on 2026-06-18 | Token caching with an API key or Vertex, not with OAuth; `/stats` shows usage and cached-token savings ([token caching][gemini-cache]) |
| [GitHub Copilot CLI](../agents/github-copilot-cli-analysis.md) | `providers.json` entries of type `openai`, `azure` or `anthropic`; local Ollama models are found automatically ([BYOK][copilot-byok]) | `baseUrl` per provider; the OpenAI type covers "Ollama, vLLM, and Foundry Local"; `COPILOT_PROVIDERS_CONFIG` moves the file ([BYOK][copilot-byok]) | AI credits, "1 AI credit = $0.01 USD"; billing of BYOK models not documented (checked 2026-11-22) ([billing][copilot-billing]) | Budget for usage beyond included credits "set in US dollars"; usage dashboard ([billing][copilot-billing]) |
| [VS Code Copilot Chat](vscode-copilot-chat-analysis.md) | Built-in providers include "Azure, Anthropic, Gemini, OpenAI, and others"; BYOK models "work without signing into a GitHub account and without a Copilot plan", chat only ([language models][vscode-lm]) | Custom Endpoint provider for Chat Completions, Responses or Messages APIs ([language models][vscode-lm]) | AI credits ([Copilot billing][copilot-billing]) | "Higher thinking effort produces more thinking tokens, which increases AI credit consumption"; budget as in the Copilot CLI row ([language models][vscode-lm], [billing][copilot-billing]) |
| [Cursor](cursor-analysis.md) | OpenAI, Anthropic, Google, Azure and AWS Bedrock keys in Settings, Models; "Custom API keys only work with chat models", Tab keeps Cursor's models ([API keys][cursor-keys]) | base URL override not documented (checked 2026-11-22) | Weekly pool for Cursor models; third-party models "at API list price, paid from prepaid credit" on Premium and above; Teams and Enterprise add a rate "on top of model API pricing" for BYOK usage ([pricing][cursor-pricing]) | "A monthly additional usage limit caps how much paid additional usage you can consume each month"; on Teams "one cap for the whole team"; "Your remaining usage and next reset date are shown in your editor settings" ([pricing][cursor-pricing]) |
| [Cline](cline-analysis.md) | "Bring Your Own Key" with cloud providers or local runtimes ([overview][cline-start]) | OpenAI Compatible provider takes a Base URL, key and model ID; OpenRouter listed ([OpenAI compatible][cline-oai], [OpenRouter][cline-or]) | Cline account: credits "used on a pay-as-you-go basis" for paid models ([Cline provider][cline-prov]); ClinePass "Flat $9.99/month subscription" that "offers 2-5x the usage on popular open coding models compared to standard API rate" (vendor claim) ([overview][cline-start]); "OpenRouter charges based on the underlying model's pricing" ([OpenRouter][cline-or]) | "View usage in Cline Settings" ([Cline provider][cline-prov]); no spend cap on the pages read (checked 2026-11-22) |
| [Aider](aider-analysis.md) | Connects to "most LLMs": OpenAI, Anthropic, Gemini, Azure, Bedrock, Vertex AI, OpenRouter, Ollama and others ([LLMs][aider-llms]) | `OPENAI_API_BASE` plus an `openai/` model prefix for OpenAI-compatible endpoints ([OpenAI compatible][aider-oai]) | No vendor pricing: Apache-2.0 repository ([repo][aider-repo]), you bring the provider's key | `--cache-prompts` for Anthropic Sonnet and Haiku and DeepSeek Chat; "caching statistics and costs are not available when streaming responses", use `--no-stream` ([caching][aider-cache]) |
| [OpenCode](opencode-analysis.md) | `/connect` adds credentials for catalog providers; Bedrock uses the AWS credential chain, Vertex uses ADC, Azure uses deployments ([providers][oc-providers]) | Add a custom provider or override `baseURL` for a catalog provider; LM Studio and vLLM have built-in local discovery ([providers][oc-providers]) | Console "uses pay-as-you-go pricing", sold "at cost, with markup only to cover processing fees": 4.6% + $0.31 per credit purchase (vendor claim); Go is a subscription, see the [headless billing table](../../cc-native/ci-remote/CC-web-auth-setup-analysis.md#other-coding-clis-headless-sign-in-and-billing) ([Console][oc-zen]) | Console: auto-recharge, and "budgets cap monthly spend for the workspace and each member" ([Console models][oc-console-models]) |
| [Amp](amp-analysis.md) | BYOK on Hobby and Individual; Teams add "Shared BYOK & model routing"; Enterprise lists regional endpoints for BYOK providers ([pricing][amp-pricing]) | Custom URL connection to "any OpenAI- or Anthropic-compatible endpoint": "Enter the base URL, and Amp appends the API path"; routers such as OpenRouter, Vercel AI Gateway and Cloudflare AI Gateway listed, "available to all users on every tier" ([model routing][amp-routing]) | "pay for what you use at standard rates" or monthly tiers; "Amp does not add a markup to providers' API prices" for individuals and non-enterprise workspaces; purchased credits expire after twelve months ([pricing][amp-pricing]) | Balance in settings or `amp usage`; per-thread cost on the thread's price label ([pricing][amp-pricing]) |
| [Windsurf](windsurf-analysis.md) | not documented (checked 2026-11-22) | not documented (checked 2026-11-22) | Docs now say Devin Desktop: since March 2026 a quota with daily and weekly allowances; extra usage "billed at API list prices for the model you're using" ([quota][ws-quota]); per-token prices per model, e.g. SWE-2 free for self-serve plans in Devin Desktop and Devin CLI through November 30, 2026 (Pacific time; not Devin cloud sessions), then $0.50/1M input and $2.50/1M output through December 31, 2026, then list $3.00/$15.00 ([models][ws-models]); legacy credit plans: "$120 for 1000 pooled credits" ([usage][ws-usage]) (vendor claims) | Remaining quota in the usage meter or plan page; docs suggest the lower-cost SWE models for routine tasks ([quota][ws-quota]); legacy credit auto-refill "subject to maximum monthly budget caps ($160 by default)" ([usage][ws-usage]); a cap on self-serve extra usage not documented (checked 2026-11-22) |
| [Kiro](kiro-analysis.md) | not documented (checked 2026-11-22); `KIRO_API_KEY` is a Kiro key for paid tiers, not a provider key ([headless][kiro-headless]) | not documented (checked 2026-11-22) | Credits: Pro $20/user/month for 1,000 credits, add-on credits $0.04 each (vendor prices) ([pricing][kiro-pricing]) | Credits used and remaining in the subscription dashboard, "updated at least every 5 minutes" ([pricing][kiro-pricing]) |
| [Zed](zed-analysis.md) | Keys go to the system keychain; Anthropic, OpenAI, Google AI, Mistral, DeepSeek, xAI; own keys on every plan including Free ([API access][zed-api], [plans][zed-plans]) | `api_url` under `language_models.openai_compatible` for an OpenAI-compatible endpoint ([API access][zed-api]) | Hosted models at provider list price "+10%", Pro includes $5 monthly token credit; own-key use "even when you pay the provider directly" is API access ([plans][zed-plans], [API access][zed-api]) | Billing page for usage; Pro default incremental limit $10, adjustable down to $0; org-wide limit on Business ([plans][zed-plans]) |
| [Kimi Code](kimi-code-analysis.md) | Provider types `kimi`, `anthropic`, `openai`, `openai_responses`, `bedrock`, `google-genai`, `vertexai`; `/login` also takes a Kimi Platform API key ([providers][kimi-prov], [getting started][kimi-start]) | `base_url` per provider; the `openai` type works with "any third-party service compatible with that protocol" ([providers][kimi-prov]) | Kimi Code is a membership subscription "with rate limiting"; the Kimi Platform is "Pay-as-you-go, top up and use" ([Kimi Code docs][kimi-docs]) | not documented (checked 2026-11-22) |
| [Antigravity](antigravity-analysis.md) | Gemini API key, or Agent Platform by API key or ADC ([getting started][ag-start]) | not documented (checked 2026-11-22) | Plans named Free, Pro and Ultra, no prices on the page ([getting started][ag-start]) | `/usage` "Displays current model credit consumption and quota limits" ([getting started][ag-start]) |

### Model access notes

- **Custom endpoints are documented by 11 of 15.** Claude Code, Codex CLI, Gemini CLI, Copilot
  CLI, VS Code, Cline, Aider, OpenCode, Amp, Zed and Kimi Code document a base-URL or gateway path.
  Cursor, Windsurf, Kiro and Antigravity do not on the pages read. A documented endpoint says the
  harness will send requests there, not that every gateway forwards the harness's features; Claude
  Code's page says so for its own case.
- **Claude Code's gateway page limits models.** It says Anthropic "doesn't support routing Claude
  Code to non-Claude models through any gateway"; Aider, OpenCode, Cline, Zed, Amp and Kimi Code
  document multi-provider setups.
- **Pass-through pricing is stated by few.** Amp ("does not add a markup", non-enterprise) and
  OpenCode Console ("at cost", plus a purchase fee) say so; Zed states +10% on hosted models;
  Cursor and Windsurf (Devin Desktop) state API list price for usage beyond their allowance. All
  are vendor claims.
- **Cost controls are mostly usage displays.** Spend caps are documented by Claude Code (Console
  workspaces), Copilot (a budget in dollars), Cursor (a monthly additional-usage limit), Zed (a
  monthly limit), OpenCode Console (workspace and per-member budgets) and, for legacy credit plans, Windsurf (a monthly budget cap). Codex's pricing page
  names none; its API-key route falls under OpenAI's general API spend limits. Caching controls
  appear for Aider (`--cache-prompts`), Gemini CLI (token caching) and Claude Code (prompt cache
  statistics).
- **Windsurf docs moved and the product was renamed.** They now live under Devin's as Devin
  Desktop; BYOK and endpoint overrides were not found there, so those cells stay undocumented.
- **Antigravity cells rest on one page.** The getting-started CLI tab lists sign-in modes and
  `/usage` but no endpoint override or prices; the auth names it uses mirror Gemini CLI's.

### Using subscriptions in other harnesses

Question: can a consumer subscription (instead of an API key) power a harness, and what do the vendors'
own pages say about it? Read 2026-11-23 from vendor pages only (the Copilot CLI Entra, OpenCode, third-party agent, Remote Control and gateway cells were read on 2026-11-26; the proxy row cites the projects' own READMEs, which are community sources, not vendor pages); evidence level per cell: **documented**
(vendor page states it) or **not addressed** (the named page is silent, which is not permission). Nothing
was run. This is not legal advice; the terms pages are the authority.

| Harness | Subscription sign-in documented | Terms wording on the vendor's own pages | Stated limits and pitfalls |
|---|---|---|---|
| Claude Code | Pro, Max, Ultra via claude.ai login; Team and Enterprise too ([auth][cc-auth]). `claude setup-token` makes a one-year token for CI that "requires a Pro, Max, Ultra, Team, or Enterprise plan" and cannot do Remote Control or claude.ai connectors ([auth][cc-auth]) | OAuth "is intended exclusively for purchasers" of the subscription plans, for "ordinary use of Claude Code and other native Anthropic applications"; developers building products "should use API key authentication"; Anthropic "does not permit third-party developers" to "route requests through Free, Pro, Max, or Ultra plan credentials on behalf of their users"; an end user may sign in to "the unmodified Claude Code binary" with their own subscription ([legal][cc-legal]) | Plan limits "assume ordinary, individual usage of Claude Code and the Agent SDK" ([legal][cc-legal]); five-hour and weekly limits "shared across Claude and Claude Code" ([plan article][cc-plan]); a set `ANTHROPIC_API_KEY` wins over the subscription and bills API rates ([auth][cc-auth], [plan article][cc-plan]); `--bare` does not read `CLAUDE_CODE_OAUTH_TOKEN` ([auth][cc-auth]) |
| [Codex CLI](codex-cli-analysis.md) | "Sign in with ChatGPT for subscription access" in the app, CLI and IDE extension; Codex cloud needs ChatGPT sign-in ([auth][codex-auth]); Codex is in Free, Go, Plus, Pro, Business, Edu and Enterprise plans ([pricing][codex-pricing]) | Third-party or automated use of the ChatGPT sign-in: not addressed on [auth][codex-auth] or [pricing][codex-pricing]; the auth page advises "API keys are still the recommended default for automation" and "Use API key authentication for programmatic Codex CLI workflows, such as CI/CD jobs" | Plus has a "five-hour period" limit and weekly limits may apply; local and cloud use share one allowance ([pricing][codex-pricing]); API-key sign-in limits or drops features that rely on ChatGPT workspace access, and bills "standard API pricing" ([auth][codex-auth]); treat `~/.codex/auth.json` "like a password" ([auth][codex-auth]) |
| [Gemini CLI](gemini-cli-analysis.md) | Google account sign-in for AI Pro or Ultra, and Code Assist ([auth][gemini-auth]); the page banner says unpaid-tier and Google One users moved to Antigravity CLI on 2026-06-18 | Directly accessing the services behind Gemini CLI "using third-party software, tools, or services (for example, using OpenClaw with Gemini CLI OAuth) is a violation of applicable terms and policies", with possible "suspension or termination" ([terms][gemini-tos]) | Per-user daily request caps by sign-in method, e.g. AI Pro 1,500 and AI Ultra 2,000 (page dated 2026-06-18) ([quota][gemini-quota]); headless runs reuse a cached credential, else need an API key or Vertex AI, with service-account keys suggested for CI ([auth][gemini-auth]); for API-key use the page says terms may differ between unpaid and paid service ([terms][gemini-tos]) |
| [GitHub Copilot CLI](../agents/github-copilot-cli-analysis.md) | Needs "An active GitHub Copilot subscription"; `/login` or a fine-grained token with the Copilot Requests permission in `COPILOT_GITHUB_TOKEN`, `GH_TOKEN` or `GITHUB_TOKEN` ([install][copilot-install]). Also, in public preview, a Microsoft Entra account with Microsoft 365 Copilot access: `/login`, then "Your organization (Microsoft Entra)"; for Frontier customers only; needs the Microsoft Copilot **Code** spending policy for usage-based billing; Windows and macOS, CLI 1.0.113 or later ([auth][copilot-auth], [changelog][copilot-entra]) | Not addressed on [install][copilot-install], [auth][copilot-auth] or the [changelog][copilot-entra] | CI use not covered on the install page; an organization or enterprise owner can disable the CLI ([install][copilot-install]). Entra sign-in is "in public preview and subject to change" ([auth][copilot-auth]); the changelog says Linux support "will follow" and that model access and usage limits are managed through the organization's Microsoft 365 Copilot settings, not GitHub ([changelog][copilot-entra]) |
| Claude and Codex agents on a Copilot plan (GitHub-hosted) | The Anthropic Claude coding agent "uses the Claude Agent SDK and can be powered by your existing Copilot subscription"; the OpenAI Codex agent uses the Codex SDK; both "currently in public preview" ([third-party agents][copilot-3p]) | A GitHub feature using Copilot's own sign-in, not a route for another vendor's consumer plan; vendor terms not addressed on [that page][copilot-3p] | "Coding agents consume **GitHub Actions minutes** and **AI credits**"; within the included amounts there is no extra cost ([third-party agents][copilot-3p]); the page lists Pro, Pro+, Max, Business and Enterprise plans under enabling-policy links, with no single eligibility list |
| [OpenCode](opencode-analysis.md) | "Sign in with ChatGPT" for OpenAI (Plus or Pro; usage counts against the plan); GitHub Copilot by device OAuth; Claude Pro/Max and Gemini subscription sign-in not covered on the page ([providers][oc-providers]). GitHub's own changelog (2026-01-16) says paid Copilot subscribers (Pro, Pro+, Business or Enterprise) can sign in with `/connect` and the GitHub device login, "no additional AI license needed" ([changelog][copilot-oc]) | Not addressed on [providers][oc-providers]; GitHub's changelog announces the sign-in as supported ([changelog][copilot-oc]) | OpenCode caps context limits for ChatGPT sign-ins by default ([providers][oc-providers]) |
| Unofficial Copilot-subscription proxies for Claude Code (`copilot-api`, `copilot-proxy-api`) | Community projects that expose a Copilot sign-in as an OpenAI- or Anthropic-style endpoint; both document Claude Code setup; stars on 2026-11-26 4155 and 60, both MIT ([copilot-api][px-capi], [copilot-proxy-api][px-cpa]) | Not vendor-documented; GitHub's terms pages were not read for this doc (unverified). `copilot-api` calls itself a reverse-engineered proxy that "is not supported by GitHub" and links GitHub's Copilot Terms; `copilot-proxy-api` calls itself unofficial and links GitHub's acceptable-use policies and Copilot Terms | Both READMEs warn of breakage when the Copilot API changes; `copilot-api` warns that bulk or scripted use "may trigger GitHub's abuse-detection systems", and `copilot-proxy-api` that activity triggering abuse controls may restrict or suspend Copilot access. Unsupported by GitHub per the projects' own READMEs |
| [Cline](cline-analysis.md) | "Claude Code (Subscription)" provider that drives the user's own installed `claude` CLI ([Cline docs][cline-cc]) | Not addressed on [Cline docs][cline-cc]; the Claude Code terms above apply to the CLI itself | Responses may not stream token by token; image uploads and prompt caching limited ([Cline docs][cline-cc]) |
| [Antigravity](antigravity-analysis.md) | Plans on personal Google accounts; AI Pro and Ultra get larger quotas ([plans][ag-plans]); sign-in steps not on that page | Third-party or automated use: not addressed on [plans][ag-plans]; BYOK and bring-your-own-endpoint "currently" unsupported | AI Pro and Ultra quota refreshes every five hours until a weekly limit; Workspace plans "don't include" Antigravity plans ([plans][ag-plans]) |

Rows not listed (Cursor, Aider, Amp, Windsurf, Kiro, Zed, Kimi Code, VS Code Copilot Chat) either sell their
own plan or use provider keys; their pages read for this doc do not describe signing in with another
vendor's consumer subscription (checked 2026-11-23, not exhaustive).

**Data handling differs by plan.** Anthropic: consumer plans may be used for training when the setting is on,
with 5-year retention if allowed and 30 days if not; commercial plans and the API keep 30 days and are not
trained on under commercial terms ([data usage][cc-data]). OpenAI: ChatGPT sign-in follows workspace
permissions and retention, API keys follow the API organization's settings ([auth][codex-auth]). Google:
the terms page points to the privacy policy and notices and does not state a training rule
([terms][gemini-tos]).

**Patterns** (documented basis in brackets; the combination is this corpus's reading, not a vendor
recommendation):

| Pattern | Basis |
|---|---|
| Subscription for interactive work on the machine you sit at; API key or cloud-provider credential for CI and shared automation | Codex auth page recommends API keys for CI; Claude Code legal page points developers and products to API keys ([auth][codex-auth], [legal][cc-legal]) |
| Use each vendor's own, unmodified harness with its own plan; do not embed another party's subscription token in a tool you operate for others | Claude Code legal page and Gemini terms page above |
| Check which credential is active before a long run (an inherited API key silently moves billing off the plan) | Claude Code `/status` and precedence rules ([auth][cc-auth]) |
| Route API-key traffic through a gateway for logging, budgets or provider switching; subscription sign-ins use the vendor's own endpoint (vendor-documented exceptions: a Copilot plan in OpenCode, and the Claude and Codex agents on a Copilot plan, above) | [gateway docs](../infrastructure/llm-routers-gateways-landscape.md); Claude Code's gateway page ([gateway][cc-gw]) |
| Keep a token file (`auth.json`, `CLAUDE_CODE_OAUTH_TOKEN`) out of repos, images and shared runners | Codex auth page; Claude Code auth page |
| Claude Code Remote Control needs the subscription sign-in itself: no API key, no cloud-provider route, no gateway base URL | Remote Control page: "API keys are not supported"; not available on Amazon Bedrock, Google Cloud's Agent Platform or Microsoft Foundry, or with `ANTHROPIC_BASE_URL` pointing away from `api.anthropic.com` ([Remote Control][cc-rc]) |
| A gateway credential replaces the subscription login; setting only `ANTHROPIC_BASE_URL` does not | Gateway page: requests carry the gateway credential "in place of a developer's claude.ai subscription login"; with only the base URL set, "a saved claude.ai login remains the active credential" and its limits and billing apply ([gateway][cc-gw]) |

Scripted-run terms for Claude Code are in
[Terms That Apply to Scripted Runs](../../cc-native/ci-remote/CC-web-auth-setup-analysis.md#terms-that-apply-to-scripted-runs).

## Context compaction by harness

Question (owner, 2026-11-23): do other harnesses offer what Claude Code's `/autocompact` window plus
percentage trigger offers? Read from vendor docs on 2026-11-23; "not documented" names the pages looked at,
and means those pages were silent. Claude Code's own settings are owned by
[Setting the auto-compact window](../../cc-native/context-memory/CC-extended-context-analysis.md#setting-the-auto-compact-window-autocompact)
and the [env vars reference](../../cc-native/configuration/CC-env-vars-reference.md), not restated here.
Defaults are vendor-documented values, not observed behaviour.

| Harness | Auto compaction | Manual command | Trigger setting (name, unit) | Scope / notes | Source |
|---|---|---|---|---|---|
| Claude Code | yes | yes | window in tokens and percent of window | see the two owner sections above | [CC-extended-context-analysis](../../cc-native/context-memory/CC-extended-context-analysis.md#setting-the-auto-compact-window-autocompact), [CC-env-vars-reference](../../cc-native/configuration/CC-env-vars-reference.md) |
| [Codex CLI](codex-cli-analysis.md) | yes ("automatic history compaction") | `/compact` | `model_auto_compact_token_limit` (tokens, unset uses model defaults); `model_post_turn_compact_threshold_percent` (0-100, percent of usable window, unset or `0` disables); `model_auto_compact_token_limit_scope` (`total` default, or `body_after_prefix`) | `compact_prompt` overrides the summary prompt; per-model settings not documented on the part read (about 100k of 166k characters of the config reference) | [config ref][codex-cfgref], [commands][codex-cmds] |
| [Gemini CLI](gemini-cli-analysis.md) | yes | `/compress` ("Replace the entire chat context with a summary") | `model.compressionThreshold` (fraction of context, default `0.5`); experimental `contextManagement.historyWindow.maxTokens` (tokens, default `150000`) and `retainedTokens` (default `40000`), behind `experimental.contextManagement` (default `false`) | disable switch not found; `hooks.PreCompress` runs before compression; last 16k characters of the configuration page not read | [configuration][gemini-cfg], [commands][gemini-cmds] |
| [GitHub Copilot CLI](../agents/github-copilot-cli-analysis.md) | yes: background compaction at "approximately 80%", pauses if context reaches about 95% first | `/compact [FOCUS-INSTRUCTIONS]` | not documented: the context article names no setting, and the first 200k characters of the command reference name none | disabling not documented; `/context` shows token usage | [context][copilot-ctx], [CLI reference][copilot-cli] |
| [VS Code Copilot Chat](vscode-copilot-chat-analysis.md) | yes, "as the conversation nears the context window limit" | `/compact` | not documented ("Setting names: none" on the page) | threshold not stated | [context][vscode-ctx] |
| [Cursor](cursor-analysis.md) | not documented (agent overview, CLI slash commands) | `/summarize`, alias `/compress` (CLI) | not documented | the CLI command is the only compaction control found | [slash commands][cursor-slash], [overview][cursor-overview] |
| [Cline](cline-analysis.md) | yes ("Auto Compact"), when a conversation nears the context limit | `/smol`; `/compact` is an alias | not documented: no percentage or token count on the page; apparently a toggle | with other models Cline falls back to rule-based truncation | [auto compact][cline-auto], [slash commands][cline-slash] |
| [Aider](aider-analysis.md) | yes, summarization of older chat history | no summarise command found; `/clear` and `/reset` drop history | `--max-chat-history-tokens` (tokens, "Soft limit ... after which summarization begins"; env `AIDER_MAX_CHAT_HISTORY_TOKENS`) | summaries by `--weak-model`; falls back to the model's own value when unset | [options][aider-opts], [commands][aider-cmds] |
| [OpenCode](opencode-analysis.md) | yes (`compaction.auto`; `false` "disables new automatic compaction") | command `session.compact`, default keybind `<leader>c`; a `/compact` entry not found on the TUI page | `compaction.buffer` (share of window kept free, example `"15%"`); `compaction.keep.tokens` (tokens of recent context kept) | compaction type `native` or `summary` per provider or model under `settings.compaction`; per-agent compaction not documented | [config][oc-config], [keybinds][oc-keybinds] |
| [Amp](amp-analysis.md) | not documented (manual, threads page, CLI settings page) | not documented | not documented | the threads page instead advises asking the agent to "Handoff and ..." for a fresh thread | [threads][amp-threads], [CLI settings][amp-cli-settings] |
| [Windsurf](windsurf-analysis.md) | not documented (Cascade page) | not documented | not documented | the page says Cascade retrieves "conversation summaries and checkpoints" when mentioning past chats | [Cascade][windsurf-cascade] |
| [Kiro](kiro-analysis.md) | yes | `/compact`, CLI only | `compaction.autoCompactionThreshold` (percent 0-100, default `80`, CLI 3.3.0 or later); `compaction.excludeMessages` (default `2`); `compaction.excludeContextWindowPercent` (default `2`) | workspace `.kiro/settings/cli.json` overrides the global default; `PreCompact` hook can refuse; off via `/settings`, no key named | [compaction][kiro-compaction] |
| [Zed](zed-analysis.md) | yes, default on | `/compact` | `agent.auto_compact.threshold` (default `"90%"`; a positive integer means tokens used, a negative integer means tokens remaining) and `enabled` | no auto compaction for models with a window under 80,000 tokens | [agent panel][zed-panel], [agent settings][zed-agent-settings] |
| [Kimi Code](kimi-code-analysis.md) | yes | `/compact` (optional hint) | `reserved_context_size` under `[loop_control]` (tokens reserved for model output; the sessions page says history is compressed automatically "when the context approaches the window limit"); `compaction_max_attempts` (default `5`) | `max_input_size` on a model entry is preferred for the window; disable switch not found | [sessions][kimi-sessions], [config files][kimi-config], [interaction][kimi-int] |
| [Antigravity](antigravity-analysis.md) | yes ("automatically compacts older turns") | `/compact`, or `/compact <message>` | not documented | `disableSlashCommands` in `settings.json` turns off slash commands in headless mode | [`/compact`][ag-compact] |

### Compaction notes

- **A percentage or fraction trigger is documented by five of the 14 other harnesses.** Gemini CLI
  (`model.compressionThreshold`), Codex CLI (`model_post_turn_compact_threshold_percent`), OpenCode
  (`compaction.buffer`), Kiro (`compaction.autoCompactionThreshold`) and Zed (`agent.auto_compact.threshold`).
  Codex, Aider, Zed and Gemini CLI's experimental key also take token counts; Kimi Code's trigger is a reserved
  token margin, not a percent.
- **Manual commands are near-universal, names differ:** `/compact` (Codex, Copilot, VS Code, Kiro, Zed, Kimi,
  Antigravity, Cline alias), `/compress` (Gemini CLI; Cursor alias), `/summarize` (Cursor), `/smol` (Cline).
  Amp, Windsurf and Aider document none.
- **Disable switches are documented by three:** Codex (`0` on the percent key), OpenCode (`compaction.auto`)
  and Zed (`enabled`). Kiro says to use `/settings`. Goose, not in this doc's harness set, is the clearest
  example of both a percent and a token cap with `0.0` to disable
  ([Goose docs][goose-ctx], read 2026-11-23).
- **No per-agent compaction setting was found** on the pages read; OpenCode documents per-provider or
  per-model type only.

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
| [Using Copilot CLI][copilot-cli-use] | Image and PDF attachments: file types, `@path`, drag-and-drop, paste, no policy required |
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
| [Claude Code: authentication][cc-auth] | API key, cloud providers |
| [Claude Code: other LLM gateways][cc-gw] | Base URL, gateway scope |
| [Claude Code: manage costs][cc-costs] | Token billing, `/usage`, controls |
| [Codex: authentication][codex-auth] | API-key sign-in, API pricing |
| [Codex: pricing][codex-pricing] | Allowance, credits, API-key sessions, `/status` |
| [Codex: advanced configuration][codex-cfg] | Model providers, `--oss`, proxy |
| [Codex: Amazon Bedrock][codex-bedrock] | OpenAI models via Bedrock |
| [Gemini CLI: authentication][gemini-auth] | API key, Vertex AI |
| [Gemini CLI: configuration][gemini-cfg] | Base URL variables |
| [Gemini CLI: token caching][gemini-cache] | Caching, `/stats` |
| [Copilot CLI: BYOK models][copilot-byok] | Provider types, `baseUrl` |
| [Copilot: individual billing][copilot-billing] | AI credits, budget, dashboard |
| [VS Code: language models][vscode-lm] | BYOK, Custom Endpoint, thinking effort |
| [Cursor: models and pricing][cursor-pricing] | Pool, list price, BYOK rate, usage display |
| [Cursor: API keys][cursor-keys] | Providers, chat-only limit |
| [Cline: what is Cline][cline-start] | BYOK, ClinePass |
| [Cline: OpenAI compatible][cline-oai] | Base URL, key, model ID |
| [Cline: OpenRouter][cline-or] | Underlying model pricing |
| [Aider: connecting to LLMs][aider-llms] | Provider list |
| [Aider: OpenAI compatible APIs][aider-oai] | `OPENAI_API_BASE` |
| [Aider: prompt caching][aider-cache] | `--cache-prompts`, cost display |
| [OpenCode: providers][oc-providers] | Catalog, `baseURL`, local discovery |
| [OpenCode: Console][oc-zen] | Pay-as-you-go, fee |
| [OpenCode: Console models][oc-console-models] | Auto-recharge and monthly budgets |
| [Amp: pricing][amp-pricing] | Pay-as-you-go, no markup, BYOK, `amp usage` |
| [Kiro: pricing][kiro-pricing] | Credits, plan prices, dashboard |
| [Kiro CLI: headless mode][kiro-headless] | `KIRO_API_KEY` |
| [Zed: use API access][zed-api] | Keys, `api_url`, billing wording |
| [Zed: plans and usage][zed-plans] | List price +10%, credits, limits |
| [Kimi Code: providers][kimi-prov] | Provider types, `base_url` |
| [Kimi Code docs][kimi-docs] | Membership vs platform billing |
| [Kimi Code: getting started][kimi-start] | `/login` Platform API key |
| [OpenAI: spend limits][oai-spend] | Organization and project hard limits for the API |
| [Cline: Cline provider][cline-prov] | Pay-as-you-go credits, View Usage |
| [Aider: repository][aider-repo] | Apache-2.0 licence |
| [Amp: model routing][amp-routing] | Custom URL connection, routers |
| [Devin Desktop: quota-based usage][ws-quota] | Extra usage at API list prices, usage meter |
| [Devin Desktop: models][ws-models] | Per-token prices, SWE-2 promotion |
| [Devin Desktop: usage (legacy credits)][ws-usage] | $120 per 1000 pooled credits, budget caps |
| [Antigravity: getting started (CLI tab)][ag-start] | Sign-in modes, `/usage`, plan names |
| [Claude Code: legal and compliance][cc-legal] | Consumer terms, OAuth intended use, products and third parties |
| [Claude: Claude Code with Pro or Max][cc-plan] | Limit windows, shared limits, API key precedence |
| [Claude Code: data usage][cc-data] | Training and retention by plan |
| [Gemini CLI: terms and privacy][gemini-tos] | Terms by sign-in method, third-party OAuth wording |
| [Gemini CLI: quota and pricing][gemini-quota] | Daily request caps by sign-in |
| [Copilot CLI: install][copilot-install] | Subscription need, tokens |
| [Copilot CLI: authenticate][copilot-auth] | Microsoft Entra sign-in: preview, Frontier, spending policy, platforms, version |
| [Copilot CLI Entra sign-in changelog (2026-11-17)][copilot-entra] | Preview announcement; Linux to follow; limits managed in Microsoft 365 |
| [Copilot supports OpenCode (2026-01-16)][copilot-oc] | Paid Copilot plans sign in to OpenCode |
| [Copilot: third-party coding agents][copilot-3p] | Claude and Codex agents on a Copilot plan, preview, billing |
| [Claude API: PDF support][claude-pdf] | Text plus page image per page, limits |
| [Claude API: vision][claude-vision] | Image limits, downscaling |
| [GPT-6.2 Astra][oai-astra] | Modalities: text and image in, text out |
| [OpenAI: file inputs][oai-files] | PDF text plus page images |
| [Gemini API: document processing][gem-doc] | PDF page limit, inline or Files API |
| [Gemini API: video understanding][gem-vid] | Video as a separate input |
| Codex CLI, Gemini CLI, OpenCode, Aider releases ([codex][codex-rel], [gemini][gemini-rel], [opencode][oc-rel], [aider][aider-rel]) | Tags the media-handling code was read at |
| [Claude Code: Remote Control][cc-rc] | Subscription-only; excluded endpoints |
| [copilot-api README][px-capi], [copilot-proxy-api README][px-cpa] | Unofficial proxies: self-description and warnings (stars from the GitHub API, 2026-11-26) |
| [Cline: Claude Code provider][cline-cc] | Subscription route via the CLI |
| [Antigravity: plans][ag-plans] | Quota windows, BYOK unsupported |
| [Codex: configuration reference][codex-cfgref] | Auto-compact settings |
| [Gemini CLI: commands][gemini-cmds] | `/compress` |
| [Copilot CLI: context management][copilot-ctx] | Auto-compact at about 80% |
| [VS Code: context][vscode-ctx] | Automatic and `/compact` |
| [Cursor: CLI slash commands][cursor-slash] | `/summarize`, `/compress` |
| [Cline: Auto Compact][cline-auto] | Auto-compact behaviour |
| [Cline: slash commands][cline-slash] | `/smol`, `/compact` |
| [Aider: options][aider-opts] | `--max-chat-history-tokens` |
| [Aider: in-chat commands][aider-cmds] | `/clear`, `/reset` |
| [OpenCode: config][oc-config] | `compaction.*` |
| [OpenCode: keybinds][oc-keybinds] | `session.compact` |
| [Amp: threads][amp-threads] | Handoff, no compaction page |
| [Amp: CLI settings][amp-cli-settings] | No compaction settings |
| [Kiro: compaction][kiro-compaction] | Thresholds, `/compact` |
| [Zed: agent settings][zed-agent-settings] | `agent.auto_compact` |
| [Kimi Code: sessions][kimi-sessions] | Auto and `/compact` |
| [Kimi Code: config files][kimi-config] | `reserved_context_size` |
| [Antigravity: `/compact`][ag-compact] | Command and auto behaviour |
| [Goose: smart context management][goose-ctx] | Percent and token compaction settings, `0.0` disables |
| [Claude Code: settings][cfg-cc-settings] | Settings scopes (linked, not repeated) |
| [Codex: config basics][cfg-codex-basic] | Precedence, project trust |
| [Codex: advanced config][cfg-codex-adv] | `CODEX_HOME`, profiles |
| [Codex: config reference][cfg-codex-ref] | Key and variable reference |
| [Codex: managed configuration][cfg-codex-mgd] | `requirements.toml`, MDM, layers |
| [Codex: AGENTS.md][cfg-codex-agents] | Discovery, override file, size cap |
| [Gemini CLI: configuration][cfg-gem-ref] | Layers, file paths, variables |
| [Gemini CLI: enterprise][cfg-gem-ent] | System settings, policy engine |
| [Copilot CLI: config directory][cfg-cop-dir] | Settings order, MDM sources, `COPILOT_HOME` |
| [Copilot CLI: custom instructions][cfg-cop-instr] | Instruction file locations |
| [VS Code: settings][cfg-vsc-set] | Scopes and precedence |
| [VS Code: enterprise policies][cfg-vsc-ent] | Group Policy, profiles, `policy.json` |
| [VS Code: custom instructions][cfg-vsc-instr] | Instruction file names |
| [Cursor: deployment patterns][cfg-cur-dep] | MDM policies, precedence |
| [Cursor: CLI configuration][cfg-cur-cli] | `cli-config.json`, variables |
| [Cursor: sandbox.json][cfg-cur-sbx] | Merge order, enterprise layer |
| [Cursor: rules][cfg-cur-rules] | Rule types, Team Rules |
| [Cursor: hooks][cfg-cur-hooks] | Team and enterprise hooks |
| [Cline: config][cfg-cline-cfg] | Directory layout, variables |
| [Cline: remote configuration][cfg-cline-ent] | Controls per product |
| [Cline: rules][cfg-cline-rules] | Rule locations |
| [Aider: YAML config][cfg-aider-yml] | Search order |
| [Aider: .env][cfg-aider-env] | `.env` locations |
| [Aider: options][cfg-aider-opt] | `AIDER_*` variables |
| [Aider: conventions][cfg-aider-conv] | `CONVENTIONS.md` with `--read` |
| [OpenCode: config][cfg-oc-cfg] | Locations, precedence, managed |
| [OpenCode: policies][cfg-oc-pol] | Policy statements |
| [OpenCode: CLI][cfg-oc-cli] | `OPENCODE_DB` |
| [Amp: configuration][cfg-amp-set] | Settings, managed settings |
| [Amp: allowed models][cfg-amp-models] | Enterprise model policy |
| [Amp: AGENTS.md][cfg-amp-agents] | Lookup paths |
| [Devin Local: customizations][cfg-ws-cust] | Rules, MCP file paths |
| [Devin Local: permissions][cfg-ws-perm] | Permission scopes |
| [Devin: local agent controls][cfg-ws-ctrl] | Root and org controls |

[cc-workflows]: https://code.claude.com/docs/en/common-workflows
[cc-tools]: https://code.claude.com/docs/en/tools-reference
[cc-voice]: https://code.claude.com/docs/en/voice-dictation
[codex-img]: https://learn.chatgpt.com/docs/image-inputs
[codex-cmds]: https://learn.chatgpt.com/docs/developer-commands?surface=cli
[gemini-fs]: https://geminicli.com/docs/tools/file-system/
[gemini-keys]: https://geminicli.com/docs/reference/keyboard-shortcuts/
[copilot-cli]: https://docs.github.com/en/copilot/reference/cli-command-reference
[copilot-cli-use]: https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/overview
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
[cc-auth]: https://code.claude.com/docs/en/authentication
[cc-gw]: https://code.claude.com/docs/en/llm-gateway
[cc-costs]: https://code.claude.com/docs/en/costs
[codex-auth]: https://learn.chatgpt.com/docs/auth
[codex-pricing]: https://learn.chatgpt.com/docs/pricing
[codex-cfg]: https://learn.chatgpt.com/docs/config-file/config-advanced
[codex-bedrock]: https://learn.chatgpt.com/docs/amazon-bedrock
[gemini-auth]: https://geminicli.com/docs/get-started/authentication/
[gemini-cfg]: https://geminicli.com/docs/reference/configuration/
[gemini-cache]: https://geminicli.com/docs/cli/token-caching/
[copilot-byok]: https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/use-byok-models
[copilot-billing]: https://docs.github.com/en/copilot/concepts/billing-and-usage/individuals/billing
[vscode-lm]: https://code.visualstudio.com/docs/copilot/customization/language-models
[cursor-pricing]: https://cursor.com/docs/models-and-pricing
[cursor-keys]: https://cursor.com/docs/settings/api-keys
[cline-start]: https://docs.cline.bot/getting-started/what-is-cline
[cline-oai]: https://docs.cline.bot/provider-config/openai-compatible
[cline-or]: https://docs.cline.bot/provider-config/openrouter
[aider-llms]: https://aider.chat/docs/llms.html
[aider-oai]: https://aider.chat/docs/llms/openai-compat.html
[aider-cache]: https://aider.chat/docs/usage/caching.html
[oc-providers]: https://opencode.ai/docs/providers/
[oc-zen]: https://opencode.ai/docs/zen/
[oc-console-models]: https://opencode.ai/docs/console/models/
[amp-pricing]: https://ampcode.com/docs/pricing
[kiro-pricing]: https://kiro.dev/pricing/
[kiro-headless]: https://kiro.dev/docs/cli/headless/
[zed-api]: https://zed.dev/docs/ai/use-api-access
[zed-plans]: https://zed.dev/docs/ai/plans-and-usage
[kimi-prov]: https://moonshotai.github.io/kimi-code/en/configuration/providers.html
[kimi-docs]: https://www.kimi.com/code/docs/en/
[ag-start]: https://antigravity.google/docs/getting-started?tab=cli
[kimi-start]: https://moonshotai.github.io/kimi-code/en/guides/getting-started.html
[oai-spend]: https://developers.openai.com/api/docs/guides/spend-limits
[cline-prov]: https://docs.cline.bot/getting-started/cline-provider
[aider-repo]: https://github.com/Aider-AI/aider
[amp-routing]: https://ampcode.com/docs/customize/model-routing
[ws-quota]: https://docs.devin.ai/desktop/accounts/quota
[ws-models]: https://docs.devin.ai/desktop/models
[ws-usage]: https://docs.devin.ai/desktop/accounts/usage
[cc-legal]: https://code.claude.com/docs/en/legal-and-compliance
[cc-plan]: https://support.claude.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan
[cc-data]: https://code.claude.com/docs/en/data-usage
[gemini-tos]: https://geminicli.com/docs/resources/tos-privacy/
[gemini-quota]: https://geminicli.com/docs/resources/quota-and-pricing/
[copilot-install]: https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/install-copilot-cli
[copilot-auth]: https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/authenticate-copilot-cli
[copilot-entra]: https://github.blog/changelog/2026-11-17-github-copilot-cli-adds-microsoft-entra-sign-in-as-a-preview
[copilot-oc]: https://github.blog/changelog/2026-01-16-github-copilot-now-supports-opencode/
[copilot-3p]: https://docs.github.com/en/copilot/concepts/agents/about-third-party-coding-agents
[cc-rc]: https://code.claude.com/docs/en/remote-control
[px-capi]: https://github.com/ericc-ch/copilot-api
[px-cpa]: https://github.com/voidsteed/copilot-proxy-api
[cline-cc]: https://docs.cline.bot/provider-config/claude-code
[ag-plans]: https://antigravity.google/docs/plans
[codex-cfgref]: https://learn.chatgpt.com/docs/config-file/config-reference
[gemini-cmds]: https://geminicli.com/docs/reference/commands/
[copilot-ctx]: https://docs.github.com/en/copilot/concepts/agents/copilot-cli/context-management
[vscode-ctx]: https://code.visualstudio.com/docs/copilot/concepts/context
[cursor-slash]: https://cursor.com/docs/cli/reference/slash-commands
[cline-auto]: https://docs.cline.bot/features/auto-compact
[cline-slash]: https://docs.cline.bot/features/slash-commands/new-task
[aider-opts]: https://aider.chat/docs/config/options.html
[aider-cmds]: https://aider.chat/docs/usage/commands.html
[oc-config]: https://opencode.ai/docs/config/
[oc-keybinds]: https://opencode.ai/docs/keybinds/
[amp-threads]: https://ampcode.com/docs/threads
[amp-cli-settings]: https://ampcode.com/docs/cli/settings
[kiro-compaction]: https://kiro.dev/docs/compaction/
[zed-agent-settings]: https://zed.dev/docs/ai/agent-settings
[kimi-sessions]: https://moonshotai.github.io/kimi-code/en/guides/sessions.html
[kimi-config]: https://moonshotai.github.io/kimi-code/en/configuration/config-files.html
[ag-compact]: https://antigravity.google/docs/commands/compact/
[goose-ctx]: https://goose-docs.ai/docs/guides/sessions/smart-context-management
[claude-pdf]: https://platform.claude.com/docs/en/build-with-claude/pdf-support
[claude-vision]: https://platform.claude.com/docs/en/build-with-claude/vision
[oai-astra]: https://developers.openai.com/api/docs/models/gpt-6.2-astra
[oai-files]: https://developers.openai.com/api/docs/guides/file-inputs
[gem-doc]: https://ai.google.dev/gemini-api/docs/document-processing
[gem-vid]: https://ai.google.dev/gemini-api/docs/video-understanding
[codex-rel]: https://github.com/openai/codex/releases/tag/rust-v0.172.0
[gemini-rel]: https://github.com/google-gemini/gemini-cli/releases/tag/v0.71.1
[oc-rel]: https://github.com/anomalyco/opencode/releases/tag/v1.19.6
[aider-rel]: https://github.com/Aider-AI/aider/releases/tag/v0.86.0
[cfg-cc-settings]: https://code.claude.com/docs/en/settings
[cfg-codex-basic]: https://learn.chatgpt.com/docs/config-file/config-basic
[cfg-codex-adv]: https://learn.chatgpt.com/docs/config-file/config-advanced
[cfg-codex-ref]: https://learn.chatgpt.com/docs/config-file/config-reference
[cfg-codex-mgd]: https://learn.chatgpt.com/docs/enterprise/managed-configuration
[cfg-codex-agents]: https://learn.chatgpt.com/docs/agent-configuration/agents-md
[cfg-gem-ref]: https://geminicli.com/docs/reference/configuration/
[cfg-gem-ent]: https://geminicli.com/docs/cli/enterprise/
[cfg-cop-dir]: https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-config-dir-reference
[cfg-cop-instr]: https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions
[cfg-vsc-set]: https://code.visualstudio.com/docs/configure/settings
[cfg-vsc-ent]: https://code.visualstudio.com/docs/enterprise/policies
[cfg-vsc-instr]: https://code.visualstudio.com/docs/agent-customization/custom-instructions
[cfg-cur-dep]: https://cursor.com/docs/enterprise/deployment-patterns
[cfg-cur-cli]: https://cursor.com/docs/cli/reference/configuration
[cfg-cur-sbx]: https://cursor.com/docs/reference/sandbox
[cfg-cur-rules]: https://cursor.com/docs/rules
[cfg-cur-hooks]: https://cursor.com/docs/hooks
[cfg-cline-cfg]: https://docs.cline.bot/getting-started/config
[cfg-cline-ent]: https://docs.cline.bot/enterprise-solutions/configuration/remote-configuration/overview
[cfg-cline-rules]: https://docs.cline.bot/customization/cline-rules
[cfg-aider-yml]: https://aider.chat/docs/config/aider_conf.html
[cfg-aider-env]: https://aider.chat/docs/config/dotenv.html
[cfg-aider-opt]: https://aider.chat/docs/config/options.html
[cfg-aider-conv]: https://aider.chat/docs/usage/conventions.html
[cfg-oc-cfg]: https://opencode.ai/docs/config/
[cfg-oc-pol]: https://opencode.ai/docs/policies/
[cfg-oc-cli]: https://opencode.ai/docs/cli/
[cfg-oc-instr]: https://opencode.ai/docs/instructions/
[cfg-amp-set]: https://ampcode.com/docs/markdown/cli/settings
[cfg-amp-models]: https://ampcode.com/docs/markdown/enterprise/allowed-models
[cfg-amp-agents]: https://ampcode.com/docs/markdown/customize/agents-md
[cfg-ws-cust]: https://docs.devin.ai/desktop/devin-local/customizations
[cfg-ws-perm]: https://docs.devin.ai/desktop/devin-local/permissions
[cfg-ws-ctrl]: https://docs.devin.ai/enterprise/local/controls
