---
name: feedback_stacks_not_kept_in_project
description: stack recipes must not stay in a project; /architecture asks the hosting inputs (domains) itself
metadata:
  type: feedback
---

`.context/stacks/` must not stay in a project once the stack-specific setup is done, and `/architecture` itself must ask the hosting and deployment inputs (domains, DNS, server access) instead of leaving them to the setup.

**Why:** the user did not want the recipes to linger, and noticed that domains were never asked before the architecture decision; deleting the recipes inside `/architecture` also removed the setup guide before it ran. See [[feedback_initialization_architecture_split]].

**How to apply:** `/architecture` prunes unused stack conventions only; each recipe's last step deletes `.context/stacks/` after the setup. Never move domain or hosting questions into `/init-project`.
