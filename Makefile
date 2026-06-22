# Requires GNU Make >= 3.82 for .ONESHELL
# macOS ships 3.81 as of Sequoia 15.4 (2025-03, Apple avoids GPLv3).
# Ref: https://opensource.apple.com/releases/ (validated 2026-04-10)
# Fix: brew install make → use gmake (not make)
ifeq ($(filter oneshell,$(.FEATURES)),)
$(error GNU Make >= 3.82 required. macOS: brew install make, then use gmake)
endif

.SILENT:
.ONESHELL:
.PHONY: \
	setup_node setup_lychee setup_mdlint setup_actionlint setup_shellcheck setup_skills setup_all \
	check_links check_docs check_actions autofix lint test \
	graph-build graph-html graph-query graph-explain graph-path graph-fonts graph-page preview \
	help
.DEFAULT_GOAL := help


# -- config --
NODE_VERSION       ?= 22.11.0
ACTIONLINT_VERSION ?= 1.7.12
NODE_DIR           := $(HOME)/.local/share/node
NODE_BIN           := $(NODE_DIR)/bin
LOCAL_BIN          := $(HOME)/.local/bin

# graphify knowledge graph — https://qte77.github.io/ai-agents-research/
# GRAPHIFY: binary (override for a side-loaded build, e.g.
#   GRAPHIFY=/workspaces/external/graphify/.venv/bin/graphify)
# GRAPHIFY_BACKEND: LLM backend for headless `make graph-build` (needs its API key)
# PYTHON: interpreter for the stdlib-only publish helper (no deps, so no uv needed)
GRAPHIFY           ?= graphify
GRAPHIFY_BACKEND   ?= gemini
PYTHON             ?= python3

# -- OS / arch detection --
UNAME_S := $(shell uname -s)
UNAME_M := $(shell uname -m)
ifeq ($(UNAME_S),Darwin)
  PKG_CMD := brew install
else ifeq ($(shell command -v dnf 2>/dev/null),)
  ifeq ($(shell command -v apt-get 2>/dev/null),)
    ifeq ($(shell command -v pacman 2>/dev/null),)
      PKG_CMD := echo "No supported package manager (brew/dnf/apt-get/pacman)" && exit 1 &&
    else
      PKG_CMD := sudo pacman -S --noconfirm
    endif
  else
    PKG_CMD := sudo apt-get install -y -qq
  endif
else
  PKG_CMD := sudo dnf install -y
endif

ifeq ($(UNAME_M),x86_64)
  NODE_ARCH   := x64
  LYCHEE_ARCH := x86_64-unknown-linux-gnu
else ifeq ($(UNAME_M),aarch64)
  NODE_ARCH   := arm64
  LYCHEE_ARCH := aarch64-unknown-linux-gnu
else ifeq ($(UNAME_M),arm64)
  NODE_ARCH   := arm64
  LYCHEE_ARCH := aarch64-apple-darwin
else
  NODE_ARCH   := $(UNAME_M)
  LYCHEE_ARCH := $(UNAME_M)-unknown-linux-gnu
endif

# Source plugin providing skills (docs-governance, cc-meta).
# Default: clone from GitHub to an XDG cache path. Override
# UTILS_PLUGIN_DIR to point at an existing local clone.
UTILS_PLUGIN_URL ?= https://github.com/qte77/claude-code-plugins
UTILS_PLUGIN_DIR ?= $(HOME)/.cache/claude-code-plugins
SKILLS_DIR       := .claude/skills


# MARK: SETUP


setup_node: ## Install Node.js user-locally to ~/.local/share/node (no sudo)
	if [ -x "$(NODE_BIN)/node" ]; then
		echo "node already installed: $$($(NODE_BIN)/node --version) (at $(NODE_DIR))"
	elif command -v node > /dev/null 2>&1; then
		echo "node already installed on PATH: $$(node --version)"
	elif [ "$(UNAME_S)" = "Darwin" ]; then
		echo "Installing Node.js via brew ..."
		brew install node
	else
		echo "Installing Node.js $(NODE_VERSION) ($(UNAME_S)/$(NODE_ARCH)) to $(NODE_DIR) ..."
		mkdir -p $(NODE_DIR)
		curl -sSfL https://nodejs.org/dist/v$(NODE_VERSION)/node-v$(NODE_VERSION)-linux-$(NODE_ARCH).tar.xz \
			| tar -xJ --strip-components=1 -C $(NODE_DIR) \
			|| { echo "Install failed — download manually from https://nodejs.org/dist/v$(NODE_VERSION)/"; exit 1; }
	fi
	mkdir -p $(LOCAL_BIN)
	for bin in node npm npx; do \
		if [ -x "$(NODE_BIN)/$$bin" ] && [ ! -e "$(LOCAL_BIN)/$$bin" ]; then \
			ln -s "$(NODE_BIN)/$$bin" "$(LOCAL_BIN)/$$bin"; \
			echo "symlinked $$bin -> $(LOCAL_BIN)/$$bin"; \
		fi; \
	done

