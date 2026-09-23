"""Render the review's editable DOT diagrams and self-contained HTML report.

Requirements: Python Markdown and Graphviz dot. Run from any directory.
"""
from __future__ import annotations

import html
import re
import subprocess
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent

GRAPHS = {
    '01-system-context': r'''
    rankdir=TB;
    person [label="Operator / researcher\nQuestion and configuration", fillcolor="#E6EEFF"];
    subgraph cluster_agent { label="Model-facing agent harness"; color="#ACC4E9";
      prompt [label="Phase prompts\nTask + file pointers + budget"];
      model [label="Language model\nProposes designs and conclusions", fillcolor="#DEF3F4"];
      loop [label="Python conversation loop\nDispatch, counters, events"];
      gate [label="Deterministic gates\nValidation and evidence checks", fillcolor="#FFF0D4"];
      workspace [label="Workspace\nRead / write / submit scopes"];
      prompt -> model; model -> loop [label="text and tool calls"];
      loop -> gate; gate -> workspace; workspace -> model [label="tool results"];
    }
    contracts [label="Catalog + environment\nHandbook + result contract", shape=folder];
    lifecycle [label="Optional lifecycle\nStart / stop / wait / resume", fillcolor="#EEE7FA"];
    backend [label="BeXhoma execution\nDatabases, loaders, benchmarkers", fillcolor="#E1F1E6"];
    cluster [label="Kubernetes cluster\nCompute, storage, monitoring", shape=component];
    artifacts [label="Results and investigation files\nEvidence, events, summaries, answer", shape=folder];
    person -> prompt; person -> lifecycle;
    lifecycle -> loop [label="invoke phase"];
    lifecycle -> model [label="manage bundled server", style=dashed];
    contracts -> workspace [label="bounded reads"];
    workspace -> backend [label="validated specification"];
    backend -> cluster; cluster -> artifacts [label="measurements"];
    backend -> artifacts [label="reports"];
    loop -> artifacts [label="trajectory + answer"];
    artifacts -> workspace [label="selected result"];
    ''',
    '02-event-graph': r'''
    start [label="Question accepted", shape=oval, fillcolor="#E6EEFF"];
    baseline [label="Optional baseline\nSeparate answer; failure is nonfatal"];
    design [label="Fresh design context\nRead contracts and handbook"];
    draft [label="Draft written"];
    valid [label="Validation passed?", shape=diamond, fillcolor="#FFF0D4"];
    repair [label="Validation error returned\nRepair while budget remains"];
    dry [label="Dry-run mode?", shape=diamond];
    proposal [label="Validated proposal\nPhase report + answer", shape=oval];
    submit [label="Fingerprint + lock\nReserve code; stage; detach child"];
    launch [label="Result directory observed?", shape=diamond];
    starting [label="Child alive after 120 s\nReturn code, state starting"];
    running [label="Return code, state running\nArchive staged inputs"];
    dead [label="Child exited\nSubmission failed", fillcolor="#FBE6E4"];
    wait [label="Lifecycle turns bundled model OFF\nWait for exact experiment report"];
    ready [label="Report exists?", shape=diamond];
    failed [label="Definitive failure\nStop exact experiment", fillcolor="#FBE6E4"];
    interpret [label="Model ON; fresh evidence context\nRead validity and evidence"];
    record [label="Structured record accepted?", shape=diamond, fillcolor="#FFF0D4"];
    revise [label="Return record errors\nContinue within turn limit"];
    summary [label="Write portable result summary\nProduce interpretation prose"];
    follow [label="Follow-up requested\nand budget remains?", shape=diamond];
    author [label="Fresh authoring context\nRead design inputs; lineage + change checks"];
    done [label="Complete without new code\nWrite answer; model OFF", shape=oval, fillcolor="#E1F1E6"];
    incomplete [label="Incomplete phase / error\nPreserve available state; model OFF", fillcolor="#FBE6E4"];
    start -> baseline -> design -> draft -> valid;
    valid -> repair [label="no"]; repair -> draft [label="attempt remains"];
    repair -> incomplete [label="budget spent"];
    valid -> dry [label="yes"]; dry -> proposal [label="yes: intended route"];
    dry -> submit [label="no"]; submit -> launch;
    launch -> running [label="yes"]; launch -> starting [label="not yet, child alive"];
    launch -> dead [label="no, child exited"]; dead -> incomplete;
    running -> wait; starting -> wait; wait -> ready;
    ready -> wait [label="not yet, alive"]; ready -> failed [label="failed/dead"];
    failed -> incomplete; ready -> interpret [label="yes"];
    interpret -> record; record -> revise [label="no"]; revise -> record [label="retry"];
    revise -> incomplete [label="turns exhausted"];
    record -> summary [label="yes"]; summary -> follow;
    follow -> done [label="no"]; follow -> author [label="yes"];
    author -> submit [label="validated follow-up"];
    author -> incomplete [label="authoring fails"];
    author -> done [label="dry-run follow-up valid"];
    ''',
    '03-tool-sequence': r'''
    rankdir=TB;
    p1 [label="1  CLI → harness\nCreate phase, metadata, fresh messages", fillcolor="#E6EEFF"];
    p2 [label="2  Harness → model endpoint\nMessages + advertised tool schemas", fillcolor="#DEF3F4"];
    p3 [label="3  Model → harness\nread_file requests"];
    p4 [label="4  Harness → workspace → model\nCanonicalize, authorize, return bounded text"];
    p5 [label="5  Model → harness\nwrite_file with full YAML"];
    p6 [label="6  Design gate → workspace\nCheck required reads, write draft", fillcolor="#FFF0D4"];
    p7 [label="7  Model → validator\nvalidate(path)"];
    p8 [label="8  Validator → model\nVerdict, errors, resource cells, cost estimate", fillcolor="#FFF0D4"];
    p9 [label="9  Model → submit\nExact approved path"];
    p10 [label="10  Submit → detached child\nReserve code; snapshot; Popen", fillcolor="#E1F1E6"];
    p11 [label="11  Submit → model\nCode + running/starting state"];
    p12 [label="12  Harness → files\nOutcome and phase account; CLI exits", shape=folder];
    execution [label="Child → BeXhoma → Kubernetes\nBenchmark continues independently", fillcolor="#E1F1E6"];
    events [label="Trajectory side channel\nEvery assistant reply and tool result", shape=folder];
    p1 -> p2 -> p3 -> p4 -> p5 -> p6 -> p7 -> p8 -> p9 -> p10 -> p11 -> p12;
    p8 -> p5 [label="rejected: bounded repair", style=dashed];
    p10 -> execution [label="detached"];
    p4 -> events [style=dashed]; p8 -> events [style=dashed]; p11 -> events [style=dashed];
    ''',
    '04-state-graph': r'''
    subgraph cluster_experiment { label="Experiment status file and observed artifacts"; color="#A5C4B0";
      reserved [label="reserved\nExclusive status-file creation"];
      starting [label="starting\nChild launched; result folder pending"];
      running [label="running\nResult directory available"];
      finished [label="finished\nreport/index.md exists", fillcolor="#E1F1E6"];
      failed [label="failed\nStored failure or dead child before report", fillcolor="#FBE6E4"];
      reserved -> starting [label="launch succeeds"];
      starting -> running [label="directory observed"];
      starting -> finished [label="later discovery"];
      running -> finished [label="report observed"];
      starting -> failed; running -> failed;
    }
    subgraph cluster_investigation { label="Investigation progression (derived, not status enums)"; color="#ACC4E9";
      d [label="Design invocation"];
      w [label="Waiting for submitted experiment"];
      i [label="Interpretation invocation"];
      f [label="Follow-up authoring context"];
      a [label="Complete; answer.md exists", shape=oval, fillcolor="#E1F1E6"];
      x [label="Incomplete / aborted\nMay require operator recovery", fillcolor="#FBE6E4"];
      d -> w [label="code in outcome"];
      w -> i [label="selected report exists"];
      i -> f [label="decision + remaining budget"];
      f -> w [label="new submitted code"];
      i -> a [label="complete, no new code"];
      d -> a [label="successful dry run"];
      d -> x; i -> x; f -> x;
    }
    finished -> i [style=dashed, label="permits interpretation"];
    failed -> x [style=dashed];
    note [label="Technical completion ≠ scientific support\nVerdict is supported / refuted / inconclusive / invalid", shape=note];
    a -> note [style=dashed];
    ''',
    '05-entity-relationship': r'''
    rankdir=TB;
    node [shape=record, style=filled, fillcolor="#F2F6FD"];
    inv [label="{INVESTIGATION|directory ID\loriginal task\lanswer path\l}"];
    phase [label="{PHASE INVOCATION|phase number + kind\lmodel + parameters\lharness hash\loutcome + budget\l}"];
    context [label="{MODEL CONTEXT|design / evidence / follow-up / baseline\lmessages and local read budget\l}"];
    event [label="{TRAJECTORY EVENT|timestamp + type\lphase / stage / turn\lassistant or tool payload\l}"];
    draft [label="{DRAFT SPECIFICATION|inbox path\lmutable full YAML\l}"];
    approval [label="{VALIDATION APPROVAL|spec + catalog + environment hashes\lin-memory workspace state\l}"];
    exp [label="{EXPERIMENT|numeric code\lsubmitted specification\loptional parent code\l}", fillcolor="#E1F1E6"];
    status [label="{STATUS RECORD|code / state / PID\lpaths / provenance references\l}"];
    input [label="{INPUT SNAPSHOT|experiment / catalog / environment\lresult contract if present\l}"];
    result [label="{RESULT DIRECTORY|experiment code\lraw artifacts\l}"];
    page [label="{REPORT PAGE|relative path\lfrontmatter / sections / tables\l}"];
    summary [label="{AGENT SUMMARY|scientific verdict\ltechnical scope\lrelative evidence paths\lunresolved question\l}"];
    account [label="{PHASE REPORT|prose account\lreasoning trace\l}"];
    inv -> phase [label="1 : 1..* contains"];
    phase -> context [label="1 : 1..2 normally"];
    inv -> event [label="1 : 0..* appends"];
    context -> event [label="1 : 0..* emits"];
    context -> draft [label="authors 0..* revisions"];
    draft -> approval [label="1 : 0..1 current approval"];
    phase -> exp [label="1 : 0..1 normal submission"];
    approval -> exp [label="exact hashes required"];
    exp -> exp [label="0..1 parent; 0..* children", color="#8864AB"];
    exp -> status [label="1 : 1"];
    exp -> input [label="1 : 1 set"];
    exp -> result [label="1 : 0..1"];
    result -> page [label="1 : 0..* pages"];
    result -> summary [label="1 : 0..1 current summary"];
    phase -> account [label="1 : 0..1 pair"];
    phase -> result [label="interpret 0..1 exact result", style=dashed];
    inv -> inv [label="0..1 linked baseline", style=dashed];
    ''',
    '06-context-memory': r'''
    rankdir=TB;
    task [label="Original question", fillcolor="#E6EEFF"];
    design [label="CONTEXT A\nInitial design\nDrafts + feedback stay here", fillcolor="#DEF3F4"];
    executed [label="Executed specification\nExact experiment code", shape=folder];
    evidence [label="CONTEXT B\nOne-result evidence interpretation", fillcolor="#DEF3F4"];
    author [label="CONTEXT C\nFollow-up authoring", fillcolor="#DEF3F4"];
    next [label="NEXT INVOCATION\nFresh interpretation for new code", fillcolor="#DEF3F4"];
    docs [label="Catalog + environment\nHandbook guidance", shape=folder];
    result [label="Selected report + contract\nLink-reachable local evidence", shape=folder];
    compact [label="Ancestor agent_summary.yml records\nOldest first; no ancestor metrics", shape=folder];
    log [label="Trajectory audit history\nRetained on disk, not replayed wholesale", shape=folder];
    old [label="Other result directories\nInside configured result root", fillcolor="#FBE6E4"];
    task -> design; task -> evidence; task -> author;
    docs -> design [label="must read before write"];
    design -> executed [label="accepted submission"];
    executed -> evidence;
    result -> evidence [label="read whitelist"];
    evidence -> author [label="interpretation + decision + parent spec"];
    compact -> author [label="compact history"];
    docs -> author [label="reread"];
    author -> next [label="new submitted experiment"];
    design -> log [style=dashed]; evidence -> log [style=dashed]; author -> log [style=dashed];
    old -> design [label="current code permits reads", style=dashed, color="#BD473F", fontcolor="#BD473F"];
    old -> author [label="restored design scope", style=dashed, color="#BD473F", fontcolor="#BD473F"];
    ''',
    '07-validation': r'''
    spec [label="Draft YAML + catalog"];
    parse [label="Read and parse", fillcolor="#FFF0D4"];
    shape [label="Schema and nested shape\nAllowed fields and factor declarations", fillcolor="#FFF0D4"];
    resolver [label="Shared catalog resolution\nBuild executable arguments", fillcolor="#FFF0D4"];
    method [label="Method checks\nHypothesis heuristic; fixed envelope\nAttribution; repetition minimum", fillcolor="#FFF0D4"];
    exists [label="Environment exists?", shape=diamond];
    fit [label="Storage + resources + placement\nPinned benchmarker peak limits", fillcolor="#FFF0D4"];
    weak [label="valid = true\nenvironment_checked = false\nNo submission approval", fillcolor="#FBE6E4"];
    strong [label="valid = true\nenvironment_checked = true", fillcolor="#E1F1E6"];
    hash [label="Store draft + catalog + environment hashes\nRecheck at submit"];
    errors [label="Structured errors\nParse / catalog / method / environment\nReturn to model for bounded repair", fillcolor="#FBE6E4"];
    estimates [label="Estimates\nSystems × resource cells × rounds × repetitions\nDeclared timeout budget; not runtime forecast", shape=note];
    spec -> parse -> shape -> resolver -> method -> exists;
    parse -> errors [label="bad YAML"]; shape -> errors [label="invalid structure"];
    resolver -> errors [label="unsupported / invalid"];
    method -> errors [label="method defects"];
    exists -> weak [label="no"]; exists -> fit [label="yes"];
    fit -> errors [label="does not fit"]; fit -> strong [label="fits"];
    strong -> hash; resolver -> estimates [style=dashed]; estimates -> strong [style=dashed];
    ''',
    '08-interpretation': r'''
    index [label="Selected report/index.md\nTests + frontmatter failed count", shape=folder];
    contract [label="Archived result contract\nOr repository fallback", shape=folder];
    method [label="Required existing handbook chapters", shape=folder];
    reads [label="Read tracking\nPath access and required sections", fillcolor="#FFF0D4"];
    benchmark [label="benchmarking.md + archived spec\nOptional monitoring evidence", shape=folder];
    assessor [label="Deterministic assessor\nCoverage, anomalies, trend/ranking, validity scope", fillcolor="#FFF0D4"];
    record [label="Model record\nHypothesis verdict + validity + questions\nQuality + typed claims + follow-up", fillcolor="#DEF3F4"];
    check [label="Exact field and citation checks", shape=diamond, fillcolor="#FFF0D4"];
    error [label="Errors returned\nRetry within 26-turn evidence ceiling"];
    summary [label="agent_summary.yml\nPortable one-result verdict", shape=folder];
    prose [label="Closing natural-language account\nRequested answer-contract structure", fillcolor="#DEF3F4"];
    decision [label="Finish or enter fresh follow-up authoring"];
    gap [label="Gap: a read path is not semantic support\nFinal prose can contradict accepted record", shape=note, fillcolor="#FBE6E4"];
    index -> reads; contract -> reads; method -> reads;
    benchmark -> assessor;
    reads -> record; assessor -> record; record -> check;
    check -> error [label="rejected"]; error -> record;
    check -> summary [label="accepted"]; check -> prose [label="tools withdrawn"];
    prose -> decision; summary -> decision;
    prose -> gap [style=dashed, color="#BD473F"]; record -> gap [style=dashed, color="#BD473F"];
    ''',
    '09-followup': r'''
    decision [label="Accepted follow_up decision"];
    action [label="action = followup?", shape=diamond];
    budget [label="Remaining budget > 0?", shape=diamond];
    finish [label="Finish current result\nUnexecuted proposal may be described", shape=oval, fillcolor="#E1F1E6"];
    context [label="Fresh authoring\nTask + interpretation + decision\nParent spec + ancestor summaries", fillcolor="#DEF3F4"];
    docs [label="Reread design inputs\nWrite new draft"];
    lineage [label="Exact parent code?\nExecution settings changed?\nApproved query subset matched?", shape=diamond, fillcolor="#FFF0D4"];
    valid [label="Shared validation passes?", shape=diamond, fillcolor="#FFF0D4"];
    repair [label="Return errors and repair\nWithin authoring attempts"];
    submit [label="Submit new experiment\nDecrease budget by successful submissions", fillcolor="#E1F1E6"];
    incomplete [label="No successful follow-up\nIncomplete authoring phase", fillcolor="#FBE6E4"];
    next [label="Wait and interpret new experiment\nSame investigation, new result evidence"];
    decision -> action;
    action -> finish [label="no"]; action -> budget [label="yes"];
    budget -> finish [label="no"]; budget -> context [label="yes"];
    context -> docs -> lineage;
    lineage -> repair [label="no"]; lineage -> valid [label="yes"];
    valid -> repair [label="no"]; repair -> docs [label="budget remains"];
    repair -> incomplete [label="spent"];
    valid -> submit [label="yes, live mode"];
    valid -> finish [label="yes, dry run"];
    submit -> next -> decision;
    ''',
    '10-deployment': r'''
    rankdir=TB;
    laptop [label="Local operator\nLifecycle + local subprocesses", fillcolor="#E6EEFF"];
    controller [label="Alternative: Kubernetes controller Job\nService account + durable state\nTemplate image/namespace require deployment values", fillcolor="#EEE7FA"];
    harness [label="Harness phase CLI\nDesign / interpret / baseline"];
    switch [label="Bundled server switch\nModel ON for reasoning\nModel OFF while waiting for benchmark", fillcolor="#EEE7FA"];
    external [label="External model endpoint\nAlready running; no switching", fillcolor="#DEF3F4"];
    service [label="bexhoma-agent-model Service\nShared name within namespace"];
    gpu [label="Qwen vLLM Pod\n1 H100/H200-compatible GPU\nExcludes benchmark node", fillcolor="#DEF3F4"];
    weights [label="150 GiB persistent weights volume\nRetained across shutdown", shape=cylinder];
    watchdog [label="Idle watchdog\n60 s polls; 1200 s idle threshold"];
    executor [label="Detached BeXhoma process", fillcolor="#E1F1E6"];
    sut [label="Kubernetes workloads\nSUT + loader + benchmarker\nDashboard, queue, monitoring", fillcolor="#E1F1E6"];
    state [label="Persistent investigation state\nStatus, snapshots, events, results", shape=cylinder];
    laptop -> harness; controller -> harness;
    laptop -> switch; controller -> switch;
    harness -> service [label="bundled API"]; harness -> external [label="external API"];
    switch -> gpu [label="create/delete"]; service -> gpu;
    weights -> gpu [label="load checkpoint"]; watchdog -> gpu [label="stop on idle"];
    harness -> executor [label="submit"]; executor -> sut;
    sut -> state [label="evidence / report"]; harness -> state [label="events / snapshots"];
    state -> controller [label="restart reconciliation", style=dashed];
    ''',
    '11-provenance': r'''
    rankdir=TB;
    live [label="Live draft + catalog + environment", shape=folder];
    approved [label="Approval fingerprint\nSHA-256 of validation inputs", fillcolor="#FFF0D4"];
    staged [label="Phase snapshots\nSubmitted experiment, catalog\nEnvironment + result contract", shape=folder];
    child [label="Detached execution child", fillcolor="#E1F1E6"];
    status [label="Status record\nExact code, PID, paths, provenance", shape=folder];
    raw [label="Result directory\nRaw logs, metrics, manifests", shape=folder];
    archived [label="Archived input files\nCopied into result directory", shape=folder];
    report [label="Tiered report\nIndex + five evidence pages", shape=folder];
    interpretation [label="Accepted interpretation\nAgent summary + answer", fillcolor="#DEF3F4"];
    trajectory [label="Trajectory\nMetadata hashes + outcomes + events\nRead text omitted from tool logs", shape=folder];
    live -> approved [label="validate"]; approved -> staged [label="submit rechecks hashes"];
    staged -> child [label="specification"];
    live -> child [label="initial launch reloads live catalog", style=dashed, color="#BD473F", fontcolor="#BD473F"];
    staged -> status; child -> status [label="PID / state"];
    child -> raw; staged -> archived [label="copy when directory exists"];
    raw -> report; archived -> interpretation; report -> interpretation;
    approved -> trajectory [style=dashed]; status -> trajectory [style=dashed];
    interpretation -> trajectory [style=dashed];
    ''',
    '12-failure-recovery': r'''
    rankdir=LR;
    fail [label="Failure or interruption", shape=oval, fillcolor="#FBE6E4"];
    model [label="Model exchange"];
    validation [label="Draft / structured record rejected"];
    launch [label="Execution / lifecycle"];
    crash [label="Process or controller crash"];
    retry [label="Rate limit / server failure\nUp to 6 outer attempts + backoff"];
    context [label="Context overflow\nResize once if limit is known\nOtherwise abort phase"];
    stall [label="Reasoning-only reply\nBounded action nudges"];
    repair [label="Feedback to model\nAttempt / turn ceiling"];
    start [label="Slow start, child alive\nKeep durable code; state starting"];
    dead [label="Dead child / failed status\nStop exact benchmark resources"];
    timeout [label="Configured wait timeout\nRaise; benchmark not necessarily stopped"];
    resume [label="Recover durable submission\nRelaunch orchestration from snapshots"];
    gap [label="Gaps\nPartial log tail; newest follow-up reconciliation\nPID identity across hosts/Pods", fillcolor="#FBE6E4"];
    cleanup [label="Lifecycle finally\nAttempt bundled model shutdown", fillcolor="#EEE7FA"];
    fail -> model; fail -> validation; fail -> launch; fail -> crash;
    model -> retry; model -> context; model -> stall;
    validation -> repair;
    launch -> start; launch -> dead; launch -> timeout;
    crash -> resume; crash -> gap;
    context -> cleanup; dead -> cleanup; timeout -> cleanup;
    repair -> cleanup [label="cannot complete"];
    ''',
    '13-model-dependence': r'''
    generic [label="Generic experiment orchestration\nContracts, validator, evidence gate\nFile state and bounded tool loop", fillcolor="#E1F1E6"];
    api [label="Chat API compatibility\nTool calls, reasoning fields\nWindow discovery and retries"];
    qwen [label="Qwen-specific bundled serving\nCheckpoint + reasoning/tool parsers\nFP8 + GPU + context settings", fillcolor="#DEF3F4"];
    policy [label="Global inference policies\nTemperature 0; reasoning discarded\n16,384 generated-token ceiling", fillcolor="#FFF0D4"];
    history [label="Observed development history\nInitial Qwen deployment\nLater Mistral / Ollama adaptations"];
    training [label="Project-specific weight training\nNo evidence in reviewed repository", shape=note];
    evaluate [label="RECOMMENDED controlled evaluation\nFrozen harness + held-out questions\nFixed evidence + live subset", fillcolor="#EEE7FA"];
    metrics [label="Measure\nDesign validity + answer correctness\nUnsupported claims + cost + variance"];
    judgment [label="Only then assess\nModel dependence or over-adaptation", shape=oval];
    generic -> api; api -> qwen; api -> policy; history -> generic;
    qwen -> training [style=dashed, label="serving is not training"];
    generic -> evaluate [style=dashed]; qwen -> evaluate [style=dashed];
    policy -> evaluate [style=dashed]; evaluate -> metrics -> judgment;
    ''',
}

