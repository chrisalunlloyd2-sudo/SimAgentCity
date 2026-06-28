# SimAgentCity

> SimAgentCity — part of the Viper RAID-0 workstation system.

*Auto-generated 2026-06-27 20:20 from source — branch `main`, 45 Python modules, 1243 other files.*

## Architecture

```
  .director_payload.md
  BUILD_LOG.txt
  Blueprint.md
  CHANGELOG.md
  ENTERPRISE_MANIFESTO.md
  GRAND_MASTER_PLAN.md
  LAUNCH_CITY.bat
  PROJECT_LOG.md
  PROJECT_MAP.txt
  PULSE_HEARTBEAT.txt
  README.md
  RUN_STRESS_TEST.bat
  assets/
    genesis_prime_core.png
    robot_nurse_doctor.png
    sim_agent_city_glow.png
  backend/
    __init__.py
    main.py
    core/
      __init__.py
      agent_container.py
      agent_registrar.py
      algebraic_governance.py
      chrono_layer.py
      critic_node.py
      crypto_ledger.py
      file_watcher.py
      fitness_engine.py
      fuzz_engine.py
      hive_mind_router.py
      llm_client.py
    data/
      ai_attributes.json
  briefcase/
    INITIAL_BOOT.json
    symphony_state.json
    genesis_logs/
      genesis_step_1.json
      genesis_step_10.json
      genesis_step_100.json
      genesis_step_1001.json
      genesis_step_1002.json
      genesis_step_1003.json
      genesis_step_1004.json
      genesis_step_1005.json
      genesis_step_1006.json
      genesis_step_1007.json
      genesis_step_1008.json
      genesis_step_1009.json
  city_workspace/
    genesis_test.txt
    tower_block.txt
  docs/
    AXIOMATIC_STATE.md
    EVOLUTIONARY_LOG.md
    GUARDRAILS.md
    PROGRESS.md
    RING_MANIFESTO.md
    TO_K_BLUEPRINT.md
    architecture.md
    technical_bible.md
  frontend/
    index.html
    css/
      style.css
    js/
      bridge.js
      engine.js
      gui.js
      input.js
      ...
```

## Dependencies

External packages imported by this project:

`backend`, `core`, `fastapi`, `mmap`, `psutil`, `py_compile`, `pydantic`, `requests`, `tools`, `uvicorn`, `watchdog`, `webbrowser`, `websockets`, `winreg`

## How to run

Executable entry points (have a `__main__` block):

- `python backend/core/agent_container.py`
- `python backend/core/agent_registrar.py`
- `python backend/core/crypto_ledger.py`
- `python backend/core/file_watcher.py`
- `python backend/core/hive_mind_router.py`
- `python backend/core/llm_client.py`
- `python backend/core/network_researcher.py`
- `python backend/core/orchestrator.py`
- `python backend/core/os_bridge.py`
- `python backend/core/registry_bridge.py`
- `python backend/core/ring_orchestrator.py`
- `python backend/core/road_builder.py`

## Modules

### `backend/core/agent_container.py`

- **class `AgentContainerManager`**
  - methods: `spawn_agent_home`, `mount_volume`, `get_agent_storage_stats`

### `backend/core/agent_registrar.py`

- **class `AgentRegistrar`**
  - methods: `register_agent`, `get_registered_agents`

### `backend/core/algebraic_governance.py`

- **class `AlgebraicGovernance`** — Uses wave-based harmonics to throttle and prioritize tasks.
  - methods: `calculate_throttle`, `prioritize`

### `backend/core/chrono_layer.py`

- **class `ChronoLayer`** — Manages system ticks, turns, and epochs for voting governance.
  - methods: `get_chronos_state`, `_get_phase`

### `backend/core/critic_node.py`

- **class `CriticNode`** — Phase 13: Structural and Logic Criticism Node.
  - methods: `analyze`

### `backend/core/crypto_ledger.py`

- **class `Block`**
  - methods: `calculate_hash`, `mine_block`
- **class `CryptoLedger`**
  - methods: `load_chain`, `save_chain`, `create_genesis_block`, `get_latest_block`, `add_transaction`, `get_balance`

### `backend/core/file_watcher.py`

- **class `CityFileHandler`**
  - methods: `on_modified`, `on_created`, `on_deleted`, `on_moved`
- **class `CityFileWatcher`** — Step 51-75: Real-time file system watcher to eliminate polling.
  - methods: `start`, `stop`

### `backend/core/fitness_engine.py`

- **class `FitnessEngine`** — Calculates Darwinian fitness score for agent proposals.
  - methods: `calculate`
- **class `ScientificConduct`** — Enforces pre-commit testing and log creation.
  - methods: `conduct_audit`