setup_lychee: ## Install lychee link checker user-locally to ~/.local/bin (no sudo)
	if command -v lychee > /dev/null 2>&1; then
		echo "lychee already installed: $$(lychee --version)"
	elif [ "$(UNAME_S)" = "Darwin" ]; then
		echo "Installing lychee via brew ..."
		brew install lychee
	else
		echo "Installing lychee ($(LYCHEE_ARCH)) to $(LOCAL_BIN) ..."
		mkdir -p $(LOCAL_BIN)
		# Tarball contains a wrapper dir (lychee-<target>/lychee).
		# Mirror lycheeverse/lychee-action's pattern: extract to tmpdir, find
		# binary via glob, install with explicit mode. Avoids GNU-tar-only
		# flags (--wildcards, --strip-components with member matching) so the
		# recipe is portable to BSD tar.
		tmp=$$(mktemp -d) \
			&& curl -sSfL https://github.com/lycheeverse/lychee/releases/latest/download/lychee-$(LYCHEE_ARCH).tar.gz \
				| tar xz -C "$$tmp" \
			&& install -m 755 "$$tmp"/lychee-*/lychee $(LOCAL_BIN)/lychee \
			&& rm -rf "$$tmp" \
			&& echo "lychee installed to $(LOCAL_BIN)/lychee — ensure $(LOCAL_BIN) is on PATH" \
			|| { rm -rf "$$tmp"; echo "Install failed — download manually from https://github.com/lycheeverse/lychee/releases"; exit 1; }
	fi

setup_mdlint: setup_node ## Install markdownlint-cli2 via user-local npm (no sudo)
	export PATH="$(NODE_BIN):$$PATH"
	if [ -x "$(NODE_BIN)/markdownlint-cli2" ]; then
		echo "markdownlint-cli2 already installed: $$(markdownlint-cli2 --version 2>&1 | head -1)"
	elif command -v markdownlint-cli2 > /dev/null 2>&1; then
		echo "markdownlint-cli2 already installed (system PATH): $$(markdownlint-cli2 --version 2>&1 | head -1)"
	else
		echo "Installing markdownlint-cli2 into $(NODE_DIR) ..."
		if [ -x "$(NODE_BIN)/npm" ] || command -v npm > /dev/null 2>&1; then
			npm install -g markdownlint-cli2
		else
			echo "ERROR: npm not found after setup_node — check Node install"
			exit 1
		fi
	fi

setup_actionlint: ## Install actionlint user-locally to ~/.local/bin (no sudo)
	if command -v actionlint > /dev/null 2>&1; then
		echo "actionlint already installed: $$(actionlint -version | head -1)"
	else
		case "$(UNAME_S)" in \
		Linux) ACTIONLINT_OS="linux" ;; \
		Darwin) ACTIONLINT_OS="darwin" ;; \
		*) echo "ERROR: unsupported OS for actionlint binary"; exit 1 ;; \
		esac
		case "$(UNAME_M)" in \
		x86_64) ACTIONLINT_ARCH="amd64" ;; \
		aarch64|arm64) ACTIONLINT_ARCH="arm64" ;; \
		*) echo "ERROR: unsupported arch for actionlint binary"; exit 1 ;; \
		esac
		echo "Installing actionlint $(ACTIONLINT_VERSION) ($$ACTIONLINT_OS/$$ACTIONLINT_ARCH) to $(LOCAL_BIN) ..."
		mkdir -p $(LOCAL_BIN)
		# Tarball contains the binary at the root (no wrapper dir) — single
		# extract step. Mirror lychee's mktemp + install -m 755 hygiene.
		tmp=$$(mktemp -d) \
			&& curl -sSfL "https://github.com/rhysd/actionlint/releases/download/v$(ACTIONLINT_VERSION)/actionlint_$(ACTIONLINT_VERSION)_$${ACTIONLINT_OS}_$${ACTIONLINT_ARCH}.tar.gz" \
				| tar xz -C "$$tmp" \
			&& install -m 755 "$$tmp/actionlint" $(LOCAL_BIN)/actionlint \
			&& rm -rf "$$tmp" \
			&& echo "actionlint installed to $(LOCAL_BIN)/actionlint — ensure $(LOCAL_BIN) is on PATH" \
			|| { rm -rf "$$tmp"; echo "Install failed — download manually from https://github.com/rhysd/actionlint/releases"; exit 1; }
	fi

