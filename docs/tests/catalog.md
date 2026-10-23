# Complete Test Suite Catalog

> **Exhaustive Test Inventory:** 266 first-party Rust test suites under `tests/`.

M31A maintains a rigorous multi-tier test architecture enforcing architectural invariants, security policies, deterministic execution, and release qualification.

## Test Partitioning Summary

- **Deterministic CI Tests (240+ suites):** Run in continuous integration without network or credential dependencies, utilizing mock doubles and isolated temporary worktrees.
- **Live Model Tests (Partitioned):** Marked with `#[ignore]` and categorized in `tests/support/live_inventory.rs`. Require explicit `NVIDIA_API_KEY` and are invoked only via `make test-live` or dedicated workflows.
- **Architectural Enforcement Tests:** Ensure layer boundaries, single-crate invariants, and fail-closed security properties cannot be violated.

## Complete Inventory of 266 Test Files

| Test Suite File | Lines | Test Functions | Category | Key Tested Modules |
|---|:---:|:---:|---|---|
| `tests/architectural_consolidation.rs` | 278 | 7 | Integration | `config::paths::PlatformPaths` |
| `tests/architecture_change_authority.rs` | 139 | 12 | Architecture | `change::( AppliedChangeSet, AtomicChangeApplier, ChangeAp...` |
| `tests/architecture_context_engine.rs` | 143 | 5 | Architecture | `Integration` |
| `tests/architecture_credential_boundary.rs` | 577 | 14 | Architecture | `Integration` |
| `tests/architecture_engineering_memory.rs` | 131 | 4 | Architecture | `context::envelope::(TrustEnvelope, TrustLevel)` |
| `tests/architecture_invariants.rs` | 775 | 12 | Architecture | `capability::providers::CliGitProvider` |
| `tests/architecture_invariants_runtime.rs` | 620 | 7 | Architecture | `capability::providers::CliGitProvider` |
| `tests/architecture_kernel_purification.rs` | 343 | 11 | Architecture | `kernel::plan::( CandidatePlan, CandidateTask, CandidateTa...` |
| `tests/architecture_live_test_partition.rs` | 1060 | 9 | Architecture | `Integration` |
| `tests/architecture_persistence_authority.rs` | 436 | 7 | Architecture | `ids::(MissionId, TaskId)` |
| `tests/architecture_planning_authority.rs` | 178 | 12 | Architecture | `kernel::CandidateTask as KernelTask` |
| `tests/architecture_process_authority.rs` | 267 | 3 | Architecture | `Integration` |
| `tests/architecture_redesign_unification.rs` | 240 | 4 | Architecture | `events::bus::BroadcastEventBus` |
| `tests/architecture_repository_intelligence.rs` | 214 | 6 | Architecture | `repo::query::( CEILING_MAX_BYTES, CEILING_MAX_DEPTH, CEIL...` |
| `tests/architecture_runtime_authority.rs` | 738 | 19 | Architecture | `agent::engine::(AgentEngine, AgentTurnOutcome)` |
| `tests/artifact_consolidation.rs` | 993 | 19 | Integration | `ids::(ArtifactId, CheckId, MissionId, TaskId, WorkflowRun...` |
| `tests/audit_render_inspector.rs` | 51 | 1 | Integration | `tui::TuiApplication` |
| `tests/checkpoint_authority_test.rs` | 279 | 2 | Architecture | `checkpoint::crash_recovery::(CrashRecoveryClassification,...` |
| `tests/common/git_auth.rs` | 233 | 0 | Integration | `git::(AuthorizationAuthority, GIT_AUTH_DEFAULT_TTL, GitGa...` |
| `tests/common/mod.rs` | 4 | 0 | Integration | `Integration` |
| `tests/common/tui_fixtures.rs` | 194 | 0 | Integration | `tui::TuiApplication` |
| `tests/config_architecture_enforcement.rs` | 647 | 18 | Architecture | `config::canonical as C` |
| `tests/config_authority_invariants.rs` | 544 | 27 | Architecture | `config::canonical as C` |
| `tests/configuration_authority.rs` | 817 | 9 | Architecture | `cli::dispatch::(CliDispatcher, RuntimeCommand)` |
| `tests/dag_consolidation.rs` | 655 | 18 | Integration | `dag::ops::( GraphAdjacency, GraphError, compute_waves_val...` |
| `tests/dead_wiring_elimination_guards.rs` | 392 | 7 | Integration | `agent::delegation::DelegationContract` |
| `tests/deployment_channels.rs` | 715 | 18 | Integration | `cli::(CliDispatcher, RuntimeCommand)` |
| `tests/docs_contract.rs` | 251 | 7 | Integration | `agent::registry::RoleRegistry` |
| `tests/dynamic_model_discovery.rs` | 1160 | 28 | Integration | `agent::model_policy::(ModelCaller, RoutedModelCaller)` |
| `tests/execution_run_convergence.rs` | 1026 | 29 | Integration | `ids::ExecutionRunId` |
| `tests/fresh_session_execution_regression.rs` | 958 | 8 | Integration | `ids::SessionId` |
| `tests/genesis_adrs.rs` | 180 | 6 | Integration | `planning::requirements::(Provenance, ProvenanceSourceType...` |
| `tests/genesis_architecture.rs` | 370 | 5 | Architecture | `planning::requirements::( EngineeringRequirement, Epistem...` |
| `tests/genesis_brownfield.rs` | 110 | 3 | Integration | `workflow::genesis::BrownfieldMap` |
| `tests/genesis_discovery.rs` | 199 | 7 | Integration | `workflow::genesis::( ConvergenceReason, DiscoveryPillar, ...` |
| `tests/genesis_environment.rs` | 153 | 6 | Integration | `workflow::genesis::(EnvironmentCategory, GenesisMode, Wor...` |
| `tests/genesis_invalidation.rs` | 460 | 7 | Integration | `planning::requirements::( EngineeringRequirement, Epistem...` |
| `tests/genesis_planning_governance.rs` | 458 | 6 | Integration | `agent::model_policy::(ModelCaller, ModelProposal)` |
| `tests/genesis_requirements.rs` | 249 | 7 | Integration | `planning::requirements::( EngineeringRequirement, Epistem...` |
| `tests/genesis_research.rs` | 185 | 6 | Integration | `state_machine::agent::AgentRole` |
| `tests/genesis_roadmap.rs` | 377 | 5 | Integration | `planning::requirements::( EngineeringRequirement, Epistem...` |
| `tests/genesis_runtime_integration.rs` | 1513 | 28 | Integration | `agent::model_policy::(ModelCaller, ModelProposal, ModelTo...` |
| `tests/genesis_synthesis.rs` | 113 | 3 | Integration | `workflow::genesis::( ProjectCharter, ResearchDimension, R...` |
| `tests/genesis_traceability.rs` | 219 | 4 | Integration | `planning::requirements::( EngineeringRequirement, Epistem...` |
| `tests/git_decoupled_coding.rs` | 405 | 8 | Integration | `agent::model_policy::(ModelCaller, ModelProposal)` |
| `tests/golden_agentic_workflow.rs` | 405 | 3 | Integration | `agent::model_policy::(ModelCaller, ModelProposal, ModelTo...` |
| `tests/golden_configuration_runtime.rs` | 606 | 1 | Integration | `agent::model_policy::(ModelCaller, ModelProposal, ModelTo...` |
| `tests/golden_configuration_workflow.rs` | 172 | 1 | Integration | `cli::dispatch::(CliDispatcher, RuntimeCommand)` |
| `tests/golden_interactive_session.rs` | 495 | 3 | Integration | `config::env::SafeEnvironmentStatus` |
| `tests/golden_project_genesis_planning.rs` | 348 | 2 | Integration | `planning::requirements::RequirementCategory` |
| `tests/golden_project_genesis_research.rs` | 243 | 1 | Integration | `agent::model_policy::(ModelCaller, ModelProposal)` |
| `tests/golden_project_genesis_workflow.rs` | 592 | 1 | Integration | `agent::model_policy::(ModelCaller, ModelProposal)` |
| `tests/golden_real_model_workflow.rs` | 407 | 3 | Integration | `config::env::SafeEnvironmentStatus` |
| `tests/golden_tui_2_scenarios.rs` | 527 | 10 | Integration | `tui::TuiApplication` |
| `tests/golden_tui_agentic_workflow.rs` | 392 | 1 | Integration | `events::bus::BroadcastEventBus` |
| `tests/golden_tui_conversation_first.rs` | 344 | 10 | Integration | `tui::TuiApplication` |
| `tests/golden_tui_pty_scenario.rs` | 333 | 2 | Integration | `Integration` |
| `tests/golden_wizard_model_selection.rs` | 755 | 14 | Integration | `init::lifecycle::SetupStep` |
| `tests/interactive_decision_overhaul.rs` | 505 | 10 | Integration | `interaction::decision::( DecisionKind, DecisionState, Int...` |
| `tests/isolation_boundary_hardening.rs` | 231 | 4 | Integration | `agent::model_policy::(ModelCaller, ModelProposal)` |
| `tests/live_model_e2e.rs` | 941 | 5 | Live Model | `dag::materializer::TaskGraphMaterializer` |
| `tests/migration_029_budget_removal.rs` | 266 | 1 | Integration | `ids::MissionId` |
| `tests/migration_030_execution_run.rs` | 276 | 1 | Integration | `persistence::sqlite::pool::create_pool` |
| `tests/mission_task_authority.rs` | 249 | 6 | Architecture | `agent::model_policy::(ModelCaller, ModelProposal)` |
| `tests/october_14_audit_remediation.rs` | 1014 | 7 | Integration | `checkpoint::manager::(CheckpointManager, StagedArtifactIn...` |
| `tests/onboarding_wizard_remediation.rs` | 768 | 21 | Integration | `config::provider_registry::ProviderRegistry` |
| `tests/output_hygiene.rs` | 177 | 3 | Integration | `Integration` |
| `tests/p0_execution_path_and_tui_state.rs` | 468 | 6 | Integration | `events::envelope::EventEnvelope` |
| `tests/p0_safety_remediation_test.rs` | 1038 | 9 | Integration | `agent::runner::ActionRequest` |
| `tests/p0_startup_assembly_regression.rs` | 823 | 20 | Integration | `checkpoint::crash_recovery::(CrashRecoveryClassification,...` |
| `tests/p1_remediation_test.rs` | 811 | 11 | Integration | `agent::profile::AgentProfile` |
| `tests/p2_remediation_test.rs` | 847 | 17 | Integration | `checkpoint::crash_recovery::StartupCrashRecoveryScanner` |
| `tests/p3_agent_execution_test.rs` | 584 | 17 | Integration | `agent::model_policy::(ModelCaller, ModelProposal, ModelTo...` |
| `tests/parity.rs` | 98 | 0 | Parity | `Integration` |
| `tests/parity/capability_reporting.rs` | 135 | 8 | Parity | `platform::capabilities::(Capability, CapabilityState, Pla...` |
| `tests/parity/credential_file_protection.rs` | 135 | 6 | Parity | `platform::permissions::(enforcement_description, ensure_p...` |
| `tests/parity/environment_isolation.rs` | 183 | 6 | Parity | `process::env::EnvironmentBuilder` |
| `tests/parity/failure_semantics.rs` | 167 | 6 | Parity | `platform::errors::(PlatformError, from_io)` |
| `tests/parity/filesystem_containment.rs` | 218 | 12 | Parity | `platform::filesystem::HostFilesystem` |
| `tests/parity/linux/bubblewrap_isolation.rs` | 59 | 2 | Parity | `platform::capabilities::(CapabilityState, PlatformCapabil...` |
| `tests/parity/linux/cgroups_v2_enforcement.rs` | 64 | 2 | Parity | `platform::filesystem::HostFilesystem` |
| `tests/parity/linux/proc_starttime_protection.rs` | 47 | 2 | Parity | `Integration` |
| `tests/parity/linux/user_namespaces.rs` | 24 | 1 | Parity | `platform::filesystem::HostFilesystem` |
| `tests/parity/macos/libproc_pid_identity.rs` | 28 | 1 | Parity | `Integration` |
| `tests/parity/macos/ptmx_pty.rs` | 21 | 1 | Parity | `Integration` |
| `tests/parity/macos/rlimit_as_best_effort.rs` | 34 | 1 | Parity | `platform::resources::ResourceBudget` |
| `tests/parity/macos/seatbelt_profile_confinement.rs` | 51 | 3 | Parity | `Integration` |
| `tests/parity/negative/degraded_seatbelt_macos.rs` | 37 | 1 | Parity | `platform::capabilities::(CapabilityState, PlatformCapabil...` |
| `tests/parity/negative/unavailable_job_objects_windows.rs` | 34 | 1 | Parity | `platform::PlatformFamily` |
| `tests/parity/negative/unsupported_fd_limit_windows.rs` | 38 | 1 | Parity | `platform::PlatformFamily` |
| `tests/parity/negative/unsupported_filesystem_isolation_windows.rs` | 25 | 1 | Parity | `platform::PlatformFamily` |
| `tests/parity/negative/unsupported_network_isolation_windows.rs` | 18 | 1 | Parity | `platform::PlatformFamily` |
| `tests/parity/process_tree_termination.rs` | 297 | 9 | Parity | `platform::process as platform_process` |
| `tests/parity/resource_limits.rs` | 308 | 10 | Parity | `platform::resources::( ResourceBudget, apply_pre_exec_lim...` |
| `tests/parity/sandbox_fail_closed.rs` | 150 | 8 | Parity | `platform::capabilities::(Capability, CapabilityState, Pla...` |
| `tests/parity/shell_execution.rs` | 213 | 9 | Parity | `platform::shell as platform_shell` |
| `tests/parity/terminal_pty.rs` | 204 | 9 | Parity | `platform::terminal as platform_terminal` |
| `tests/parity/windows/acl_file_protection.rs` | 26 | 1 | Parity | `Integration` |
| `tests/parity/windows/cmd_powershell_quoting.rs` | 30 | 1 | Parity | `platform::windows::shell as wshell` |
| `tests/parity/windows/conpty_dimensions_resize.rs` | 38 | 1 | Parity | `platform::windows::conpty::(ConsoleSize, conpty_available)` |
| `tests/parity/windows/job_object_memory_limit.rs` | 40 | 1 | Parity | `platform::resources::ResourceBudget` |
| `tests/parity/windows/job_object_tree_termination.rs` | 44 | 1 | Parity | `platform::resources::ResourceBudget` |
| `tests/parity/windows/path_security_reparse_points.rs` | 62 | 2 | Parity | `platform::windows::path as winpath` |
| `tests/phase_01_events_ids_kernel.rs` | 359 | 12 | Integration | `events::(EventCategory, EventEnvelope, EventType)` |
| `tests/phase_01_persistence_streams_artifacts.rs` | 246 | 10 | Integration | `error::M31AError` |
| `tests/phase_01_state_machines.rs` | 419 | 14 | Integration | `state_machine::( AgentEvent, AgentState, MissionEvent, Mi...` |
| `tests/phase_02_intake_completion_recovery.rs` | 419 | 14 | Integration | `error::M31AError` |
| `tests/phase_02_service_bus_transactions.rs` | 525 | 12 | Integration | `events::bus::(BroadcastEventBus, EventBus, EventFilter)` |
| `tests/phase_03_autonomy_controller.rs` | 877 | 9 | Integration | `controller::AutonomyController` |
| `tests/phase_04_planning_authority.rs` | 149 | 2 | Architecture | `agent::model_policy::(ModelCaller, ModelProposal)` |
| `tests/phase_05_replan_reconciliation.rs` | 201 | 1 | Integration | `dag::materializer::TaskGraphMaterializer` |
| `tests/phase_05_resource_manager.rs` | 237 | 5 | Integration | `ids::(MissionId, TaskId)` |
| `tests/phase_05_scheduler_concurrency.rs` | 248 | 5 | Integration | `ids::(AgentId, MissionId)` |
| `tests/phase_05_task_dag_persistence.rs` | 265 | 4 | Integration | `dag::materializer::TaskGraphMaterializer` |
| `tests/phase_06_agent_runtime.rs` | 913 | 17 | Integration | `agent::envelope::(CapabilityIntersectionError, calculate_...` |
| `tests/phase_07_models_context_repo.rs` | 532 | 5 | Integration | `context::compiler::ProductionContextCompiler` |
| `tests/phase_08_capability_registry_seams.rs` | 443 | 5 | Integration | `capability::error::CapabilityError` |
| `tests/phase_08_execution_pipeline.rs` | 562 | 6 | Integration | `agent::runner::ActionRequest` |
| `tests/phase_08_process_jobs_supervisor.rs` | 274 | 6 | Integration | `ids::(AgentId, MissionId, TaskId)` |
| `tests/phase_08_tool_catalog_schemas.rs` | 404 | 8 | Integration | `agent::envelope::CapabilityEnvelope` |
| `tests/phase_09_interactive_approval_grants.rs` | 727 | 4 | Integration | `agent::runner::ActionRequest` |
| `tests/phase_09_policy_precedence_invariants.rs` | 741 | 11 | Integration | `agent::runner::ActionRequest` |
| `tests/phase_09_process_jobs_recovery.rs` | 662 | 6 | Integration | `ids::(AgentId, JobId, MissionId, TaskId)` |
| `tests/phase_09_sandbox_isolation_confinement.rs` | 309 | 5 | Integration | `sandbox::capabilities::SandboxCapabilities` |
| `tests/phase_10_checkpoints_crash_recovery.rs` | 956 | 7 | Integration | `checkpoint::crash_recovery::(CrashRecoveryClassification,...` |
| `tests/phase_10_failure_recovery_loop.rs` | 387 | 2 | Integration | `ids::(AgentId, MissionId, TaskId)` |
| `tests/phase_10_verification_hierarchy.rs` | 620 | 3 | Integration | `agent::envelope::CapabilityEnvelope` |
| `tests/phase_11_cli.rs` | 343 | 5 | Integration | `cli::(Cli, CliDispatcher, RuntimeCommand)` |
| `tests/phase_11_config.rs` | 354 | 4 | Integration | `config::(ConfigError, ConfigPrecedenceEngine, ConfigTier)` |
| `tests/phase_11_git.rs` | 622 | 5 | Integration | `git::(WorktreeConfig, WorktreeManager)` |
| `tests/phase_11_tui.rs` | 482 | 8 | Integration | `events::envelope::EventEnvelope` |
| `tests/phase_12_completion_reports.rs` | 859 | 6 | Integration | `ids::(AgentId, ArtifactId, CheckId, CheckpointId, EventId...` |
| `tests/phase_12_eval_harness.rs` | 146 | 10 | Integration | `eval::runner::EvalRunner` |
| `tests/phase_12_resource_budgets.rs` | 142 | 5 | Integration | `ids::(JobId, MissionId)` |
| `tests/phase_12_security_hardening.rs` | 513 | 10 | Integration | `capability::error::CapabilityError` |
| `tests/phase_12_skills_profiles.rs` | 248 | 6 | Integration | `config::merge::ConfigError` |
| `tests/phase_12_telemetry_correlation.rs` | 306 | 6 | Integration | `cli::args::(Cli, Commands, TelemetryArgs, TelemetryCommands)` |
| `tests/phase_13_ad007_dependency_guards.rs` | 337 | 15 | Integration | `Integration` |
| `tests/phase_13_cockpit_views.rs` | 194 | 3 | Integration | `interaction::action::ApplicationAction` |
| `tests/phase_13_framebuffer_snapshots.rs` | 155 | 6 | Integration | `tui::input::text_input::(InputMasking, TextInput)` |
| `tests/phase_13_onboarding_config.rs` | 353 | 3 | Integration | `config::provenance::(ConfigLayer, ConfigurationService, P...` |
| `tests/phase_13_pty_scenarios.rs` | 189 | 4 | Integration | `tui::guard::(TerminalGuard, install_panic_hook)` |
| `tests/phase_13_terminal_tokens.rs` | 150 | 3 | Integration | `tui::guard::(TerminalGuard, install_panic_hook)` |
| `tests/phase_13_visual_review.rs` | 99 | 3 | Integration | `tui::registry::(ViewId, ViewRegistry)` |
| `tests/phase_20_repository_intelligence.rs` | 562 | 6 | Integration | `capability::providers::repo_graph::RepositoryGraphProvider` |
| `tests/phase_21_context_engine.rs` | 661 | 16 | Integration | `context::compiler::ProductionContextCompiler` |
| `tests/phase_22_adaptive_planning.rs` | 505 | 38 | Integration | `kernel::plan::( CandidatePlanAssumption, PlanRevisionReco...` |
| `tests/phase_23_adversarial_mutation.rs` | 565 | 9 | Integration | `capability::providers::local_fs::LocalFileSystemProvider` |
| `tests/phase_23_code_modification_authority.rs` | 817 | 10 | Architecture | `capability::providers::local_fs::LocalFileSystemProvider` |
| `tests/phase_24_closed_loop_recovery.rs` | 758 | 12 | Integration | `capability::providers::local_fs::LocalFileSystemProvider` |
| `tests/phase_25_engineering_memory.rs` | 832 | 12 | Integration | `context::compiler::ProductionContextCompiler` |
| `tests/phase_26_autonomous_intent.rs` | 683 | 19 | Integration | `ids::MissionId` |
| `tests/phase_27_5_extension_seams.rs` | 959 | 9 | Integration | `agent::model_policy::(ModelCaller, ModelProposal)` |
| `tests/phase_27_declarative_boundary.rs` | 679 | 13 | Integration | `agent::model_policy::(ModelCaller, ModelProposal)` |
| `tests/phase_29_5_real_model.rs` | 1396 | 1 | Integration | `kernel::seams::planner::(PlanRequest, PlanService, Upstre...` |
| `tests/phase_29_6_gap_a_research_ownership.rs` | 305 | 6 | Integration | `agent::registry::RoleRegistry` |
| `tests/phase_29_6_gap_b_recovery_circuit_breaker.rs` | 412 | 8 | Integration | `ids::(MissionId, TaskId)` |
| `tests/phase_29_6_gap_c_discovery_unknowns.rs` | 327 | 5 | Integration | `kernel::seams::planner::UpstreamPlanContext` |
| `tests/phase_29_6_gap_d_planning_retry.rs` | 288 | 7 | Integration | `agent::model_policy::(ModelCaller, ModelProposal)` |
| `tests/phase_29_autonomous_engineering.rs` | 1093 | 13 | Integration | `agent::model_policy::(ModelCaller, ModelProposal, ModelTo...` |
| `tests/phase_30_agentic_core.rs` | 890 | 10 | Integration | `agent::engine::(AgentEngine, AgentEngineState, AgentTurnO...` |
| `tests/phase_31_agent_convergence.rs` | 676 | 9 | Integration | `agent::model_policy::ModelProposal` |
| `tests/phase_32_intent_understanding.rs` | 1180 | 30 | Integration | `agent::AgentTurnOutcome` |
| `tests/phase_33_adaptive_execution.rs` | 1021 | 12 | Integration | `agent::adaptive::( AdaptiveReplanRequest, ExecutionFailur...` |
| `tests/phase_35_lifecycle_governance.rs` | 795 | 9 | Integration | `interaction::action::ApplicationAction` |
| `tests/phase_36_1_runtime_truth.rs` | 696 | 8 | Integration | `controller::AutonomyController` |
| `tests/phase_36_3_truth_boundary.rs` | 934 | 28 | Integration | `agent::intent::FactOrigin` |
| `tests/phase_36_4_tui_governance.rs` | 741 | 18 | Integration | `events::envelope::EventEnvelope` |
| `tests/phase_36_5_wiring_convergence.rs` | 728 | 16 | Integration | `capability::registry::CapabilityRegistry` |
| `tests/phase_36_6_tui_truth_projection.rs` | 480 | 10 | Integration | `events::envelope::EventEnvelope` |
| `tests/phase_36_runtime_handoff.rs` | 892 | 23 | Integration | `interaction::action::ApplicationAction` |
| `tests/phase_37_authority_convergence.rs` | 580 | 14 | Architecture | `events::bus::(EventBus, EventFilter)` |
| `tests/phase_39_evidence_observability.rs` | 527 | 11 | Integration | `agent::registry::RoleRegistry` |
| `tests/phase_40_governed_execution.rs` | 2317 | 42 | Integration | `agent::ProductionWorkerDispatcher` |
| `tests/phase_41_integrity.rs` | 1770 | 42 | Integration | `agent::model_policy::(ModelCaller, RoutedModelCaller)` |
| `tests/phase_42_production_proof.rs` | 1622 | 11 | Integration | `agent::model_policy::ModelCaller` |
| `tests/phase_43_reliability.rs` | 1484 | 35 | Integration | `agent::model_policy::(ModelCaller, RoutedModelCaller)` |
| `tests/phase_44_security_closure.rs` | 1568 | 32 | Integration | `capability::providers::LocalFileSystemProvider` |
| `tests/phase_45_release_validation.rs` | 696 | 19 | Integration | `events::bus::BroadcastEventBus` |
| `tests/phase_46_autonomous_reliability_remediation.rs` | 650 | 13 | Integration | `capability::providers::LocalFileSystemProvider` |
| `tests/phase_remediation_scheduler.rs` | 600 | 7 | Integration | `events::EventBus` |
| `tests/phase_remediation_workspace_detection.rs` | 265 | 15 | Integration | `workflow::genesis::( GenesisError, GenesisMode, WorkflowT...` |
| `tests/planning_prompt_consolidation.rs` | 1250 | 19 | Integration | `agent::AgentRole` |
| `tests/platform.rs` | 16 | 0 | Platform | `Integration` |
| `tests/platform/common/capabilities.rs` | 263 | 18 | Platform | `Integration` |
| `tests/platform/linux/mod.rs` | 137 | 13 | Platform | `platform::resources::(ResourceBudget, apply_pre_exec_limits)` |
| `tests/platform/macos/mod.rs` | 142 | 14 | Platform | `platform::resources::(ResourceBudget, apply_pre_exec_limits)` |
| `tests/platform/windows/mod.rs` | 290 | 23 | Platform | `platform::resources::ResourceBudget` |
| `tests/production_comment_hygiene.rs` | 122 | 1 | Integration | `Integration` |
| `tests/production_four_defects_remediation.rs` | 557 | 12 | Integration | `config::ResolvedConfiguration` |
| `tests/production_runtime_authority_identity.rs` | 502 | 11 | Architecture | `events::EventBus` |
| `tests/prompt_reachability.rs` | 674 | 13 | Integration | `agent::model_policy::(ModelCaller, ModelProposal)` |
| `tests/promptos_phase2_builtins.rs` | 311 | 4 | Integration | `prompt::builtins::load_all_builtin_contracts` |
| `tests/promptos_phase3_compiler.rs` | 774 | 20 | Integration | `prompt::( CompilationOptions, DefaultPromptCompiler, Miss...` |
| `tests/promptos_phase4_cutover.rs` | 333 | 6 | Integration | `agent::profile::AgentProfile` |
| `tests/promptos_phase5_verification.rs` | 899 | 24 | Integration | `ids::(MissionId, TaskId)` |
| `tests/promptos_phase6_adaptation.rs` | 813 | 20 | Integration | `model::router::resolver::(ModelCandidate, ModelTier)` |
| `tests/promptos_phase7_provenance.rs` | 773 | 10 | Integration | `agent::AgentStepRecord` |
| `tests/promptos_phase8_workspace.rs` | 926 | 13 | Integration | `kernel::seams::policy::PolicyGate` |
| `tests/promptos_v2_behavioral.rs` | 342 | 11 | Integration | `agent::profile::AgentProfile` |
| `tests/provider_capability_alignment.rs` | 543 | 13 | Integration | `agent::model_policy::(ModelCaller, RoutedModelCaller)` |
| `tests/provider_instrumentation_deterministic.rs` | 367 | 7 | Integration | `model::ModelProvider` |
| `tests/remediation_autonomy_assembly.rs` | 224 | 5 | Integration | `controller::AutonomyController` |
| `tests/remediation_bug_fixes.rs` | 2330 | 35 | Integration | `agent::action::(ActionParseError, ActionUserOption, Agent...` |
| `tests/remediation_cli_binary.rs` | 166 | 6 | Integration | `Integration` |
| `tests/remediation_cli_persistence.rs` | 261 | 2 | Integration | `cli::dispatch::(CliDispatcher, RuntimeCommand)` |
| `tests/remediation_recovery_hardening.rs` | 270 | 3 | Integration | `controller::AutonomyController` |
| `tests/remediation_repository_discovery.rs` | 184 | 4 | Integration | `context::compiler::ProductionContextCompiler` |
| `tests/remediation_runtime_convergence.rs` | 1325 | 21 | Integration | `capability::family::CapabilityFamily` |
| `tests/remediation_runtime_model_promptos.rs` | 541 | 14 | Integration | `config::provider_registry::PRODUCTION_PROVIDER_ID` |
| `tests/remediation_seam_hardening.rs` | 296 | 4 | Integration | `controller::AutonomyController` |
| `tests/remediation_single_authority.rs` | 651 | 29 | Architecture | `config::profile::ProfileResolver` |
| `tests/remediation_targeted_verification.rs` | 552 | 9 | Integration | `agent::runner::compute_action_fingerprint` |
| `tests/remediation_tui_approval.rs` | 195 | 3 | Integration | `cli::dispatch::(CliDispatcher, RuntimeCommand)` |
| `tests/remediation_tui_core_integration.rs` | 1773 | 23 | Integration | `config::canonical::DEFAULT_TUI_MAX_EVENTS_PER_TICK` |
| `tests/request_routing_intent_enforcement.rs` | 1298 | 18 | Integration | `agent::model_policy::(ModelCaller, ModelProposal)` |
| `tests/sandbox_wiring_test.rs` | 140 | 3 | Integration | `capability::error::CapabilityError` |
| `tests/second_stage_remediation.rs` | 2933 | 66 | Integration | `agent::adaptive::UNKNOWN_FINGERPRINT_PREFIX` |
| `tests/security_p0_credential_boundary.rs` | 314 | 13 | Integration | `config::env::SafeEnvironmentStatus` |
| `tests/security_p0_endpoint_trust.rs` | 258 | 10 | Integration | `config::resolved::ResolvedConfiguration` |
| `tests/security_p0_governed_verification.rs` | 171 | 8 | Integration | `ids::(MissionId, TaskId)` |
| `tests/security_p0_output_classification.rs` | 191 | 6 | Integration | `ids::ArtifactId` |
| `tests/security_p0_process_boundary.rs` | 795 | 14 | Integration | `capability::error::CapabilityError` |
| `tests/security_p0_prompt_trust.rs` | 174 | 4 | Integration | `prompt::MissionStage` |
| `tests/security_p0_protected_paths.rs` | 924 | 13 | Integration | `capability::error::CapabilityError` |
| `tests/security_p1_dns_binding.rs` | 157 | 7 | Integration | `policy::destination::(NetworkDestinationPolicy, Validatin...` |
| `tests/session_interaction_consolidation.rs` | 1123 | 21 | Integration | `events::bus::(EventBus, EventFilter)` |
| `tests/storage_architecture.rs` | 602 | 12 | Architecture | `config::resolved::ResolvedConfiguration` |
| `tests/support/autonomous.rs` | 369 | 0 | Integration | `agent::engine::AgentEngineState` |
| `tests/support/credentials.rs` | 297 | 6 | Integration | `Integration` |
| `tests/support/live_inventory.rs` | 410 | 0 | Live Model | `Integration` |
| `tests/support/mock_provider.rs` | 300 | 0 | Integration | `model::provider::(BoxStreamChunk, ModelProvider)` |
| `tests/support/mod.rs` | 15 | 0 | Integration | `Integration` |
| `tests/support/model_caller.rs` | 251 | 0 | Integration | `agent::model_policy::(ModelCaller, ModelProposal)` |
| `tests/support/policy.rs` | 20 | 0 | Integration | `kernel::seams::policy::( PolicyDecision, PolicyError, Pol...` |
| `tests/support/real_model.rs` | 461 | 0 | Integration | `agent::model_policy::RoutedModelCaller` |
| `tests/support/runtime_harness.rs` | 229 | 0 | Integration | `events::bus::(BroadcastEventBus, EventBus, EventFilter)` |
| `tests/tui_3_live_cockpit.rs` | 515 | 7 | Integration | `interaction::events::InteractionEvent` |
| `tests/tui_architecture_principles.rs` | 309 | 10 | Architecture | `tui::navigation::ScreenId` |
| `tests/tui_autocomplete_repair.rs` | 1289 | 53 | Integration | `interaction::action::ApplicationAction` |
| `tests/tui_canonical_reduction.rs` | 440 | 12 | Integration | `ids::MissionId` |
| `tests/tui_first_frame_regression.rs` | 608 | 18 | Integration | `events::bus::(BroadcastEventBus, EventBus)` |
| `tests/tui_layout_and_interaction_correctness.rs` | 492 | 10 | Integration | `tui::TuiApplication` |
| `tests/tui_runtime_integration_remediation.rs` | 756 | 10 | Integration | `events::bus::(BroadcastEventBus, EventBus)` |
| `tests/tui_runtime_state_repair.rs` | 867 | 18 | Integration | `interaction::action::ApplicationAction` |
| `tests/tui_ux_reconstruction.rs` | 368 | 10 | Integration | `tui::TuiApplication` |
| `tests/tui_ux_remediation_suite.rs` | 2693 | 69 | Integration | `events::envelope::EventEnvelope` |
| `tests/tui_wiring_integrity_remediation.rs` | 825 | 14 | Integration | `cli::dispatch::RuntimeCommand` |
| `tests/tui_workspace_v2.rs` | 567 | 8 | Integration | `tui::TuiApplication` |
| `tests/user_defined_commands.rs` | 2165 | 23 | Integration | `events::bus::BroadcastEventBus` |
| `tests/user_freedom_configuration.rs` | 261 | 6 | Integration | `config::resolved::ResolvedConfiguration` |
| `tests/wiring_remediation_regression.rs` | 567 | 9 | Integration | `config::ResolvedConfiguration` |
| `tests/workflow_authority_convergence.rs` | 603 | 8 | Architecture | `agent::model_policy::(ModelCaller, ModelProposal)` |
| `tests/workflow_compiler.rs` | 203 | 5 | Integration | `prompt::InMemoryPromptCatalog` |
| `tests/workflow_domain.rs` | 548 | 14 | Integration | `ids::(WorkflowRunId, WorkflowStepRunId)` |
| `tests/workflow_e2e_canonical.rs` | 263 | 1 | Integration | `agent::model_policy::(ModelCaller, ModelProposal)` |
| `tests/workflow_engine.rs` | 810 | 7 | Integration | `agent::model_policy::(ModelCaller, ModelProposal)` |
| `tests/workflow_engine_failure.rs` | 542 | 6 | Integration | `agent::model_policy::(ModelCaller, ModelProposal)` |
| `tests/workflow_engine_recovery.rs` | 764 | 6 | Integration | `agent::model_policy::(ModelCaller, ModelProposal)` |
| `tests/workflow_execution_spine.rs` | 1239 | 11 | Integration | `agent::model_policy::(ModelCaller, ModelProposal, ModelTo...` |
| `tests/workflow_lowering.rs` | 751 | 20 | Integration | `ids::MissionId` |
| `tests/workflow_manifest.rs` | 372 | 11 | Integration | `state_machine::agent::AgentRole` |
| `tests/workflow_persistence.rs` | 574 | 9 | Integration | `ids::(MissionId, WorkflowRunId)` |
| `tests/workflow_prompts.rs` | 497 | 10 | Integration | `context::priority::ContextPriority` |
| `tests/workflow_quality_gates.rs` | 344 | 7 | Integration | `ids::(WorkflowRunId, WorkflowStepRunId)` |
| `tests/workspace_instance_lifecycle.rs` | 730 | 23 | Integration | `init::( InitError, InitManager, InitState, OnboardingReas...` |