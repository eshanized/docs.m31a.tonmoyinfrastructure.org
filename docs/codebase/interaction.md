# Interaction & Slash Commands

> **Architectural Layer:** L9 Interaction  
> **Source Directory:** `src/interaction`  
> **File Count:** 13 source files  

Session parser, user-defined slash commands, approval actions, and mention resolution.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [action.rs](#src-interaction-action-rs) | 253 | `ApplicationAction, InteractionIntent` | Strongly typed UI and Application Actions for developer interaction (P... |
| [approval.rs](#src-interaction-approval-rs) | 173 | `InteractiveApprovalChannel, PendingApprovalPrompt` | Interactive CLI Approval Channel and Coordinator Bridge (POL-01, D-09,... |
| [commands.rs](#src-interaction-commands-rs) | 2684 | `AnswerCommandHandler, AuthorizeCommandHandler, CancelHandler` | Centralized Slash Command Subsystem and Command Registry (PRD §01, CLI... |
| [continuation.rs](#src-interaction-continuation-rs) | 2614 | `ActiveExecution` | runtime-layer conversational execution for submitted user text.  this ... |
| [decision.rs](#src-interaction-decision-rs) | 817 | `DecisionOption, DecisionWaiterRegistry, InteractiveDecision` | Strongly typed interactive decision model for user choices and workflo... |
| [events.rs](#src-interaction-events-rs) | 1007 | `QuarantineItemRecord, EventDeliveryClass, InteractionEvent` | User-facing event stream abstraction decoupling CLI/TUI from internal ... |
| [mentions.rs](#src-interaction-mentions-rs) | 650 | `LineRange, MentionParser, MentionReference` | Developer-oriented @mention parsing, path resolution, and context inje... |
| [mod.rs](#src-interaction-mod-rs) | 53 | `Functions/Traits` | Developer Interaction Layer &amp; Agentic Interaction Protocol (PRD §0... |
| [parser.rs](#src-interaction-parser-rs) | 368 | `InteractionParser` | Interaction Input Parser and Deterministic Intent Classifier (PRD §01,... |
| [runner.rs](#src-interaction-runner-rs) | 2613 | `InteractiveSessionRunner` | Interactive CLI Session Runner and Terminal REPL Loop (PRD §01, CLI-01... |
| [session.rs](#src-interaction-session-rs) | 1017 | `Session, SqliteSessionRepository, ConversationTurn` | Durable interactive coding session aggregate and repository (PRD §01, ... |
| [state.rs](#src-interaction-state-rs) | 160 | `StateTransitionError, SessionPromptState` | Interactive prompt and session lifecycle state machine (PRD §01, CLI-0... |
| [user_commands.rs](#src-interaction-user_commands-rs) | 1972 | `BoundArguments, CapabilitiesSection, CommandSection` | Global User-Defined Slash Commands.  Lets an individual M31A user defi... |

---

### `src/interaction/action.rs` {#src-interaction-action-rs}

- **Source Link:** [`src/interaction/action.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/interaction/action.rs)
- **Lines of Code:** 253 (9227 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate | 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Strongly typed UI and Application Actions for developer interaction (PRD §01, CLI-01, CLI-04).  "Input -&gt; Interaction Parser -&gt; Typed Application Action -&gt; Application Command -&gt; Runtime -&gt; Events / State -&gt; CLI/TUI projection."

#### Types & Trait Declarations
- **Enums (2):** `ApplicationAction`, `InteractionIntent`

---

### `src/interaction/approval.rs` {#src-interaction-approval-rs}

- **Source Link:** [`src/interaction/approval.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/interaction/approval.rs)
- **Lines of Code:** 173 (5941 bytes)

#### Primary Responsibility
Interactive CLI Approval Channel and Coordinator Bridge (POL-01, D-09, D-11, CLI-01).  "When policy produces ASK, the interactive CLI MUST remain alive." "The answer must reach the authoritative runtime. Support: approve, deny, cancel."

#### Types & Trait Declarations
- **Structs (2):** `InteractiveApprovalChannel`, `PendingApprovalPrompt`

#### Key Functions & Signatures (8 shown)
```rust
// private
fn default() -> Self;
// pub
fn new() -> Self;
// pub
fn with_listener(mut self,
        listener: Arc<dyn Fn(PendingApprovalPrompt);
// pub
async fn current_pending_prompt(&self) -> Option<PendingApprovalPrompt>;
// pub
async fn submit_decision(&self,
        id: ApprovalRequestId,
        action: ApprovalAction,) -> Result<(), ApprovalEr;
// private
async fn notify_request(&self,
        packet: &ApprovalExplanationPacket,) -> Result<(), ApprovalError>;
// private
async fn poll_response(&self,
        id: ApprovalRequestId,) -> Result<Option<ApprovalAction>, ApprovalError>;
// private
async fn test_interactive_approval_channel_notify_and_resolve();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_interactive_approval_channel_notify_and_resolve`

---

### `src/interaction/commands.rs` {#src-interaction-commands-rs}

- **Source Link:** [`src/interaction/commands.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/interaction/commands.rs)
- **Lines of Code:** 2684 (99112 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence | 🛡️ Enforces Policy Gate

#### Primary Responsibility
Centralized Slash Command Subsystem and Command Registry (PRD §01, CLI-01).  "Do NOT use scattered match statements throughout the CLI/TUI. Create a typed command abstraction."  Minimum commands: - `/help` [command] - `/status` - `/model` [name] - `/profile` [name] - `/config` - `/tools` - `/skills` - `/diff` - `/commit` [message] - `/cancel` - `/resume` [session-id] - `/clear` - `/clear-session` - `/exit`

#### Types & Trait Declarations
- **Structs (31):** `AnswerCommandHandler`, `AuthorizeCommandHandler`, `CancelHandler`, `ClearHandler`, `ClearSessionHandler`, `CommandContext`, `CommitHandler`, `ConfigHandler`, `DiffHandler`, `DoctorHandler`, `ExecHandler`, `ExitHandler`, `GenesisHandler`, `HelpHandler`, `ModelHandler`, `NoPlanCommandHandler`, `PlanCommandHandler`, `ProfileHandler`, `ResumeHandler`, `RoadmapHandler`, `SettingsHandler`, `SkillsHandler`, `SlashCommand`, `SlashCommandRegistry`, `StatusHandler`, `TaskCommandHandler`, `TasksCommandHandler`, `ToolsHandler`, `VersionHandler`, `WorkflowCommandHandler`, `WorkspaceCommandHandler`
- **Enums (2):** `CommandOutput`, `CommandSideEffect`
- **Traits (1):** `CommandHandler`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn parse_slash_command(input: &str) -> (String, Vec<String>);
// pub
fn wrap_text(text: &str, width: usize) -> Vec<String>;
// pub
fn wrap_paragraphs(text: &str, width: usize) -> String;
// pub
fn render_field(label: &str, value: &str, width: usize) -> String;
// private
fn strip_quotes(s: &str) -> String;
// pub
fn info(text: impl Into<String>) -> Self;
// pub
fn error(msg: impl Into<String>) -> Self;
// private
async fn execute(&self,
        args: &[String],
        ctx: &CommandContext<'_>,) -> Result<CommandOutput, M31AError>;
// private
async fn execute(&self,
        args: &[String],
        ctx: &CommandContext<'_>,) -> Result<CommandOutput, M31AError>;
// pub
fn builtin(name: &'static str,
        description: &'static str,
        usage: &'static str,
        side_effect: Comm;
// pub
fn dynamic(name: String,
        description: String,
        usage: String,
        side_effect: CommandSideEffect,
   ;
// pub
fn with_alias(mut self, alias: impl Into<String>) -> Self;
// pub
fn with_help_details(mut self, details: impl Into<String>) -> Self;
// pub
fn with_user_command(mut self,
        def: Arc<crate::interaction::user_commands::UserCommandDefinition>,) -> Self;
// private
fn default() -> Self;
```

#### Unit Verification (8 inline tests)
Tests defined within module:
`test_slash_command_discovery_and_help`, `test_unknown_command_produces_structured_error`, `test_command_argument_parsing`, `test_parse_slash_command_quoted_strings`, `test_parse_slash_command_json`, `test_parse_slash_command_unquoted`, `test_parse_slash_command_mixed`, `test_parse_slash_command_edge_cases`

---

### `src/interaction/continuation.rs` {#src-interaction-continuation-rs}

- **Source Link:** [`src/interaction/continuation.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/interaction/continuation.rs)
- **Lines of Code:** 2614 (107976 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate | 🛑 Supports Cancellation Tokens

#### Primary Responsibility
runtime-layer conversational execution for submitted user text.  this module owns what the tui bridge must never own: end-to-end handling of a natural-language submission — mention injection, session turn persistence, governed front-door routing (pre_execution_coordinator), and supervised mission execution after authorization via autonomy_controller.  the tui bridge (`crate::tui::runtime_bridge`) only translates: it turns `application_action::user_text_submitted` into a call here, and turns the emitted `interaction_event`s into projection updates. execution truth and governance stay in the runtime/interaction layers.  core rule: runtime owns truth. tui owns presentation.

#### Types & Trait Declarations
- **Structs (1):** `ActiveExecution`

#### Key Functions & Signatures (9 shown)
```rust
// pub(crate)
fn emit(event_tx: &TuiInteractionSender, event: InteractionEvent) -> bool;
// pub
async fn handle_user_text_submitted(runtime: &mut Arc<AppRuntime>,
    workspace_root: &Path,
    session_repo: &SqliteS;
// private
async fn try_governed_front_door(runtime: &mut Arc<AppRuntime>,
    workspace_root: &Path,
    session: &mut Session,
  ;
// private
async fn execute_direct_agent_turn(runtime: &Arc<AppRuntime>,
    session: &mut Session,
    full_prompt: &str,
    clas;
// private
async fn invoke_lifecycle_action(action: ApplicationAction,
    runtime: &mut Arc<AppRuntime>,
    session_repo: &Sqlite;
// private
async fn handle_decision_response(resp: &crate::interaction::decision::InteractiveDecisionResponse,
    runtime: &mut Ar;
// pub(crate)
async fn handle_lifecycle_action(action: ApplicationAction,
    runtime: &mut Arc<AppRuntime>,
    session_repo: &Sqlite;
// private
fn fill_lifecycle_session_id(action: ApplicationAction, sid: &str) -> ApplicationAction;
// private
async fn emit_lifecycle_response(resp: PreExecutionResponse,
    runtime: &mut Arc<AppRuntime>,
    session: &mut Sessio;
```

---

### `src/interaction/decision.rs` {#src-interaction-decision-rs}

- **Source Link:** [`src/interaction/decision.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/interaction/decision.rs)
- **Lines of Code:** 817 (26950 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate | 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Strongly typed interactive decision model for user choices and workflow approvals (PRD §01, CLI-01).  Provides a unified, structured interaction abstraction replacing command-only prompts (such as `/plan accept`, `/tasks accept`, `/no-plan`, etc.) with native, interactive decision points across both CLI and TUI interfaces.

#### Types & Trait Declarations
- **Structs (4):** `DecisionOption`, `DecisionWaiterRegistry`, `InteractiveDecision`, `InteractiveDecisionResponse`
- **Enums (3):** `DecisionKind`, `DecisionResumeOutcome`, `DecisionState`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new(id: impl Into<String>,
        label: impl Into<String>,
        description: impl Into<String>,) -> Self;
// pub
fn with_value(mut self, value: impl Into<String>) -> Self;
// pub
fn is_pending(&self) -> bool;
// pub
fn is_submitting(&self) -> bool;
// pub
fn is_terminal(&self) -> bool;
// pub
fn planning_choice(session_id: impl Into<String>,
        _raw_prompt: impl Into<String>,
        question: impl Into<St;
// pub
fn plan_review(session_id: impl Into<String>,
        revision: u32,
        objective: impl Into<String>,
        task_;
// pub
fn tasks_review(session_id: impl Into<String>,
        plan_revision: u32,
        task_revision: u32,
        task_coun;
// pub
fn execution_authorization(session_id: impl Into<String>,
        plan_revision: u32,
        task_revision: u32,
      ;
// pub
fn discovery_question(session_id: impl Into<String>,
        question: &crate::workflow::genesis::DynamicQuestion,) -> S;
// pub
fn ask_user(session_id: impl Into<String>,
        execution_id: Option<String>,
        question_id: impl Into<String>,;
// pub
fn permission_approval(session_id: impl Into<String>,
        request_id: impl Into<String>,
        tool_name: impl Int;
// pub
fn select_next(&mut self);
// pub
fn select_prev(&mut self);
// pub
fn select_index(&mut self, idx: usize) -> bool;
```

---

### `src/interaction/events.rs` {#src-interaction-events-rs}

- **Source Link:** [`src/interaction/events.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/interaction/events.rs)
- **Lines of Code:** 1007 (33820 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
User-facing event stream abstraction decoupling CLI/TUI from internal scheduling (PRD §01, CLI-02).  Maps internal domain events and model/tool executions into structured, human- and machine-readable interaction events without scheduler coupling.

#### Types & Trait Declarations
- **Structs (1):** `QuarantineItemRecord`
- **Enums (2):** `EventDeliveryClass`, `InteractionEvent`

#### Key Functions & Signatures (2 shown)
```rust
// pub
fn format_human(&self) -> String;
// pub
fn delivery_class(&self) -> EventDeliveryClass;
```

---

### `src/interaction/mentions.rs` {#src-interaction-mentions-rs}

- **Source Link:** [`src/interaction/mentions.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/interaction/mentions.rs)
- **Lines of Code:** 650 (24523 bytes)

#### Primary Responsibility
Developer-oriented @mention parsing, path resolution, and context injection (PRD §01, CLI-01).  Supports: - `@file` - `@directory` - `@path:line` (e.g. `@src/parser.rs:120`) - `@path:start-end` (e.g. `@src/parser.rs:10-50`)  Enforces: - Workspace path confinement (rejection of `..`, `/etc/passwd`, symlink escapes) - Protection of internal `.m31a` storage paths - Bounded file/directory reads for context enrichment - Typed `MentionReference` and `ParsedUserMessage` structures

#### Types & Trait Declarations
- **Structs (4):** `LineRange`, `MentionParser`, `MentionReference`, `ParsedUserMessage`
- **Enums (3):** `MentionKind`, `MessageSegment`, `ResolutionStatus`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn single(line: usize) -> Self;
// pub
fn new(start: usize, end: usize) -> Self;
// pub
fn has_mentions(&self) -> bool;
// pub
fn resolved_mentions(&self) -> Vec<&MentionReference>;
// pub
fn normalized_prompt(&self) -> String;
// pub
fn parse(raw_text: &str, workspace_root: &Path) -> ParsedUserMessage;
// pub
fn parse_implicit_or_explicit(raw_text: &str, workspace_root: &Path) -> ParsedUserMessage;
// private
fn resolve_mention(original_text: &str,
        raw_path: &str,
        range_spec: Option<(usize, usize, bool);
// pub
fn inject_mention_context(_workspace_root: &Path, mentions: &[MentionReference]) -> String;
// private
fn test_parse_simple_file_and_dir_mentions();
// private
fn test_parse_line_and_range_mentions();
// private
fn test_reject_path_traversal();
// private
fn test_reject_m31a_internal_storage();
// private
fn test_malformed_line_range();
// private
fn test_missing_target();
```

#### Unit Verification (7 inline tests)
Tests defined within module:
`test_parse_simple_file_and_dir_mentions`, `test_parse_line_and_range_mentions`, `test_reject_path_traversal`, `test_reject_m31a_internal_storage`, `test_malformed_line_range`, `test_missing_target`, `test_trailing_sentence_punctuation`

---

### `src/interaction/mod.rs` {#src-interaction-mod-rs}

- **Source Link:** [`src/interaction/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/interaction/mod.rs)
- **Lines of Code:** 53 (2250 bytes)

#### Primary Responsibility
Developer Interaction Layer &amp; Agentic Interaction Protocol (PRD §01, CLI-01–CLI-04).  "Input -&gt; Interaction Parser -&gt; Typed Ui/Application Action -&gt; Application Command -&gt; Runtime -&gt; Events / State -&gt; CLI/TUI projection."  Exposes: - `action`: Typed UI and Application Actions (`ApplicationAction`, `InteractionIntent`) - `mentions`: @file, @directory, and @path:line parser and resolver - `commands`: Centralized slash command registry and command metadata - `session`: Durable session aggregate and conversation repository - `state`: Session prompt state machine - `events`: Decoupled user-facing interaction events - `parser`: Unified input parser and deterministic intent classifier - `approval`: Interactive CLI/TUI approval channel - `runner`: Interactive REPL session loop

---

### `src/interaction/parser.rs` {#src-interaction-parser-rs}

- **Source Link:** [`src/interaction/parser.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/interaction/parser.rs)
- **Lines of Code:** 368 (12838 bytes)

#### Primary Responsibility
Interaction Input Parser and Deterministic Intent Classifier (PRD §01, CLI-01).  "Input -&gt; Interaction Parser -&gt; Typed Application Action -&gt; Application Command -&gt; Runtime -&gt; Events / State -&gt; CLI/TUI projection."  "Do NOT use an LLM to classify simple slash commands. Deterministic parser first."

#### Types & Trait Declarations
- **Structs (1):** `InteractionParser`

#### Key Functions & Signatures (14 shown)
```rust
// private
fn default() -> Self;
// pub
fn new(command_registry: impl Into<std::sync::Arc<SlashCommandRegistry>>) -> Self;
// pub
fn with_snapshot_handle(handle: crate::interaction::user_commands::CommandSnapshotHandle,) -> Self;
// pub
fn set_snapshot_handle(&mut self,
        handle: crate::interaction::user_commands::CommandSnapshotHandle,);
// pub
fn set_command_registry(&mut self, registry: std::sync::Arc<SlashCommandRegistry>);
// pub
fn active_registry(&self) -> std::sync::Arc<SlashCommandRegistry>;
// pub
fn command_registry(&self) -> &SlashCommandRegistry;
// pub
fn command_registry_arc(&self) -> &std::sync::Arc<SlashCommandRegistry>;
// pub
fn classify_intent(&self,
        input: &str,
        prompt_state: SessionPromptState,
        has_active_mission: boo;
// pub
fn parse(&self,
        input: &str,
        workspace_root: &Path,
        prompt_state: SessionPromptState,
        ac;
// private
fn test_classify_slash_commands();
// private
fn test_classify_phrasal_inspection_and_commit();
// private
fn test_classify_approval_in_awaiting_state();
// private
fn test_parse_into_typed_application_action();
```

#### Unit Verification (4 inline tests)
Tests defined within module:
`test_classify_slash_commands`, `test_classify_phrasal_inspection_and_commit`, `test_classify_approval_in_awaiting_state`, `test_parse_into_typed_application_action`

---

### `src/interaction/runner.rs` {#src-interaction-runner-rs}

- **Source Link:** [`src/interaction/runner.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/interaction/runner.rs)
- **Lines of Code:** 2613 (131033 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate | 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Interactive CLI Session Runner and Terminal REPL Loop (PRD §01, CLI-01, CLI-04).  Provides the primary interactive developer experience: - Natural language task input - Structured multiline input (line continuation with `\`, block quotes with `"""`, paste) - Centralized slash command dispatch (/help, /status, /diff, /commit, etc.) - Real @file and @directory mention resolution and context injection - Follow-up conversation turns maintaining durable session history - Interactive approval prompt when policy triggers ASK - Graceful Ctrl-C cancellation preserving session integrity - Deterministic session persistence and resumption

#### Types & Trait Declarations
- **Structs (1):** `InteractiveSessionRunner`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn print_console_error(msg: impl std::fmt::Display);
// pub
fn new(runtime: Arc<AppRuntime>) -> Self;
// pub
fn current_session(&self) -> Option<&Session>;
// pub
fn session_repo(&self) -> &SqliteSessionRepository;
// pub
fn session_id(&self) -> Option<SessionId>;
// pub
fn workspace_root(&self) -> &Path;
// pub
fn runtime(&self) -> &Arc<AppRuntime>;
// pub
fn command_registry(&self) -> &Arc<SlashCommandRegistry>;
// pub
fn parser(&self) -> &InteractionParser;
// pub
fn has_active_engine(&self) -> bool;
// pub
fn active_engine(&self) -> Option<&AgentEngine>;
// pub
fn invalidate_engine(&mut self);
// pub
fn rebind_runtime(&mut self, runtime: Arc<AppRuntime>);
// pub
fn refresh_registry(&mut self);
// private
fn runtime_model_status(&self) -> (String, String, String);
```

---

### `src/interaction/session.rs` {#src-interaction-session-rs}

- **Source Link:** [`src/interaction/session.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/interaction/session.rs)
- **Lines of Code:** 1017 (37631 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
Durable interactive coding session aggregate and repository (PRD §01, MSN-05, CONTEXT.md §43).  Stores and reconstructs: - Session identity, workspace root, and active mission - Strictly ordered, typed conversation turns: - UserMessage - AssistantMessage - ToolCallMessage - ToolResultMessage - SystemMessage - ApprovalMessage - VerificationMessage  Enforces: - Zero transcript loss across process restarts - Foreign key satisfaction with SQLite missions table - Cryptographically unforgeable UUIDv7 IDs

#### Types & Trait Declarations
- **Structs (2):** `Session`, `SqliteSessionRepository`
- **Enums (1):** `ConversationTurn`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new(id: SessionId, workspace_root: PathBuf) -> Self;
// pub
fn sequence(&self) -> u64;
// pub
fn kind_str(&self) -> &'static str;
// pub
fn text_content(&self) -> &str;
// pub
fn new(pool: SqlitePool) -> Self;
// pub
fn with_event_bus(mut self, bus: Arc<dyn EventBus>) -> Self;
// pub
fn pool(&self) -> &SqlitePool;
// pub
async fn create_session(&self, workspace_root: &Path) -> Result<Session, M31AError>;
// pub
async fn get_session(&self, id: SessionId) -> Result<Option<Session>, M31AError>;
// pub
async fn list_sessions(&self) -> Result<Vec<Session>, M31AError>;
// pub
async fn set_active_mission(&self,
        session_id: SessionId,
        mission_id: MissionId,) -> Result<(), M31AErro;
// pub
async fn set_active_run(&self,
        session_id: SessionId,
        run_id: crate::ids::ExecutionRunId,) -> Result<(),;
// pub
async fn clear_active_run(&self, session_id: SessionId) -> Result<(), M31AError>;
// pub
async fn update_status(&self,
        session_id: SessionId,
        status: SessionState,) -> Result<(), M31AError>;
// pub
async fn set_planning_choice(&self,
        session_id: SessionId,
        choice: crate::runtime::PlanningChoice,) -> R;
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`test_session_lifecycle_and_conversation_persistence`

---

### `src/interaction/state.rs` {#src-interaction-state-rs}

- **Source Link:** [`src/interaction/state.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/interaction/state.rs)
- **Lines of Code:** 160 (7832 bytes)

#### Primary Responsibility
Interactive prompt and session lifecycle state machine (PRD §01, CLI-01, CLI-04).  Enforces explicit, legal state transitions during interactive developer coding sessions:  ```text ┌───────────────────────────────┐ │             Idle              │◄─────────────────┐ └───────┬───────────────▲───────┘                  │ │ (user types)  │                          │ ▼               │                          │ ┌───────────────┐       │ (cancel/complete)        │ │    Editing    │       │                          │ └───────┬───────┘       │                          │ │ (submit)      │                          │ ▼               │                          │ ┌───────────────┐       │                          │ │  Submitting   │───────┘ (command/info)           │ └───────┬───────┘                                  │ │ (run mission)                            │ ▼                                          │ ┌───────────────┐       (policy ask) ┌────────────────────┐ │   Executing   │───────────────────►│  AwaitingApproval  │ └───────┬───────┘◄───────────────────└────────────────────┘ │                (resolved) ▼ ┌───────────────┐ │  Completing   │──────────────────────────────────┘ └───────────────┘ ```

#### Types & Trait Declarations
- **Structs (1):** `StateTransitionError`
- **Enums (1):** `SessionPromptState`

#### Key Functions & Signatures (4 shown)
```rust
// pub
fn can_transition_to(&self, next: SessionPromptState) -> bool;
// pub
fn transition_to(&mut self, next: SessionPromptState) -> Result<(), StateTransitionError>;
// private
fn test_valid_transitions();
// private
fn test_invalid_transitions();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_valid_transitions`, `test_invalid_transitions`

---

### `src/interaction/user_commands.rs` {#src-interaction-user_commands-rs}

- **Source Link:** [`src/interaction/user_commands.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/interaction/user_commands.rs)
- **Lines of Code:** 1972 (69750 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Global User-Defined Slash Commands.  Lets an individual M31A user define their own slash commands as TOML prompt definitions in their **global user configuration directory**, without modifying M31A source code:  ```text &lt;global_config_dir&gt;/prompts/commands/atomic-commit.v1.toml  →  /atomic-commit ```  # Architecture  ```text Built-in slash commands + Global user slash commands ↓ SlashCommandRegistry (deterministic lookup/parsing; built-ins are reserved) ↓ PromptCommand (typed command contract — this module) ↓ PromptReference → canonical PromptCatalog → canonical PromptCompiler ↓ typed model invocation (ModelInvocationKind::UserCommand) ↓ model tool proposals → PolicyGate → ApprovalCoordinator → ToolPipeline ↓ Verification → CommandOutput ```  # Security model

#### Types & Trait Declarations
- **Structs (17):** `BoundArguments`, `CapabilitiesSection`, `CommandSection`, `CommandSnapshot`, `CommandSnapshotHandle`, `ExecutionSection`, `InputEntry`, `InputsSection`, `PromptCommand`, `PromptCommandHandler`, `TemplateSection`, `UserCommandDefinition`, `UserCommandFile`, `UserCommandInput`, `UserCommandLoadReport`, `UserCommandRejection`, `VerificationSection`
- **Enums (2):** `UserCommandError`, `UserCommandInputType`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn invalid(command: impl Into<String>, reason: impl Into<String>) -> Self;
// private
fn from(e: UserCommandError) -> Self;
// pub
fn parse(s: &str) -> Result<Self, String>;
// pub
fn as_str(&self) -> &'static str;
// pub
fn validate_value(&self, name: &str, value: &str) -> Result<(), String>;
// pub
fn prompt_reference(&self) -> PromptReference;
// pub
fn to_prompt_contract(&self) -> Result<PromptContract, UserCommandError>;
// pub
fn find_input(&self, flag: &str) -> Option<&UserCommandInput>;
// pub
fn bind_arguments(&self, args: &[String]) -> Result<BoundArguments, UserCommandError>;
// private
fn valid_flags_hint(&self) -> String;
// pub
fn generated_usage(&self) -> String;
// pub
fn describe(&self) -> String;
// pub
fn new(command: Arc<PromptCommand>) -> Result<Self, UserCommandError>;
// pub
fn from_prompt_command(command: impl Into<Arc<PromptCommand>>,) -> Result<Self, UserCommandError>;
// pub
fn new(snapshot: CommandSnapshot) -> Self;
```

#### Unit Verification (15 inline tests)
Tests defined within module:
`example_toml_parses_to_typed_contract`, `non_command_kind_rejected`, `non_command_namespace_rejected`, `layer0_and_behavioral_ids_rejected`, `invalid_names_rejected`, `undeclared_template_variable_rejected`, `malformed_template_rejected`, `argument_binding_validates_deterministically`, `required_verification_requires_at_least_one_check`, `verification_check_names_are_trimmed_before_storage`...

---
