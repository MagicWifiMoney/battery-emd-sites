#!/usr/bin/env node
// PreToolUse guard for MCP tools that touch production or money (Vercel, Stripe,
// Autumn billing). A block never asks a human: each deny names the safe route,
// and Claude is expected to take it on its own and carry on.
//
//   - Read-only tools (get_, list_, search_, ...) pass with no decision.
//   - Vercel deploy shortcuts (create a deployment, promote, roll back, move an
//     alias, rolling releases) are denied: production ships from git.
//   - Vercel steps that spend money or can't be undone (buy or transfer a
//     domain, delete or pause a project) are denied and listed for Jay.
//   - Other Vercel writes (env vars, domains config, DNS, flags, firewall,
//     routes) get no decision, so the normal permission rules apply.
//   - Stripe and Autumn writes are denied unless the MCP server is a test-mode
//     or sandbox one (its name contains "test" or "sandbox"). Build and test in
//     test mode; the live change is listed for Jay's one yes.
//
// Fail closed: wired with "onFailure": "block" in .claude/settings.json.
// If this script is missing, crashes, times out or can't read its input, the
// tool call is blocked instead of let through. That is why bad input exits 1.
//
// The settings matcher already skips read-only tool names, so reads never
// start this script. The same check runs here as a second line in case the
// matcher is widened later.

const GUARDED_SERVER = /vercel|stripe|autumn/i; // autumn: Sermon Clips billing API
const MONEY_SERVER = /stripe|autumn/i;
const TEST_SERVER = /test|sandbox/i;
const READ_ONLY = /^(get|list|search|retrieve|fetch|count|aggregate|filter|read|check|web_fetch|wait_for)_/;
// Names that look read-only but change something
const NOT_READ_ONLY = new Set(["get_access_to_vercel_url", "get_or_create_drive", "get_project_deletion_link"]);
const VERCEL_DEPLOY = /^(create_deployment|request_promote|request_rollback|assign_alias|start_rolling_release|approve_rolling_release_stage|complete_rolling_release)$/;
const VERCEL_HOLD = /^(buy_domain|create_or_transfer_domain|accept_project_transfer_request|delete_\w+|pause_project|get_project_deletion_link|create_ai_gateway_api_key|upsert_ai_gateway_budget\w*)$/;
const GO_ON = " Do that now without asking; this is the normal path here.";
const FOR_JAY = " Then stop and list the exact step (what, where, and why) under \"Needs Jay\" in your final report; Jay approves those in one batch. Carry on with the rest of the task.";

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

let raw = "";
process.stdin.on("data", (c) => (raw += c));
process.stdin.on("end", () => {
  let input;
  try {
    input = JSON.parse(raw);
  } catch {
    console.error("guard-mcp: could not read hook input");
    process.exit(1); // a failure, so onFailure "block" refuses the call
  }
  const name = String(input?.tool_name ?? "");
  const cut = name.lastIndexOf("__");
  if (!name.startsWith("mcp__") || cut < 5) process.exit(0); // not an MCP tool
  const server = `${input?.mcp_server?.name ?? ""} ${name.slice(5, cut)}`;
  const tool = name.slice(cut + 2);
  if (!GUARDED_SERVER.test(server)) process.exit(0);
  if (READ_ONLY.test(tool) && !NOT_READ_ONLY.has(tool)) process.exit(0);

  if (MONEY_SERVER.test(server)) {
    if (TEST_SERVER.test(server)) process.exit(0); // test-mode server: build freely
    deny(`Blocked: ${tool} would change live billing. Build and test it in Stripe test mode (a test-mode key, or a test or sandbox MCP server) and confirm it works there.` + FOR_JAY.replace("\"Needs Jay\"", "\"Needs Jay: live Stripe\"").replace("the exact step (what, where, and why)", "the exact live change (object, field, old value to new value)"));
  }

  // Vercel from here on
  if (VERCEL_DEPLOY.test(tool)) {
    deny(`Blocked: ${tool} deploys around git. Production ships from git here: commit and push through git the way this repo ships (your branch and its PR, or the repo's usual push to its default branch) and let Vercel's git deploy run. Then verify the deployed commit SHA.` + GO_ON);
  }
  if (VERCEL_HOLD.test(tool)) {
    deny(`Blocked: ${tool} spends money or can't be undone, so it waits for Jay.` + FOR_JAY);
  }
  process.exit(0); // other Vercel writes: no decision, normal permissions apply
});