### `backend/core/fuzz_engine.py`

- **class `FuzzEngine`** — Generates chaotic noise for agent input mutation.
  - methods: `mutate`
- **class `ShadowExecutor`** — Runs code in a cloned ghost-environment replica.
  - methods: `setup_ghost`, `execute`

### `backend/core/hive_mind_router.py`

- **class `HiveMindRouter`**
  - methods: `route_task`, `_generate_fallback`, `generate_chat_bubble`

### `backend/core/llm_client.py`

- **class `LLMClient`**
  - methods: `ping`, `process_file_task`

### `backend/core/message_bus.py`

- **class `SymphonyBus`** — Centralized, thread-safe asynchronous MessageBus.
  - methods: `connect`, `disconnect`, `broadcast`

### `backend/core/network_researcher.py`

- **class `NetworkResearchDaemon`** — SimAgentCity Advanced Crawler & Network Auditor.
  - methods: `run_network_audit`, `verify_clawhub_compliance`, `execute_and_seal_research`

### `backend/core/orchestrator.py`

- **class `AgentCityOrchestrator`**
  - methods: `_on_fs_event`, `_clear_transaction`, `run_miner_loop`, `run_processor_loop`, `run_shipper_loop`, `_run_heartbeat`, `assign_task`, `_process_next`, `_execute_agent_flow`

### `backend/core/os_bridge.py`

- **class `OSBridge`**
  - methods: `move_file`, `update_registry_mock`, `get_file_tree`

### `backend/core/permutation_tester.py`

- **class `ConstraintPermutationTester`** — Systematically tests all permutations within logic boundaries.
  - methods: `derive_boundaries`, `run_exhaustive`

### `backend/core/registry_bridge.py`

- **class `RegistryBridge`**
  - methods: `get_keys`, `read_value`, `write_value`, `delete_value`

### `backend/core/ring_orchestrator.py`

- **class `RingOrchestrator`**
  - methods: `submit_task`, `_log_to_chat`, `run_continuous`

### `backend/core/road_builder.py`

- **class `RoadBuilder`** — Step 151-175: Transit Mapping
  - methods: `build_road`, `protocol_dispatch`, `bulldoze`

### `backend/core/sbi_monitor.py`

- **class `SBIMonitor`**
  - methods: `log_movement`, `interpolate_behavior`, `get_interpol_status`

### `backend/core/script_sync.py`

- **class `ScriptLibrarySync`** — Synchronizes successful briefcase artifacts to ViperNotes.
  - methods: `sync`, `_export`

### `backend/core/self_corrector.py`

- **class `AgentSelfCorrector`**
  - methods: `analyze_failure`, `apply_mutation`

### `backend/core/symphony_sync.py`

- **class `SymphonySync`** — Orchestrator for autonomous database correlation.
  - methods: `run_symphony`

### `backend/core/telemetry_monitor.py`

- **class `MEMORYSTATUSEX`**
- **class `MetabolismMonitor`**
  - methods: `cleanup_processes`
- **class `TelemetryMonitor`**
  - methods: `get_memory_stats`, `get_hardware_bus`, `get_city_vitals`

### `backend/core/tester_node.py`

- **class `TesterNode`** — Phase 16/17: Hyper-Dimensional Stress & Exhaustive Permutation Testing.
  - methods: `run_proposal`

### `backend/core/tok_memory_arena.py`

- **class `ToKMemoryArena`** — Phase 1: Native Memory Arena for Radix-Trie ToK.
  - methods: `write_node`, `read_node`

### `backend/core/trust_layer.py`

- **class `TrustLayer`**
  - methods: `mint_trust`, `verify_identity`, `save_graph`, `load_graph`

### `backend/core/voting_engine.py`

- **class `VotingEngine`** — Manages epoch-based structured ballot casting.
  - methods: `cast_vote`

### `backend/core/zoning_manager.py`

- **class `ZoningManager`**
  - methods: `set_zone`, `get_zone`, `save_zones`, `load_zones`, `get_all_zones`

### `backend/main.py`

- `get_chrono_status()` — Returns the current voting epoch, turn, and phase.
- `post_chat(req)`
- `get_chat()`
- `get_heartbeat()`
- `get_metropolis_state()`
- `post_metropolis_state()`
- `get_network_status()`
- `get_physical_status()`
- `get_hardware()`
- `get_evolution()`
- `get_hardware_telemetry()`
- `mint_currency(req)`
- `get_ledger_status()`

### `cli_wrapper.py`

- `run_server(port)`
- `auto_launch_browser(port)` — Automatically closes existing SimAgentCity windows and launches a fresh one.
- `main()`

### `genesis_pyramid.py`

