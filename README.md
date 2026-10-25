# TON Price Bot — Clean Rebuild

## Files
- `gh_price_once.py`: fetches TON/USD, converts to IQD, and posts a Telegram message.
- `.github/workflows/price.yml`: scheduled run every 10 minutes.

## Setup
1. Create a new GitHub repository.
2. Upload `gh_price_once.py` to the repository root.
3. Upload `.github/workflows/price.yml` at that exact path.
4. In repository Settings → Secrets and variables → Actions, create a repository secret:
   - Name: `BOT_TOKEN`
   - Secret: your Telegram bot token (do not put it in source code).
5. Add the bot as an administrator to `@Gram_Price_Today` and allow it to post messages.
6. Open Actions and enable workflows if prompted.
7. Use Run workflow once to test. After that, schedule runs automatically.

## Schedule
`*/10 * * * *` requests a run every 10 minutes. GitHub Actions can delay scheduled jobs; exact minute-level timing is not guaranteed. Scheduled workflows should be on the repository's default branch. GitHub may disable scheduled workflows in inactive public repositories.

## Important
If a bot token was ever posted publicly or sent into an untrusted place, revoke it using BotFather and save the new token as the `BOT_TOKEN` secret.
