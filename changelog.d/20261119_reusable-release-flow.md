### Changed

- Release flow moved to the estate's reusable workflows: `bump.yaml` (signed bump commit, scriv collected via uvx) replaces the local `bump-my-version.yaml`, and `release.yaml` tags and publishes the GitHub Release in one run, replacing `tag-release.yaml`; `publish-release.yaml` stays as a manual fallback. CONTRIBUTING's release steps updated.
