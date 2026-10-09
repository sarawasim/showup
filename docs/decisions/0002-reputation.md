# 0002: Reputation

Date: 2026-10-08. Status: agreed for sprint 1; sprint 2 and 3 items are designed, not built.

This answers the proposal and pitch feedback: how a newcomer joins a first game, who verifies
attendance, how an incorrect report is challenged, and how hosts are held accountable.

## The number

Reputation is a show-up rate with a cushion of three attended games that every player is
given on day one:

```
reputation = round(100 × (games showed up to + 3) ÷ (games marked + 3))
```

| Situation | Score |
|---|---|
| Brand new | 100 |
| First game, no-show | 75 |
| No-show, then five shows | 89 |
| Twenty shows, one no-show | 96 |
| Three no-shows, nothing else | 50 |

It is recomputed from the `attendance` table every time a host marks a game and stored on
`users.reputation`. The formula and every constant live in `backend/app/reputation.py`.

## Rules

1. **Newcomers start at 100 and are labelled "New"** until they have three marked or hosted
   games. Hosts see the score, the games played count and the label together, so a fresh
   100 and a veteran 100 are not confused. This is the initial access route the feedback asked for.
2. **A host may require anything up to 100.** The team chose no cap: a host who asks for 100
   gets a smaller pool, and the fallback in rule 3 is the way out of an empty roster.
3. **One-step fallback.** A host may set a lower requirement that applies from N hours before
   kickoff (`fallback_min_reputation`, `fallback_hours_before_start`). It is evaluated when a
   player tries to join; nothing runs in the background. Hosts can also edit the requirement
   any time.
4. **The host verifies attendance**, after kickoff, within 7 days. Every mark records who made
   it (`marked_by`). The first mark sets the game to `played`. Unmarked games change nothing
   for anyone; a lazy host never costs a player.
5. **A player can dispute a mark once** within the same 7 days, with a short note. The host
   sees it and may flip the mark. After 7 days everything locks. (Columns exist; endpoint is
   sprint 2.)
6. **Leaving before kickoff is free.** Being on the roster at kickoff and absent is the only
   no-show.
7. **Spots exclude the host.** A 10-spot game has room for 10 players plus the host.
8. **Star ratings are separate.** Players rating hosts (sprint 2) and hosts rating players
   (sprint 3) go in a `ratings` table and show as their own number. They never change
   reputation, so the one number hosts trust stays a fact, not an opinion.

## What this answers

| Feedback question | Answer | When |
|---|---|---|
| How does someone with no history join a first game? | Rule 1, plus rules 2 and 3 | Sprint 1 |
| Who verifies attendance? | The host, named on every mark (rule 4) | Sprint 1 |
| How can users challenge an incorrect attendance report? | Dispute within the window (rule 5) | Sprint 2 |
| Host accountability and two-way reputation | Players rate hosts; a late cancel costs the host | Sprint 2 |
| Fake events or dishonest hosts | Report button on a game; host rating | Sprint 3 |
| Reminders | Epic E4 on the board, uses `updated_at` on games | Sprint 2 |
| Free app versus court fees | The app is free. `cost` on a game is the court or drop-in fee, shown before joining | Wording, now |

## Known limits, accepted for now

- A player can delete their account and return at 100. Email verification later makes this
  cost something; the "New" label is the only defence until then.
- A host can mark a no-show out of spite. The mark is attributed and disputable; host
  ratings give players a reply.
- Hosts have no reputation cost yet for cancelling late or not showing to their own game.
