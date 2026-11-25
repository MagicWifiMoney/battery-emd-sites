#!/usr/bin/env node
// PreToolUse guard for Bash. Turns the fleet's shipping rules into hard checks.
// A block never asks a human: each deny names the safe route, and Claude is
// expected to take that route on its own and carry on.
//   1. never skip git hooks (--no-verify, commit -n, core.hooksPath)
//   2. never force-push main/master (a lease on your own branch is fine)
//   3. production ships from git, never from the Vercel CLI
//      (vercel --prod, --target production, promote, rollback, redeploy)
//   4. `vercel env add` stores EMPTY on Jay's Mac: set env another way
//   5. every vercel command names the team scope
//   6. never overwrite .env.local (plain `vercel env pull` does exactly that)
//   7. no live-mode Stripe CLI calls: build and test in test mode
// Install: .claude/hooks/guard-bash.mjs, wired in .claude/settings.json under
// hooks.PreToolUse with matcher "Bash" and "onFailure": "block".
//
// This is a guardrail against honest mistakes, not a sandbox: quoted text and
// heredoc bodies are ignored on purpose, so commit messages and PR bodies that
// mention these commands are not blocked.

const VERCEL_SCOPE = process.env.CLAUDE_VERCEL_SCOPE || "giebz"; // {{VERCEL_SCOPE}}
const GO_ON = " Do that now without asking; this is the normal path here.";

// vercel subcommands that never touch a project, so no scope is needed
const SCOPE_FREE = new Set(["--version", "-v", "version", "help", "--help", "-h", "whoami", "login", "logout", "telemetry"]);
// vercel global flags that take a value, so the value is not the subcommand
const VALUE_FLAGS = new Set(["--scope", "-S", "--token", "-t", "--cwd", "--team", "-T", "--local-config", "-A", "--global-config", "-Q", "--target", "--env", "-e", "--build-env", "-b", "--meta", "-m"]);
const PROTECTED_BRANCH = /^(main|master)$/;

function deny(reason) {
  process.stdout.write(JSON.stringify({
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: reason,
    },
  }));
  process.exit(0);
}

const isEnvLocal = (p) => /^(\.\/)?\.env\.local$/.test(p ?? "");

