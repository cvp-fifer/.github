#!/usr/bin/env bash
# Seed the labels referenced by the org issue forms (ISSUE_TEMPLATE/*.yml).
# GitHub silently skips a form's `labels:` when the label doesn't exist in the
# target repo — run this against every new repo in the org. Idempotent (--force).
set -euo pipefail

ORG=cvp-fifer
REPOS=(fifer fifer-web fifer-desktop evs-guardian fifer-inspect fifer-docs)

seed() { # name color description
  for repo in "${REPOS[@]}"; do
    gh label create "$1" -R "$ORG/$repo" --force --color "$2" --description "$3"
    echo "  $ORG/$repo: $1"
  done
}

seed bug     d73a4a "Something is broken or behaving wrong"
seed feature a2eeef "New capability, framed as a user story"
seed task    ededed "Concrete work item"
seed epic    3e4b9e "Multi-issue outcome tracked via sub-issues"
seed spike   d4c5f9 "Timeboxed investigation that informs a decision"
