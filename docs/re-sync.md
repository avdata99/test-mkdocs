# Re sync with upstream template

This is not a simple process.  
You can try this methods but you may need to do some manual changes.  

If you want to update your documentation to latest version, you can run

```bash
python3 okf_collab_docs/run.py update-from-template
```

You can also do it manually by running

```bash
git remote add upstream git@github.com:okfn/okfn-collaborative-docs.git
git fetch upstream
git rebase -Xours upstream/main main
git push -f origin main
```
