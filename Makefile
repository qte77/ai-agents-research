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
	setup_node setup_lychee setup_mdlint setup_skills setup_all \
	check_links check_docs autofix lint \
	help
.DEFAULT_GOAL := help


# -- config --
NODE_VERSION ?= 22.11.0
NODE_DIR     := $(HOME)/.local/share/node
NODE_BIN     := $(NODE_DIR)/bin
LOCAL_BIN    := $(HOME)/.local/bin

# Sibling repo providing plugin skills (docs-governance, cc-meta)
UTILS_PLUGIN_DIR ?= $(HOME)/repos/claude-code-utils-plugin
SKILLS_DIR       := .claude/skills


# MARK: SETUP


setup_node: ## Install Node.js user-locally to ~/.local/share/node (no sudo)
	if [ -x "$(NODE_BIN)/node" ]; then
		echo "node already installed: $$($(NODE_BIN)/node --version) (at $(NODE_DIR))"
	elif command -v node > /dev/null 2>&1; then
		echo "node already installed on PATH: $$(node --version)"
	else
		echo "Installing Node.js $(NODE_VERSION) to $(NODE_DIR) ..."
		mkdir -p $(NODE_DIR)
		curl -sSfL https://nodejs.org/dist/v$(NODE_VERSION)/node-v$(NODE_VERSION)-linux-x64.tar.xz \
			| tar -xJ --strip-components=1 -C $(NODE_DIR) \
			&& echo "node installed — add to PATH: export PATH=$(NODE_BIN):\$$PATH" \
			|| echo "Install failed — download manually from https://nodejs.org/dist/v$(NODE_VERSION)/"
	fi

setup_lychee: ## Install lychee link checker user-locally to ~/.local/bin (no sudo)
	if command -v lychee > /dev/null 2>&1; then
		echo "lychee already installed: $$(lychee --version)"
	else
		mkdir -p $(LOCAL_BIN)
		curl -sSfL https://github.com/lycheeverse/lychee/releases/latest/download/lychee-x86_64-unknown-linux-gnu.tar.gz \
			| tar xz -C $(LOCAL_BIN) \
			&& echo "lychee installed to $(LOCAL_BIN) — ensure it is on PATH" \
			|| echo "Install failed — download manually from https://github.com/lycheeverse/lychee/releases"
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

setup_skills: ## Symlink docs-governance + compacting-context skills from sibling claude-code-utils-plugin (local dev; gitignored)
	if [ ! -d "$(UTILS_PLUGIN_DIR)" ]; then
		echo "ERROR: expected sibling repo at $(UTILS_PLUGIN_DIR)"
		echo "Clone: git clone https://github.com/qte77/claude-code-utils-plugin $(UTILS_PLUGIN_DIR)"
		echo "Or override: make setup_skills UTILS_PLUGIN_DIR=/path/to/claude-code-utils-plugin"
		exit 1
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

setup_all: setup_lychee setup_mdlint ## Install all tooling (lychee + node + markdownlint-cli2)


# MARK: DEV


check_links: ## Check links with lychee
	if command -v lychee > /dev/null 2>&1; then
		lychee --config lychee.toml .
	else
		echo "lychee not installed — run: make setup_lychee"
		exit 1
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

lint: check_links check_docs ## Run all linters (links + markdown)


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
