# Reels Setup — one time

## Prerequisite (run first — system repo)
1. System repo ka `Onetime.md` complete ho: opencode install (manual), repo clone, Kaggle Secrets set.
2. System repo ka `Firststartup.md` ho: relink + bootstrap + verify (Node 22 + HyperFrames + Chrome).
3. Kaggle Secrets set ho: `WORKER_TOKEN` (gateway auth) aur `GITHUB_TOKEN` (repo push ke liye, optional).
4. `yt-dlp` install ho (sirf agar link se reel banana hai): `pip install -q yt-dlp` (abhi nahi hai).

## Then
- `ReelProcedure.md` follow karo (RP-1).
- Master prompt chahiye? `ReelMasterprompt.md` bhar do, ya empty chor do (fallback chalaega).
- Gateway: `BASE` + `TOKEN` — dono Kaggle Secrets se / cell.py se auto-load hoga.

Repo structure: `_template/` sirf reusable build system. `projects/<slug>/` mein naya reel banoge.