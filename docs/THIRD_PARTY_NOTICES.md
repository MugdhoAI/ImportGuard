# ImportGuard Third-Party Notices and License Inventory

Maintain this file when dependencies, copied source, fonts, icons, images, or other assets are added.

| Package/asset | Version/source | License/terms checked? | Required attribution/notice | Decision/notes |
|---|---|---|---|---|
| FastAPI | 0.162.0; https://github.com/fastapi/fastapi | Installed distribution license file inspected | MIT | No source copied |
| Uvicorn | 0.54.0; https://github.com/encode/uvicorn | Installed distribution license file inspected | BSD-3-Clause | No source copied |
| Jinja2 | 3.1.6; https://github.com/pallets/jinja | Installed distribution license file inspected | BSD-3-Clause | No source copied |
| Pydantic | 2.14.1; https://github.com/pydantic/pydantic | Installed distribution license file inspected | MIT | No source copied |
| python-multipart | 0.0.32; https://github.com/Kludex/python-multipart | Installed distribution license file inspected | Apache-2.0 | No source copied |
| python-dotenv | 1.2.4; https://github.com/theskumar/python-dotenv | Installed distribution license file inspected | BSD-3-Clause | No source copied |
| OpenAI Python SDK | 2.54.0; https://github.com/openai/openai-python | Installed distribution license file inspected | Apache-2.0 | Optional Meta-compatible API client |
| HTTPX | 0.28.1; https://github.com/encode/httpx | Installed distribution license file inspected | BSD-3-Clause | TestClient dependency |
| pytest | 8.4.2; https://github.com/pytest-dev/pytest | Installed distribution license file inspected | MIT | Development/test only |
| Ruff | 0.16.10; https://github.com/astral-sh/ruff | Installed distribution license file inspected | MIT | Development only |
| ThreeUI Community components (Predictive Arc, GlassAiButton, AnimatedTopDock, stylesheet) | `frontend/src/vendor/threeui/`; canonical bundles from https://threeui.com | MIT license text preserved in `frontend/src/vendor/threeui/LICENSE` | Keep vendor copyright + license notices; see `frontend/src/vendor/threeui/THIRD_PARTY_NOTICES.md` | Vendor files unchanged; product adapters live outside the vendor directory |
| Fragment Mono font (`fragment-mono.woff2`, 15,176 bytes) | ThreeUI source path; SHA-256 `4f4dc27f…3ab96c` | OFL 1.1 text preserved in `frontend/src/vendor/threeui/FONT-LICENSES.md` | Keep OFL notices | Exact verified asset only |
| Three.js runtimes (bundled + `three128` npm alias 0.128.0) | three.js authors; https://github.com/mrdoob/three.js | MIT / SPDX headers retained in files | Keep in-file headers | No source copied outside vendor dir |
| React, React-DOM, Vite, Vitest, Puppeteer Core, axe-core, fflate, TypeScript | `frontend/package.json` (pinned) | MIT/Apache-2.0/BSD family per package metadata; recheck before release | Keep package license files on distribution | Frontend build/test only; no key or app data involved |

Rules:
- Verify the actual license for each direct dependency and copied asset.
- Keep attribution and required notices.
- The supplied ThreeUI source hashes identify content but do not prove reuse rights. Do not copy a ThreeUI component/asset until current source and license/terms have been inspected.
- Do not include third-party project content without proper rights.
