# Putting this folder on GitHub — for someone who has never used Git

← [START_HERE.md](../START_HERE.md) · **Owner: S3** · **20 minutes, once.**

## What Git actually is, in 4 lines

- **Git** = an undo history for a folder. It lives *on your laptop*.
- **GitHub** = a website that holds a copy of that history so other people can get it.
- **commit** = "save a snapshot, with a note saying what changed".
- **push** = "send my snapshots to GitHub". **pull** = "get everyone else's".

That is the whole model. Everything else is detail you do not need this week.

---

## What goes in, what stays out

The AI weights (139 MB), the advisor's code (751 MB) and the videos **cannot go
on GitHub** — it rejects any single file over 100 MB. That is already handled:
[`.gitignore`](../.gitignore) tells Git to skip them.

| Goes on GitHub | Stays on Google Drive |
|---|---|
| All the `.md` plans and notes | `best.pt` and every other `.pt` |
| Our own code in `06_Software/oceaneye/` | `06_Software/advisor_code/` |
| The script and slides (`.docx`, `.pptx`) | All `.mp4` footage |
| The competition rules | `Mamba-YOLO-main.zip` |

**Do both.** GitHub for the words, Drive for the heavy files. Put the Drive
link at the top of the repo's README so nobody has to ask.

---

## Set it up — copy these one line at a time

**Already done for you:** `git init` has been run and everything is committed. You can
check with `git log --oneline` — you should see two entries. So skip straight to
creating the repo on GitHub.

Open a terminal in this folder. You are already logged in as `Dararoth-ML`, so:

```bash
gh repo create oceaneye-group22 --private --source=. --push
```

- `--private` = **only people you invite can see it.** This matters: it holds
  Prof. Wang's unpublished work.
- `--source=.` = use this folder.
- `--push` = upload immediately.

Then invite your two teammates (they need GitHub accounts first — free, 2 min):

```bash
gh repo edit --add-collaborator THEIR_GITHUB_USERNAME
```

Repeat for the second teammate.

---

## The only 3 commands you need after that

```bash
git pull                        # before you start working — get their changes
git add . && git commit -m "what I changed"   # after you finish
git push                        # send it
```

**Pull before you work. Push when you stop.** That is the rhythm. If you both
edit the same file at the same time Git will complain — when that happens,
message the team rather than fighting it. You have five days; do not learn
merge conflicts this week.

---

## What your teammates do, once

```bash
git clone https://github.com/Dararoth-ML/oceaneye-group22.git
cd oceaneye-group22
```

Then they download the heavy files from Google Drive into the matching folders.

---

## If something goes wrong

| Problem | Fix |
|---|---|
| `remote contains work that you do not have` | `git pull` first, then push again |
| Pushed something secret by accident | Tell the team, then ask for help — don't just delete the file, the history keeps it |
| A file is over 100 MB and push fails | It should be in `.gitignore`. Add it, then `git rm --cached path/to/file` |
| Completely lost | `git status` tells you where you are. It is safe to run any time. |

> **Not a backup.** GitHub does not hold `best.pt`. **Two USB sticks + a cloud
> folder** is the backup plan for the weights, and that is still S2's job.