setup_skills: ## Clone claude-code-plugins (if missing) and symlink its skills into .claude/skills (gitignored; zero sudo)
	if [ ! -d "$(UTILS_PLUGIN_DIR)/.git" ]; then
		echo "Cloning $(UTILS_PLUGIN_URL) to $(UTILS_PLUGIN_DIR) ..."
		mkdir -p $$(dirname $(UTILS_PLUGIN_DIR))
		git clone --depth=1 $(UTILS_PLUGIN_URL) $(UTILS_PLUGIN_DIR) \
			|| { echo "ERROR: clone failed — check network, URL, or override UTILS_PLUGIN_DIR=/path/to/local/clone"; exit 1; }
	else
		echo "Plugin repo already present at $(UTILS_PLUGIN_DIR)"
	fi
	mkdir -p $(SKILLS_DIR)
	for skill_path in \
		$(UTILS_PLUGIN_DIR)/plugins/docs-governance/skills/enforcing-doc-hierarchy \
		$(UTILS_PLUGIN_DIR)/plugins/docs-governance/skills/maintaining-agents-md \
		$(UTILS_PLUGIN_DIR)/plugins/cc-meta/skills/compacting-context; do
		name=$$(basename $$skill_path)
		if [ ! -d "$$skill_path" ]; then
			echo "WARN: source skill missing: $$skill_path — skipping"
			continue
		fi
		if [ -L "$(SKILLS_DIR)/$$name" ]; then
			echo "$$name: already symlinked"
		elif [ -e "$(SKILLS_DIR)/$$name" ]; then
			echo "WARN: $(SKILLS_DIR)/$$name exists and is not a symlink — skipping"
		else
			ln -s $$skill_path $(SKILLS_DIR)/$$name
			echo "$$name: linked"
		fi
	done

setup_shellcheck: ## Install shellcheck user-locally to ~/.local/bin (no sudo); actionlint runs it when on PATH
	if command -v shellcheck > /dev/null 2>&1; then
		echo "shellcheck already installed: $$(shellcheck --version 2>&1 | grep '^version:' || true)"
	elif [ "$(UNAME_S)" = "Darwin" ]; then
		echo "Installing shellcheck via brew ..."
		brew install shellcheck
	else
		case "$(UNAME_M)" in \
		x86_64) SC_ARCH="x86_64" ;; \
		aarch64|arm64) SC_ARCH="aarch64" ;; \
		*) echo "ERROR: unsupported arch for shellcheck binary"; exit 1 ;; \
		esac
		echo "Installing shellcheck (stable, linux/$$SC_ARCH) to $(LOCAL_BIN) ..."
		mkdir -p $(LOCAL_BIN)
		# Tarball (.tar.xz) holds shellcheck-stable/shellcheck — extract to tmp,
		# install with explicit mode (mirrors setup_lychee / setup_actionlint).
		tmp=$$(mktemp -d) \
			&& curl -sSfL "https://github.com/koalaman/shellcheck/releases/download/stable/shellcheck-stable.linux.$${SC_ARCH}.tar.xz" \
				| tar xJ -C "$$tmp" \
			&& install -m 755 "$$tmp"/shellcheck-stable/shellcheck $(LOCAL_BIN)/shellcheck \
			&& rm -rf "$$tmp" \
			&& echo "shellcheck installed to $(LOCAL_BIN)/shellcheck — ensure $(LOCAL_BIN) is on PATH" \
			|| { rm -rf "$$tmp"; echo "Install failed — download manually from https://github.com/koalaman/shellcheck/releases"; exit 1; }
	fi

setup_all: setup_lychee setup_mdlint setup_actionlint setup_shellcheck ## Install all tooling (lychee + node + markdownlint-cli2 + actionlint + shellcheck)


# MARK: DEV


check_links: ## Check links with lychee
	export PATH="$(LOCAL_BIN):$$PATH"
	if ! command -v lychee > /dev/null 2>&1; then
		echo "lychee not installed — run: make setup_lychee"
		exit 1
	fi
	if [ ! -f lychee.toml ]; then
		echo "lychee.toml not found — running without config"
		lychee .
	else
		lychee --config lychee.toml .
	fi

