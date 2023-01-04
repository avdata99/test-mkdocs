# Re sync with upstream template

One way to do it could be:

```bash
git remote add upstream git@github.com:okfn/okfn-collaborative-docs.git
git fetch upstream
git rebase upstream/main main
# Resolve conflicts if any
git push -f origin main
```