- **class `GenesisOrchestrator`**
  - methods: `log_move`, `execute_batch`

### `lean_controller.py`

- **class `LeanController`**
  - methods: `throttle`, `run`

### `master_controller.py`

- **class `TaskPool`** — Pre-allocated pool for task objects to avoid dynamic allocation.
  - methods: `get_task`
- **class `ActorObserverController`** — Implements the Actor/Observer split and GITAUTOSHIP pattern.
  - methods: `_observer_log`, `_git_autoship`, `run`, `run`

### `master_verification.py`

- **class `MasterVerifier`** — Verifies full system integrity.
  - methods: `verify`

### `orchestrator_pyramid.py`

- **class `Actor`** — The task executor.
  - methods: `execute`
- **class `Observer`** — The telemetry and logging layer.
  - methods: `observe`
- **class `PyramidOrchestrator`**
  - methods: `run_layer`

### `stability_watchdog.py`

- **class `StabilityWatchdog`** — Proactively monitors backend and controller PIDs.
  - methods: `check_and_heal`, `is_running`

### `swarm_healing.py`

- **class `SwarmHealer`** — Proactively heals network and process deadlocks.
  - methods: `diagnose_and_heal`, `heal_bus`

### `system_health_tester.py`

- **class `SystemHealthTester`**
  - methods: `test_cycle`, `restart_backend`, `run`

### `tools/agent_registrar_tool.py`

- `main()`

### `tools/task_mgr_mini.py`

- `get_process_summary()` — AI-Compatible Task Manager: Returns lightweight process list for agent analysis.
- `kill_process(pid)` — Step 176-200: Demolish a process sprite to kill the OS process.

### `websocket_tester.py`

- `test_ws()`

## Public API index

| Module | Function | Signature |
|--------|----------|-----------|
| `agent_registrar_tool` | `main` | `main()` |
| `cli_wrapper` | `auto_launch_browser` | `auto_launch_browser(port)` |
| `cli_wrapper` | `main` | `main()` |
| `cli_wrapper` | `run_server` | `run_server(port)` |
| `main` | `get_chat` | `get_chat()` |
| `main` | `get_chrono_status` | `get_chrono_status()` |
| `main` | `get_evolution` | `get_evolution()` |
| `main` | `get_hardware` | `get_hardware()` |
| `main` | `get_hardware_telemetry` | `get_hardware_telemetry()` |
| `main` | `get_heartbeat` | `get_heartbeat()` |
| `main` | `get_ledger_status` | `get_ledger_status()` |
| `main` | `get_metropolis_state` | `get_metropolis_state()` |
| `main` | `get_network_status` | `get_network_status()` |
| `main` | `get_physical_status` | `get_physical_status()` |
| `main` | `mint_currency` | `mint_currency(req)` |
| `main` | `post_chat` | `post_chat(req)` |
| `main` | `post_metropolis_state` | `post_metropolis_state()` |
| `task_mgr_mini` | `get_process_summary` | `get_process_summary()` |
| `task_mgr_mini` | `kill_process` | `kill_process(pid)` |
| `websocket_tester` | `test_ws` | `test_ws()` |

## Status

- Branch: `main`
- Last commit: 2026-06-27 01:11:41 -0600
- File types: .json ×1206, .md ×16, .txt ×6, .bat ×5, .js ×4, .png ×3, .log ×1, .html ×1

### Recent commits
```
86713fc [Moe autonomous] SimAgentCity 2026-06-27 01:11
68f1d0f [Moe autonomous] SimAgentCity 2026-06-20 10:34
eab0622 [Moe autonomous] SimAgentCity 2026-06-20 09:18
b1b4062 [Moe autonomous] SimAgentCity 2026-06-20 00:26
46ef5ed Automated Add-Only Sync
c27e419 System: Integrate new premium visual assets, deterministic model attributes, and network researcher daemon. TIMESTAMP: 2026-06-01T01:05:00.000Z PROJECT_ID: SimAgentCity-v1.3 AGENT_ID: Antigravity-CLI-Architect
7b9f826 System: Resolve README.md merge conflicts, successfully rebasing and merging upstream restoration guidelines with local stashed features. TIMESTAMP: 2026-05-31T22:36:00.000Z PROJECT_ID: SimAgentCity-v1.3 AGENT_ID: Antigravity-CLI-Architect
2d6edc4 System: Merge and integrate Phase II stability upgrades, daily build validator, and active agent governance resolution. TIMESTAMP: 2026-05-31T19:25:00.000Z PROJECT_ID: SimAgentCity-v1.3 AGENT_ID: Antigravity-CLI-Architect
```

---
*README generated by `readme_generator.py` (Viper). Deterministic — derived from source, not LLM prose.*