BASE = '''digraph G {
graph [bgcolor="transparent", pad="0.25", nodesep="0.38", ranksep="0.48", fontname="Helvetica", fontsize=13, compound=true];
node [shape=box, style="rounded,filled", fillcolor="#F2F6FD", color="#8196B4", fontcolor="#172B49", fontname="Helvetica", fontsize=12, margin="0.16,0.11", penwidth=1.1];
edge [color="#647A99", fontcolor="#415674", fontname="Helvetica", fontsize=10, arrowsize=0.7];
'''

CSS = '''
:root {--ink:#192c49;--muted:#566880;--blue:#326ce5;--border:#dce4ef;--paper:#fff;--bg:#f3f6fb}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:24px}body{margin:0;color:var(--ink);background:var(--bg);font:16px/1.72 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
aside{position:fixed;inset:0 auto 0 0;width:285px;padding:26px 24px;overflow:auto;background:#162842;color:#dce7f8}aside .brand{font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:#8eafe8}aside strong{display:block;font-size:22px;line-height:1.3;margin:10px 0 20px}aside a{color:#c7d7ef;text-decoration:none}aside a:hover{color:white}aside ul{padding-left:16px;margin:8px 0}aside li{font-size:12px;line-height:1.5;margin:7px 0}aside>.toc>ul{padding-left:0;list-style:none}aside>.toc>ul>li>ul{padding-left:0;list-style:none}aside>.toc>ul>li>a{display:none}aside li li ul{display:none}
main{max-width:1220px;margin:0 0 0 285px;padding:56px 64px 100px;background:var(--paper);min-height:100vh}h1{font-size:43px;line-height:1.14;letter-spacing:-.04em;margin:0 0 20px;color:#152843}h2{font-size:27px;line-height:1.3;border-top:1px solid var(--border);padding-top:34px;margin-top:54px;letter-spacing:-.02em}h3{font-size:21px;line-height:1.4;margin-top:35px}p{margin:17px 0}a{color:#245dc6;text-decoration-thickness:1px;text-underline-offset:3px}code{font-size:.86em;background:#eef3f9;border-radius:4px;padding:2px 5px;overflow-wrap:anywhere}pre{background:#13243b;color:#e1eaf8;padding:24px;overflow:auto;border-radius:8px;font-size:13px;line-height:1.6}pre code{background:none;padding:0;color:inherit}table{border-collapse:collapse;width:100%;font-size:13px;line-height:1.6;margin:24px 0}th{text-align:left;background:#edf3fc;color:#1d3f73}td,th{padding:12px 14px;border:1px solid var(--border);vertical-align:top}tr:nth-child(even) td{background:#fafcff}td a{overflow-wrap:anywhere}li{margin:8px 0}blockquote{border-left:4px solid var(--blue);margin:24px 0;padding:4px 20px;background:#f2f6fc}.diagram{border:1px solid var(--border);border-radius:10px;margin:24px 0;background:#fbfcff;overflow:hidden}.diagram-tools{display:flex;gap:10px;align-items:center;padding:10px 16px;border-bottom:1px solid var(--border);background:#edf3fc}.diagram-tools span{font-size:12px;color:var(--muted);flex:1}button{border:1px solid #bccde6;border-radius:5px;background:white;color:#234b83;padding:6px 12px;cursor:pointer;font:inherit;font-size:12px}button:hover{background:#e1edff}.svg-wrap{padding:16px;overflow:auto;max-height:1000px}.svg-wrap svg{display:block;width:100%;height:auto;min-width:620px}.artifact-note{font-size:12px;color:#6d7c91;margin:30px 0}.print-button{margin:16px 0;background:#edf3ff}
dialog{width:96vw;max-width:none;height:94vh;max-height:none;border:0;border-radius:12px;padding:0;color:var(--ink)}dialog::backdrop{background:rgba(11,24,42,.72)}dialog .toolbar{height:60px;display:flex;align-items:center;gap:12px;background:#edf3fc;padding:12px 20px}dialog .toolbar strong{flex:1}#zoomview{height:calc(94vh - 60px);overflow:auto;padding:24px;background:white}#zoomview svg{display:block;height:auto;max-width:none}
@media(min-width:1600px){main{margin-left:calc(285px + (100vw - 1600px)/2)}}@media(max-width:1000px){aside{position:static;width:100%;max-height:260px}aside .toc{display:none}main{margin:0;padding:36px 24px}h1{font-size:34px}table{font-size:12px}td,th{padding:8px}}@media print{aside,.diagram-tools,.print-button{display:none}body,main{background:white}main{margin:0;padding:0;max-width:none}h1{font-size:28px}h2{break-before:auto}h2,h3{break-after:avoid}body{font-size:10pt}table{font-size:8pt}tr{break-inside:avoid}a{color:inherit}.diagram{break-inside:avoid}.svg-wrap{max-height:none}.svg-wrap svg{min-width:0;max-height:220mm}pre{white-space:pre-wrap;font-size:8pt}dialog{display:none}}
'''

