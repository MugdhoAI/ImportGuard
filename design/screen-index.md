# ImportGuard Screen Index (As-Built)

Screenshots: `visual-qa/*.png` (synthetic demo data, dark unless noted).
States quoted are implemented and render-tested.

| Route | Template | Shots | States covered |
|---|---|---|---|
| `/home` | `home.html` | `home-user-dark-1280` | Guest marketing; user welcome + recent + usage; empty activity |
| `/dashboard` | `dashboard.html` | `dashboard-{dark,light}-1280`, `-768`, `-390` | Guest/user; 4 stats; empty activity; attention link |
| `/app`, `/workspace` | `app.html` + `app.js` | (owner browser run) | Upload/profile/preview/mapping/review/export/replay; guest save-nudge |
| `/history` | `history.html` | `history-dark-1280`, `-768` | Search, status filter, pagination, validation pills, empty/no-match |
| `/exports` | `exports.html` | `exports-dark-1280` | Pending banner, download pills, guest gate links, empty |
| `/exports/pending` | `pending.html` | — | Auth-only; claimed-work list; empty |
| `/exports/{id}` | `export_detail.html` | — | Pending/downloaded/expired; owner vs guest gate |
| `/billing` | `billing.html` | — | Current plan, unavailable upgrades, no-invoices empty, danger zone |
| `/payments` | `product_page.html` | — | All methods unavailable; no card collection (honest) |
| `/teams` | `teams.html` | — | List + create; empty |
| `/teams/{id}` | `team_detail.html` | `team-detail-dark-1280` | Members/roles, invites + share link, shared history, leave |
| `/invitations/accept` | `invite_accept.html` | — | Invalid/expired; confirm; wrong-email error |
| `/settings` | `settings.html` | `settings-dark-1280`, `-390` | Profile, password, sessions, delete; notices/errors |
| `/help` | `help.html` | — | Workflow, guests/accounts, recipes, troubleshooting |
| `/login`, `/signup` | `auth.html` | — | Errors, reset notice, forgot link (login) |
| `/forgot-password`, `/reset-password` | `forgot.html`, `reset.html` | — | Shell-less; honest not-configured notice; token errors |
| `/admin` | `admin.html` | `admin-dark-1280` | Counts, provider notice, plan distribution, subscriptions |
| `/privacy` | `privacy.html` | — | Unchanged notice page |

Unshot pages reuse the same reviewed shell/table/form components; all are
covered by the every-page render sweep test (status + `None`-leak check).
