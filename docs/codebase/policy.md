# Policy Engine & Security Gates

> **Architectural Layer:** L1 Security  
> **Source Directory:** `src/policy`  
> **File Count:** 15 source files  

Non-bypassable policy evaluation, 4 decisions (Allow/Deny/Ask/Escalate), and approvals.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [adapter.rs](#src-policy-approval-adapter-rs) | 216 | `ProductionEscalationChannel` | Production EscalationChannel implementation integrating ApprovalCoordi... |
| [channel.rs](#src-policy-approval-channel-rs) | 46 | `ApprovalError` | Asynchronous approval notification and response channel trait (POL-01,... |
| [coordinator.rs](#src-policy-approval-coordinator-rs) | 822 | `ApprovalCoordinator` | Concurrent approval coordinator managing async waiter multiplexing and... |
| [explanation.rs](#src-policy-approval-explanation-rs) | 98 | `ApprovalExplanationPacket` | Structured approval explanation packet generator with progressive disc... |
| [grant.rs](#src-policy-approval-grant-rs) | 307 | `PolicyGrant, PolicyGrantStore` | Durable SQLite persistent grants repository evaluated at Layer 9 (POL-... |
| [mod.rs](#src-policy-approval-mod-rs) | 293 | `ApprovalRequest, ApprovalAction, ApprovalRequestState` | Interactive approval workflow, concurrent coordinator, and persistent ... |
| [audit.rs](#src-policy-audit-rs) | 281 | `DurablePolicyAuditor, PolicyDecisionAuditRow` | Durable policy audit logging in SQLite (POL-05, D-04). |
| [defaults.rs](#src-policy-defaults-rs) | 227 | `Functions/Traits` | Hardcoded Layer 1 built-in safety vetoes and POL-04 developer defaults... |
| [destination.rs](#src-policy-destination-rs) | 627 | `NetworkDestinationPolicy, ValidatedSocketAddr, ValidatingDnsResolver` | Centralized Network Destination Policy and SSRF Defense (SEC-NET, Find... |
| [effective.rs](#src-policy-effective-rs) | 488 | `EffectivePolicy, EffectivePolicyBuilder, PolicyDecisionRecord` | Effective policy compiler and evaluation engine implementing PolicyGat... |
| [file.rs](#src-policy-file-rs) | 61 | `PolicyFileError` | Declarative policy file loader and syntax validator (POL-01, D-01). |
| [layers.rs](#src-policy-layers-rs) | 182 | `PolicyLayer` | 10-tier policy layer hierarchy and non-weakening decision merger (POL-... |
| [matcher.rs](#src-policy-matcher-rs) | 612 | `PolicyEvaluationContext, PolicyMatcher` | Structured policy matching for tools, paths, arguments, roles, and aut... |
| [mod.rs](#src-policy-mod-rs) | 27 | `Functions/Traits` | Policy engine, multi-layer evaluation hierarchy, and authorization enf... |
| [rule.rs](#src-policy-rule-rs) | 96 | `PolicyDocument, PolicyRule` | Declarative policy document and rule AST definitions (POL-01, POL-02, ... |

---

### `src/policy/approval/adapter.rs` {#src-policy-approval-adapter-rs}

- **Source Link:** [`src/policy/approval/adapter.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/policy/approval/adapter.rs)
- **Lines of Code:** 216 (7718 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence

#### Primary Responsibility
Production EscalationChannel implementation integrating ApprovalCoordinator and SQLite persistence (AUT-01, POL-01, BLK-02).

#### Types & Trait Declarations
- **Structs (1):** `ProductionEscalationChannel`

#### Key Functions & Signatures (6 shown)
```rust
// private
fn default() -> Self;
// pub
fn new(pool: Option<SqlitePool>) -> Self;
// pub
fn with_coordinator(mut self, coordinator: Arc<ApprovalCoordinator>) -> Self;
// pub
async fn resolve(&self,
        id: EscalationRequestId,
        response: EscalationResponse,) -> Result<(), Escalation;
// private
async fn request_escalation(&self,
        req: EscalationRequest,) -> Result<EscalationRequestId, EscalationError>;
// private
async fn check_response(&self,
        id: EscalationRequestId,) -> Result<Option<EscalationResponse>, EscalationError>;
```

---

### `src/policy/approval/channel.rs` {#src-policy-approval-channel-rs}

- **Source Link:** [`src/policy/approval/channel.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/policy/approval/channel.rs)
- **Lines of Code:** 46 (1507 bytes)

#### Primary Responsibility
Asynchronous approval notification and response channel trait (POL-01, D-09).

#### Types & Trait Declarations
- **Enums (1):** `ApprovalError`
- **Traits (1):** `ApprovalChannel`

#### Key Functions & Signatures (2 shown)
```rust
// private
async fn notify_request(&self, packet: &ApprovalExplanationPacket) -> Result<(), ApprovalError>;
// private
async fn poll_response(&self,
        id: ApprovalRequestId,) -> Result<Option<ApprovalAction>, ApprovalError>;
```

---

### `src/policy/approval/coordinator.rs` {#src-policy-approval-coordinator-rs}

- **Source Link:** [`src/policy/approval/coordinator.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/policy/approval/coordinator.rs)
- **Lines of Code:** 822 (35510 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence | 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Concurrent approval coordinator managing async waiter multiplexing and cancellation cascades (POL-01, D-09, D-11).

#### Types & Trait Declarations
- **Structs (1):** `ApprovalCoordinator`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new(pool: Option<SqlitePool>, channel: Option<Arc<dyn ApprovalChannel>>) -> Self;
// pub
fn with_event_bus(mut self, bus: Arc<dyn crate::events::EventBus>) -> Self;
// pub
fn with_channel(self, channel: Arc<dyn ApprovalChannel>) -> Self;
// pub
fn set_channel(&self, channel: Arc<dyn ApprovalChannel>);
// pub
async fn has_active_waiter(&self, id: &ApprovalRequestId) -> bool;
// pub
async fn active_waiters_count(&self) -> usize;
// pub
async fn pending_request_ids(&self) -> Vec<crate::ids::ApprovalRequestId>;
// pub
async fn task_mapping_count(&self) -> usize;
// pub
fn wait_for_approval(&self) -> bool;
// pub
fn set_wait_for_approval(&self, wait: bool);
// pub
fn with_wait_for_approval(self, wait: bool) -> Self;
// pub
fn set_wait_for_approval_for(&self, mission_id: MissionId, wait: bool);
// pub
fn clear_wait_for_approval_for(&self, mission_id: MissionId);
// pub
fn effective_wait_for_approval(&self, mission_id: MissionId) -> bool;
// private
async fn remove_task_mapping(&self, task_id: Option<TaskId>, req_id: ApprovalRequestId);
```

---

### `src/policy/approval/explanation.rs` {#src-policy-approval-explanation-rs}

- **Source Link:** [`src/policy/approval/explanation.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/policy/approval/explanation.rs)
- **Lines of Code:** 98 (3801 bytes)

#### Primary Responsibility
Structured approval explanation packet generator with progressive disclosure (POL-01, D-12).

#### Types & Trait Declarations
- **Structs (1):** `ApprovalExplanationPacket`

#### Key Functions & Signatures (2 shown)
```rust
// pub
fn redact_sensitive_arguments(args: &serde_json::Value) -> serde_json::Value;
// pub
fn format_explanation_packet(req: &ApprovalRequest) -> ApprovalExplanationPacket;
```

---

### `src/policy/approval/grant.rs` {#src-policy-approval-grant-rs}

- **Source Link:** [`src/policy/approval/grant.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/policy/approval/grant.rs)
- **Lines of Code:** 307 (10816 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence | 🛡️ Enforces Policy Gate

#### Primary Responsibility
Durable SQLite persistent grants repository evaluated at Layer 9 (POL-03, D-10).

#### Types & Trait Declarations
- **Structs (2):** `PolicyGrant`, `PolicyGrantStore`

#### Key Functions & Signatures (7 shown)
```rust
// pub
fn new(mission_id: MissionId,
        task_id: Option<TaskId>,
        scope_type: ApprovalResolutionScope,
        tool;
// pub
fn new() -> Self;
// pub
async fn create_grant(&self,
        pool: &SqlitePool,
        grant: &PolicyGrant,) -> Result<(), sqlx::Error>;
// pub
async fn find_applicable_grants(&self,
        pool: &SqlitePool,
        mission_id: MissionId,
        task_id: Option;
// pub
async fn consume_one_shot_grant(&self,
        pool: &SqlitePool,
        grant_id: uuid::Uuid,) -> Result<bool, sqlx::E;
// pub
async fn invalidate_task_grants(&self,
        pool: &SqlitePool,
        task_id: TaskId,) -> Result<u64, sqlx::Error>;
// pub
async fn invalidate_mission_grants(&self,
        pool: &SqlitePool,
        mission_id: MissionId,) -> Result<u64, sqlx;
```

---

### `src/policy/approval/mod.rs` {#src-policy-approval-mod-rs}

- **Source Link:** [`src/policy/approval/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/policy/approval/mod.rs)
- **Lines of Code:** 293 (8882 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Interactive approval workflow, concurrent coordinator, and persistent session grants (POL-01, D-09, D-10, D-11, D-12).

#### Types & Trait Declarations
- **Structs (1):** `ApprovalRequest`
- **Enums (4):** `ApprovalAction`, `ApprovalRequestState`, `ApprovalResolutionScope`, `ApprovalTarget`

#### Key Functions & Signatures (12 shown)
```rust
// pub
fn as_str(&self) -> &'static str;
// pub
fn as_str(&self) -> &'static str;
// pub
fn is_allowed(&self) -> bool;
// pub
fn resolution_scope(&self) -> Option<ApprovalResolutionScope>;
// pub
fn tool_call(id: ToolCallId) -> Self;
// pub
fn user_command(command_id: impl Into<String>,
        command_version: u32,
        invocation_id: uuid::Uuid,) -> Self;
// pub
fn target_identifier(&self) -> String;
// pub
fn is_command(&self) -> bool;
// pub
fn is_tool_call(&self) -> bool;
// pub
fn new(mission_id: MissionId,
        task_id: Option<TaskId>,
        agent_id: Option<AgentId>,
        tool_call_id: ;
// pub
fn new_user_command(mission_id: MissionId,
        task_id: Option<TaskId>,
        agent_id: Option<AgentId>,
        c;
// pub
fn with_target(mission_id: MissionId,
        task_id: Option<TaskId>,
        agent_id: Option<AgentId>,
        target;
```

---

### `src/policy/audit.rs` {#src-policy-audit-rs}

- **Source Link:** [`src/policy/audit.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/policy/audit.rs)
- **Lines of Code:** 281 (9760 bytes)
- **Runtime Properties:** 💾 Interacts with SQLite Persistence | 🛡️ Enforces Policy Gate

#### Primary Responsibility
Durable policy audit logging in SQLite (POL-05, D-04).

#### Types & Trait Declarations
- **Structs (2):** `DurablePolicyAuditor`, `PolicyDecisionAuditRow`

#### Key Functions & Signatures (6 shown)
```rust
// pub
fn hash_normalized_arguments(args: &serde_json::Value) -> String;
// pub
fn new() -> Self;
// pub
async fn record_decision(&self,
        pool: &SqlitePool,
        mission_id: MissionId,
        task_id: Option<TaskId;
// pub
async fn record_domain_decision(&self,
        pool: &SqlitePool,
        mission_id: MissionId,
        task_id: Option;
// pub
async fn get_decision(&self,
        pool: &SqlitePool,
        id: PolicyEvaluationId,) -> Result<Option<PolicyDecision;
// pub
async fn list_decisions_for_mission(&self,
        pool: &SqlitePool,
        mission_id: MissionId,) -> Result<Vec<Poli;
```

---

### `src/policy/defaults.rs` {#src-policy-defaults-rs}

- **Source Link:** [`src/policy/defaults.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/policy/defaults.rs)
- **Lines of Code:** 227 (9756 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Hardcoded Layer 1 built-in safety vetoes and POL-04 developer defaults (POL-04, POL-06, D-02, D-04).

#### Key Functions & Signatures (2 shown)
```rust
// pub
fn built_in_safety_rules() -> Vec<PolicyRule>;
// pub
fn developer_defaults() -> Vec<PolicyRule>;
```

---

### `src/policy/destination.rs` {#src-policy-destination-rs}

- **Source Link:** [`src/policy/destination.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/policy/destination.rs)
- **Lines of Code:** 627 (22419 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Centralized Network Destination Policy and SSRF Defense (SEC-NET, Findings H &amp; I).  Enforces strict egress security controls across all network, web, and HTTP clients. Blocks access to: - Loopback addresses (127.0.0.0/8, ::1) - RFC 1918 private IPv4 ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) - Link-local ranges (169.254.0.0/16, fe80::/10) - Cloud instance metadata services (169.254.169.254, [fd00:ec2::254], etc.) - IPv6 unique-local / private ranges (fc00::/7) - IPv6 loopback, unspecified, and discard ranges - IPv4-mapped / IPv4-compatible IPv6 addresses encoding blocked IPv4 addresses - Broadcast and multicast ranges (224.0.0.0/4, ff00::/8, 255.255.255.255) - Documentation and reserved test networks (192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24, 2001:db8::/32) - Carrier-grade NAT (100.64.0.0/10) - Unspecified addresses (0.0.0.0, ::)  Hostnames are resolved through DNS and all resolved IP addresses are validated before connection. Redirect targets are step-by-step validated so that public endpoints cannot redirect to private targets.

#### Types & Trait Declarations
- **Structs (3):** `NetworkDestinationPolicy`, `ValidatedSocketAddr`, `ValidatingDnsResolver`
- **Enums (1):** `NetworkSecurityError`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new() -> Self;
// pub
fn is_ipv4_blocked(ip: &Ipv4Addr) -> Option<&'static str>;
// pub
fn is_ipv6_blocked(ip: &Ipv6Addr) -> Option<&'static str>;
// pub
fn is_ip_blocked(ip: &IpAddr) -> Option<&'static str>;
// pub
fn validate_ip(&self, ip: IpAddr) -> Result<(), NetworkSecurityError>;
// pub
async fn validate_host(&self, host: &str) -> Result<Vec<IpAddr>, NetworkSecurityError>;
// pub
async fn validate_url(&self, raw_url: &str) -> Result<reqwest::Url, NetworkSecurityError>;
// pub
async fn resolve_socket_addrs(&self,
        host: &str,
        port: u16,) -> Result<Vec<ValidatedSocketAddr>, Network;
// pub
async fn connect_validated(&self,
        validated: &ValidatedSocketAddr,
        timeout: std::time::Duration,) -> Res;
// pub
fn socket_addr(&self) -> SocketAddr;
// pub
fn host(&self) -> &str;
// pub
fn port(&self) -> u16;
// private
fn resolve(&self, name: reqwest::dns::Name) -> reqwest::dns::Resolving;
// pub
fn policy_validating_client_builder() -> reqwest::ClientBuilder;
// private
fn test_loopback_blocked();
```

#### Unit Verification (9 inline tests)
Tests defined within module:
`test_loopback_blocked`, `test_rfc1918_private_ipv4_blocked`, `test_metadata_service_blocked`, `test_link_local_blocked`, `test_ipv6_unique_local_blocked`, `test_public_ips_allowed`, `test_ipv4_mapped_ipv6_loopback_blocked`, `test_localhost_aliases_blocked`, `test_url_schemes`

---

### `src/policy/effective.rs` {#src-policy-effective-rs}

- **Source Link:** [`src/policy/effective.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/policy/effective.rs)
- **Lines of Code:** 488 (18973 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Effective policy compiler and evaluation engine implementing PolicyGate (POL-01, POL-02, POL-03, D-01, D-02).

#### Types & Trait Declarations
- **Structs (3):** `EffectivePolicy`, `EffectivePolicyBuilder`, `PolicyDecisionRecord`
- **Enums (1):** `PolicyLoadError`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn to_contract(&self) -> PolicyDecisionContract;
// private
fn from(r: PolicyDecisionRecord) -> Self;
// private
fn from(r: &PolicyDecisionRecord) -> Self;
// pub
fn new(layers: Vec<(PolicyLayer, Vec<PolicyRule>);
// pub
fn new_with_fallback(mut layers: Vec<(PolicyLayer, Vec<PolicyRule>);
// pub
fn builder() -> EffectivePolicyBuilder;
// pub
fn restricted() -> Self;
// pub
fn standard(workspace_root: &Path) -> Result<Self, PolicyLoadError>;
// pub
fn try_standard(workspace_root: &Path) -> Result<Self, PolicyLoadError>;
// pub
fn standard_with_policy_config(workspace_root: &Path,
        policy_config: Option<&crate::config::PolicyConfig>,) -> R;
// pub
fn try_standard_with_policy_config(workspace_root: &Path,
        policy_config: Option<&crate::config::PolicyConfig>,) ;
// pub
fn active_policy_hash(&self) -> &str;
// pub
fn extended_for_execution(&self,
        mission_rules: Vec<PolicyRule>,
        agent_role_rules: Vec<PolicyRule>,
    ;
// pub
fn layers(&self) -> &[(PolicyLayer, Vec<PolicyRule>)];
// pub
fn evaluate_request(&self,
        ctx: &PolicyEvaluationContext,) -> (PolicyDecision, PolicyDecisionRecord);
```

---

### `src/policy/file.rs` {#src-policy-file-rs}

- **Source Link:** [`src/policy/file.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/policy/file.rs)
- **Lines of Code:** 61 (2147 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Declarative policy file loader and syntax validator (POL-01, D-01).

#### Types & Trait Declarations
- **Enums (1):** `PolicyFileError`

#### Key Functions & Signatures (3 shown)
```rust
// pub
fn from_toml_str(content: &str) -> Result<Self, PolicyFileError>;
// pub
fn load_from_file(path: &Path) -> Result<Self, PolicyFileError>;
// pub
async fn load_from_file_async(path: &Path) -> Result<Self, PolicyFileError>;
```

---

### `src/policy/layers.rs` {#src-policy-layers-rs}

- **Source Link:** [`src/policy/layers.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/policy/layers.rs)
- **Lines of Code:** 182 (7072 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
10-tier policy layer hierarchy and non-weakening decision merger (POL-03, POL-06, D-02).

#### Types & Trait Declarations
- **Enums (1):** `PolicyLayer`

#### Key Functions & Signatures (9 shown)
```rust
// pub
fn precedence_rank(self) -> u32;
// pub
fn name(self) -> &'static str;
// pub
fn authority_source(self) -> &'static str;
// pub
fn merge_preliminary_decision(higher: (PolicyDecision, PolicyLayer, String);
// private
fn test_layer_ranking_order();
// private
fn test_built_in_deny_is_immutable_veto();
// private
fn test_lower_layer_can_further_restrict();
// private
fn test_lower_layer_cannot_weaken_deny();
// private
fn test_session_approval_can_resolve_ask();
```

#### Unit Verification (5 inline tests)
Tests defined within module:
`test_layer_ranking_order`, `test_built_in_deny_is_immutable_veto`, `test_lower_layer_can_further_restrict`, `test_lower_layer_cannot_weaken_deny`, `test_session_approval_can_resolve_ask`

---

### `src/policy/matcher.rs` {#src-policy-matcher-rs}

- **Source Link:** [`src/policy/matcher.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/policy/matcher.rs)
- **Lines of Code:** 612 (21424 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Structured policy matching for tools, paths, arguments, roles, and autonomy modes (POL-01, D-03).

#### Types & Trait Declarations
- **Structs (2):** `PolicyEvaluationContext`, `PolicyMatcher`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new(tool_id: impl Into<String>, workspace_root: PathBuf) -> Self;
// pub
fn with_target_paths(mut self, paths: Vec<PathBuf>) -> Self;
// pub
fn with_args(mut self, args: serde_json::Value) -> Self;
// pub
fn with_role(mut self, role: AgentRole) -> Self;
// pub
fn with_mode(mut self, mode: AutonomyMode) -> Self;
// pub
fn try_from_request(req: &PolicyEvaluationRequest) -> Result<Self, PolicyError>;
// pub
fn from_request(req: &PolicyEvaluationRequest) -> Self;
// pub
fn extract_shell_tokens(cmd: &str) -> Vec<String>;
// pub
fn lexical_normalize(path: &Path) -> PathBuf;
// pub
fn canonicalize_and_validate_path(path: &Path,
    workspace_root: &Path,) -> Result<PathBuf, PolicyError>;
// pub
fn glob_to_regex(glob: &str, is_path: bool) -> String;
// pub
fn matches_tool(pattern: &str, tool_id: &str) -> bool;
// pub
fn matches_path(pattern: &str, target_path: &Path, workspace_root: &Path) -> bool;
// pub
fn matches_args(pattern_args: Option<&serde_json::Value>,
        actual_args: &serde_json::Value,) -> bool;
// private
fn matches_single_arg(expected: &serde_json::Value, actual: &serde_json::Value) -> bool;
```

---

### `src/policy/mod.rs` {#src-policy-mod-rs}

- **Source Link:** [`src/policy/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/policy/mod.rs)
- **Lines of Code:** 27 (1096 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Policy engine, multi-layer evaluation hierarchy, and authorization enforcement (POL-01..POL-06).

---

### `src/policy/rule.rs` {#src-policy-rule-rs}

- **Source Link:** [`src/policy/rule.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/policy/rule.rs)
- **Lines of Code:** 96 (2826 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Declarative policy document and rule AST definitions (POL-01, POL-02, D-01).

#### Types & Trait Declarations
- **Structs (2):** `PolicyDocument`, `PolicyRule`

#### Key Functions & Signatures (8 shown)
```rust
// pub
fn new(name: Option<String>, rules: Vec<PolicyRule>) -> Self;
// pub
fn new(id: impl Into<String>, decision: PolicyDecision) -> Self;
// pub
fn with_description(mut self, description: impl Into<String>) -> Self;
// pub
fn with_tools(mut self, tools: impl IntoIterator<Item = impl Into<String>>) -> Self;
// pub
fn with_paths(mut self, paths: impl IntoIterator<Item = impl Into<String>>) -> Self;
// pub
fn with_args(mut self, args: serde_json::Value) -> Self;
// pub
fn with_roles(mut self, roles: impl IntoIterator<Item = AgentRole>) -> Self;
// pub
fn with_modes(mut self, modes: impl IntoIterator<Item = AutonomyMode>) -> Self;
```

---