JS = '''
const dialog=document.getElementById('graphdialog'),view=document.getElementById('zoomview');let baseWidth=1000,zoom=1;
document.querySelectorAll('.enlarge').forEach(b=>b.addEventListener('click',()=>{const source=b.closest('.diagram').querySelector('svg');view.replaceChildren(source.cloneNode(true));document.getElementById('graphtitle').textContent=b.dataset.title;const svg=view.querySelector('svg');baseWidth=svg.viewBox.baseVal.width;zoom=Math.min(1.4,(window.innerWidth*.9)/baseWidth);resize();dialog.showModal();}));
function resize(){const svg=view.querySelector('svg');if(svg)svg.style.width=(baseWidth*zoom)+'px';document.getElementById('zoomvalue').textContent=Math.round(zoom*100)+'%';}
document.getElementById('zoomin').onclick=()=>{zoom=Math.min(zoom*1.25,5);resize()};document.getElementById('zoomout').onclick=()=>{zoom=Math.max(zoom/1.25,.15);resize()};document.getElementById('zoomfit').onclick=()=>{zoom=(view.clientWidth-48)/baseWidth;resize()};document.getElementById('closegraph').onclick=()=>dialog.close();dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close()});
'''


def main() -> None:
    """Render all graphs and embed them in an offline report."""
    diagrams = ROOT / 'diagrams'
    diagrams.mkdir(exist_ok=True)
    for name, body in GRAPHS.items():
        source = diagrams / f'{name}.dot'
        source.write_text(BASE + body + '\n}\n')
        subprocess.run(['dot', '-Tsvg', str(source), '-o', str(source.with_suffix('.svg'))], check=True)
    renderer = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc'], extension_configs={'toc': {'toc_depth': '1-3'}})
    content = renderer.convert((ROOT / 'report.md').read_text())

    def embed(match: re.Match[str]) -> str:
        title, name = html.unescape(match[1]), match[2]
        svg = (ROOT / name).read_text()
        svg = svg[svg.index('<svg'):]
        # Prefix every SVG ID because Graphviz reuses node/edge IDs per graph.
        prefix = Path(name).stem
        svg = re.sub(r'id="([^"]+)"', lambda item: f'id="{prefix}-{item[1]}"', svg)
        svg = svg.replace('<svg ', f'<svg role="img" aria-label="{html.escape(title, quote=True)}" ', 1)
        return ('<figure class="diagram"><div class="diagram-tools"><span>'
                + html.escape(title) + '</span><button class="enlarge" data-title="'
                + html.escape(title, quote=True) + '">Enlarge</button></div><div class="svg-wrap">'
                + svg + '</div></figure>')

    content = re.sub(r'<p><img alt="([^"]*)" src="(diagrams/[^"]+\.svg)"\s*/></p>', embed, content)
    assert content.count('class="diagram"') == len(GRAPHS), 'Every diagram must be embedded'
    page = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>How the BeXhoma agent works — implementation review</title><style>' + CSS + '</style></head><body>'
            '<aside><div class="brand">BeXhoma · Implementation review</div><strong>How our agent works</strong>'
            '<p style="font-size:12px;color:#93afd7">v0.10.13 · 21 September 2026<br>13 diagrams · source-linked findings</p>'
            + renderer.toc + '</aside><main><button class="print-button" onclick="window.print()">Print report</button>'
            + content + '<p class="artifact-note">Reviewed implementation: 66a67a58 · Offline diagrams embedded · No live benchmark was launched for this review.</p></main>'
            '<dialog id="graphdialog"><div class="toolbar"><strong id="graphtitle">Diagram</strong>'
            '<button id="zoomout" aria-label="Zoom out">−</button><span id="zoomvalue"></span><button id="zoomin" aria-label="Zoom in">+</button>'
            '<button id="zoomfit">Fit width</button><button id="closegraph">Close</button></div><div id="zoomview"></div></dialog>'
            '<script>' + JS + '</script></body></html>')
    (ROOT / 'report.html').write_text(page)
    print(f'Rendered {len(GRAPHS)} diagrams; report.html is {len(page):,} characters.')


if __name__ == '__main__':
    main()