check_docs: ## Lint markdown files (reads .markdownlint.json)
	export PATH="$(NODE_BIN):$$PATH"
	if command -v markdownlint-cli2 > /dev/null 2>&1; then
		markdownlint-cli2 "README.md" "CHANGELOG.md" "CONTRIBUTING.md" "docs/**/*.md"
	else
		echo "markdownlint-cli2 not installed — run: make setup_mdlint"
		exit 1
	fi

autofix: ## Auto-fix markdown lint issues (markdownlint --fix)
	export PATH="$(NODE_BIN):$$PATH"
	if command -v markdownlint-cli2 > /dev/null 2>&1; then
		markdownlint-cli2 --fix "README.md" "CHANGELOG.md" "CONTRIBUTING.md" "docs/**/*.md"
	else
		echo "markdownlint-cli2 not installed — run: make setup_mdlint"
		exit 1
	fi

check_actions: ## Lint GitHub Actions workflows + composite actions
	export PATH="$(LOCAL_BIN):$$PATH"
	if ! command -v actionlint > /dev/null 2>&1; then
		echo "actionlint not installed — run: make setup_actionlint"
		exit 1
	fi
	actionlint -color

lint: check_links check_docs check_actions ## Run all linters (links + markdown + actions)

test: ## Run unit tests (stdlib unittest; covers .github/scripts/lib + scripts/pages_build modules)
	$(PYTHON) -m unittest discover -s tests -v


# MARK: GRAPH


# Query/navigate ops are free (no LLM). Building needs an extraction model: the
# /graphify skill (key-free, uses the Claude Code session) or `graphify extract`
# with an API key. Config (GRAPHIFY / GRAPHIFY_BACKEND / PYTHON) is at the top.

graph-build: ## Headless full rebuild (AST + semantic) — needs an LLM backend API key
	$(GRAPHIFY) extract . --backend $(GRAPHIFY_BACKEND)
	$(GRAPHIFY) label . --backend $(GRAPHIFY_BACKEND)

graph-html: ## Re-render graphify-out/graph.html from graph.json (no LLM)
	if [ ! -f graphify-out/graph.json ]; then echo "no graph.json — build first (/graphify skill or make graph-build)"; exit 1; fi
	$(GRAPHIFY) export html

graph-query: ## Query the graph: make graph-query Q="how does X work?"
	if [ -z "$(Q)" ]; then echo 'Usage: make graph-query Q="<question>"'; exit 2; fi
	$(GRAPHIFY) query "$(Q)"

graph-explain: ## Explain a node + neighbors: make graph-explain N="Node Label"
	if [ -z "$(N)" ]; then echo 'Usage: make graph-explain N="<node>"'; exit 2; fi
	$(GRAPHIFY) explain "$(N)"

graph-path: ## Shortest path between nodes: make graph-path A="Node A" B="Node B"
	if [ -z "$(A)" ] || [ -z "$(B)" ]; then echo 'Usage: make graph-path A="<node>" B="<node>"'; exit 2; fi
	$(GRAPHIFY) path "$(A)" "$(B)"

graph-fonts: ## Fetch self-hosted brand fonts (Inter + JetBrains Mono woff2) into ui/assets/fonts/
	$(PYTHON) scripts/fetch-web-fonts.py

graph-page: graph-html ## Render + EyeRest-restyle the graph into committed ui/graph.html (commit + push; the gh-pages workflow deploys)
	$(PYTHON) scripts/render-graph-page.py

preview: ## Serve the branded site (ui/) locally at http://localhost:$$PORT (default 8000)
	echo "Serving ui/ at http://localhost:$${PORT:-8000}/  ->  / (landing), /graph.html  (Ctrl-C to stop)"
	echo "Tip: run 'make graph-fonts' first to preview the real brand fonts (else system-ui fallback)."
	$(PYTHON) -m http.server $${PORT:-8000} --directory ui


# MARK: HELP


help: ## Show available recipes grouped by section
	echo "Usage: make [recipe]"
	echo ""
	awk '/^# MARK:/ { \
		section = substr($$0, index($$0, ":")+2); \
		printf "\n\033[1m%s\033[0m\n", section \
	} \
	/^[a-zA-Z0-9_-]+:.*?##/ { \
		helpMessage = match($$0, /## (.*)/); \
		if (helpMessage) { \
			recipe = $$1; \
			sub(/:/, "", recipe); \
			printf "  \033[36m%-22s\033[0m %s\n", recipe, substr($$0, RSTART + 3, RLENGTH) \
		} \
	}' $(MAKEFILE_LIST)
