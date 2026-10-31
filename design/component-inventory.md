# ImportGuard Component Inventory (As-Built)

All components are server-rendered Jinja + shared CSS in
`app/static/css/styles.css`. No component ships without a real action.

## Shell

| Component | Classes / file | Variants |
|---|---|---|
| Sidebar | `.app-sidebar`, `base.html` | WORKSPACE / YOUR DATA / ACCOUNT groups; ADMIN (admins only); plan footer (users); auth block; mobile top-bar mode |
| Topbar | `.topbar`, `.crumbs` | Breadcrumb (Home + `crumb_for()` label) + theme toggle |
| Page header | `.product-heading`, `.eyebrow` | Title + description + optional action(s) (`.heading-actions`) |

## Data

| Component | Classes | Variants |
|---|---|---|
| Table | `.table-scroll`, `.history-table` | Full/paginated; wraps text at tablet; horizontal scroll on small screens |
| Status pill | `.pill` + `.pill-pending` / `.pill-downloaded` / `.pill-expired` | Download state (Exports) and validation state (History: Completed/Needs review) |
| Stats | `.dashboard-stats`, `.product-card` | 4-up → 2-up → 1-up responsive |
| Detail list | `.detail-list` (`dl`) | 2-col → stacked on mobile |
| Preview table | `.preview-table` | Sticky header, ellipsis cells, row-count caption (workspace JS) |

## Forms & feedback

| Component | Classes | Variants |
|---|---|---|
| Field | `.auth-field` (+`select` support) | Label + input/select; used on all forms |
| Filter row | `.filter-row` | Search + select + submit + clear |
| Pager | `.pager` | Prev/next with preserved query params |
| Messages | `.message` + `.error` / `.success` / `.notice` | Alert/status roles |
| Inline row actions | `.inline-form`, `.link-button` | Revoke/set/remove inside tables |
| Share link | `.share-link` | Invitation URL display (manual share) |
| Empty states | `.empty-activity` | Icon + explanation + next action link |
| Danger zone | `.danger-zone`, `.button-danger` | Delete account (password-confirmed) |

## Buttons

`.button`, `.button-secondary`, `.button-small`, `.button-quiet`,
`.link-button`, `.text-button` — every button submits a real form, navigates,
or runs a workspace action. Disabled states carry `title` explanations.