// Drop heredoc bodies and the contents of quoted strings.
function stripQuoted(cmd) {
  const lines = cmd.split("\n");
  const kept = [];
  for (let i = 0; i < lines.length; i++) {
    kept.push(lines[i]);
    const m = lines[i].match(/<<-?\s*(['"]?)(\w+)\1/);
    if (m) {
      while (i + 1 < lines.length && lines[i + 1].trim() !== m[2]) i++;
      i++; // skip the terminator line too
    }
  }
  return kept.join("\n").replace(/'[^']*'/g, "''").replace(/"(\\.|[^"\\])*"/g, '""');
}

let raw = "";
process.stdin.on("data", (c) => (raw += c));
process.stdin.on("end", () => {
  let cmd = "";
  try {
    cmd = JSON.parse(raw)?.tool_input?.command ?? "";
  } catch {
    console.error("guard-bash: could not read hook input");
    process.exit(1); // a failure, so onFailure "block" refuses the call
  }
  if (!cmd) process.exit(0);

  // Check each part of a compound command on its own.
  const parts = stripQuoted(cmd).split(/&&|\|\||;|\||\n/).map((p) => p.trim().replace(/^[({\s]+/, "")).filter(Boolean);

  for (const part of parts) {
    // Skip leading env assignments and wrappers to find the real command.
    let words = part.split(/\s+/).map((w) => w.replace(/[)}]+$/, "")).filter(Boolean);
    while (words.length && (/^\w+=/.test(words[0]) || ["sudo", "env", "command", "exec", "time"].includes(words[0]))) words = words.slice(1);
    const cmd0 = words[0] ?? "";

    if (cmd0 === "git") {
      const subAt = words.findIndex((w, i) => i > 0 && !w.startsWith("-") && words[i - 1] !== "-c" && words[i - 1] !== "-C");
      const sub = subAt === -1 ? "" : words[subAt];

      // 1. git hooks are the deploy gate here
      if (words.includes("--no-verify") ||
          words.some((w, i) => words[i - 1] === "-c" && /^core\.hookspath=/i.test(w)) ||
          (sub === "commit" && words.some((w) => /^-[a-zA-Z]*n[a-zA-Z]*$/.test(w)))) {
        deny("Blocked: skipping git hooks (--no-verify, commit -n, core.hooksPath) skips the pre-push build and tests. Fix what the hook reports, commit the fix, and push again with hooks on." + GO_ON);
      }

      // 2. force-push: plain --force or -f anywhere; any force onto main/master
      if (sub === "push") {
        const rest = words.slice(subAt + 1);
        const plainForce = rest.some((w) => w === "--force" || /^-[a-zA-Z]*f[a-zA-Z]*$/.test(w));
        const lease = rest.some((w) => /^--force-with-lease/.test(w) || /^--force-if-includes/.test(w));
        const refs = rest.filter((w) => !w.startsWith("-"));
        const toProtected = refs.slice(1).some((r) => PROTECTED_BRANCH.test(r.replace(/^\+/, "").split(":").pop().replace(/^refs\/heads\//, "")));
        const plusRef = refs.slice(1).some((r) => r.startsWith("+"));
        if (plainForce || ((lease || plusRef) && toProtected) || (plusRef && !lease)) {
          deny("Blocked: no plain force-push, and no force onto main/master. On your own branch use `git push --force-with-lease`; to change main, push a new commit (or a revert) instead of rewriting it." + GO_ON);
        }
      }
    }

    // 6a. shell writes onto .env.local (redirects anywhere in the part; cp/mv/tee only as target)
    if (/>{1,2}\s*(\.\/)?\.env\.local(\s|$)/.test(part) ||
        (["cp", "mv"].includes(cmd0) && isEnvLocal(words[words.length - 1])) ||
        (cmd0 === "tee" && words.slice(1).some(isEnvLocal))) {
      deny("Blocked: never overwrite .env.local (some sensitive vars pull empty). Write to a new file such as .env.pulled.local and copy over only the lines you need." + GO_ON);
    }

    // 7. Stripe CLI in live mode
    if (cmd0 === "stripe" && (words.includes("--live") || words.some((w) => /sk_live_|rk_live_/.test(w)))) {
      deny("Blocked: no live-mode Stripe calls from here. Build and test the change in Stripe test mode (drop --live, use the test key). Then stop and list the exact live change (object, field, old value to new value) under \"Needs Jay: live Stripe\" in your final report; Jay approves those in one batch. Carry on with the rest of the task.");
    }

    // Find a vercel invocation: vercel, npx vercel[@x], pnpm dlx vercel, bunx vercel, yarn dlx vercel
    let vi = -1;
    if (/^vercel(@\S+)?$/.test(cmd0)) vi = 0;
    else if (["npx", "bunx"].includes(cmd0)) vi = words.findIndex((w, i) => i > 0 && /^vercel(@\S+)?$/.test(w));
    else if (["pnpm", "yarn"].includes(cmd0) && words[1] === "dlx") vi = words.findIndex((w, i) => i > 1 && /^vercel(@\S+)?$/.test(w));
    if (vi === -1) continue;
    const args = words.slice(vi + 1);

    // The subcommand is the first word that is neither a flag nor a flag's value.
    let sub = "", subAt = -1;
    for (let i = 0; i < args.length; i++) {
      const a = args[i];
      if (a.startsWith("-")) { if (VALUE_FLAGS.has(a)) i++; continue; }
      sub = a; subAt = i; break;
    }

    // 3. production from the CLI
    const targetProd = args.some((a, i) => a === "--prod" || a === "--production" || a === "--target=production" || (a === "--target" && args[i + 1] === "production"));
    if (["promote", "rollback", "redeploy"].includes(sub) || (targetProd && ["", "deploy", "build"].includes(sub))) {
      deny("Blocked: production ships from git here, never from the Vercel CLI (a stale checkout reverted prod twice). Commit and push through git the way this repo ships (your branch and its PR, or the repo's usual push to its default branch) and let Vercel's git deploy run. Then verify the deployed commit SHA with `vercel ls --scope " + VERCEL_SCOPE + "` and `vercel inspect`." + GO_ON);
    }

    // 4. `vercel env add` stores an empty value on Jay's Mac
    if (sub === "env" && args[subAt + 1] === "add") {
      deny("Blocked: `vercel env add` stores an EMPTY value on Jay's Mac. Set the variable with the Vercel MCP env tool or the Vercel REST API (POST /v10/projects/{id}/env), then `vercel env pull .env.pulled.local --scope " + VERCEL_SCOPE + "` and check the value's length, never print it. A new env var reaches prod with the next git deploy." + GO_ON);
    }

    // 6b. `vercel env pull` with no filename, or .env.local, overwrites it
    if (sub === "env" && args[subAt + 1] === "pull") {
      const rest = args.slice(subAt + 2);
      let file;
      for (let i = 0; i < rest.length; i++) {
        if (rest[i].startsWith("-")) { if (VALUE_FLAGS.has(rest[i]) || /^--(environment|git-branch)$/.test(rest[i])) i++; continue; }
        file = rest[i]; break;
      }
      if (!file || isEnvLocal(file)) {
        deny("Blocked: `vercel env pull` without a filename overwrites .env.local. Use `vercel env pull .env.pulled.local --scope " + VERCEL_SCOPE + "`." + GO_ON);
      }
    }

    // 5. scope on every project command
    if (SCOPE_FREE.has(sub || args[0] || "")) continue;
    const i = args.findIndex((a) => a === "--scope" || a === "-S" || a.startsWith("--scope="));
    const scope = i === -1 ? null : args[i].includes("=") ? args[i].split("=")[1] : args[i + 1];
    if (scope !== VERCEL_SCOPE) {
      deny(`Blocked: vercel commands here must use --scope ${VERCEL_SCOPE}${scope ? ` (got ${scope})` : ""}. Re-run the same command with --scope ${VERCEL_SCOPE}.` + GO_ON);
    }
  }
  process.exit(0); // no decision: normal permission rules apply
});
