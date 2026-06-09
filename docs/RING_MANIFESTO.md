# BOT-DRIVEN RECURSIVE IMPROVEMENT RING (SimAgentCity)

## 🎯 MISSION
To automate the lifecycle of SimAgentCity development, maintenance, and optimization through a recursive, multi-agent SLM ring. Zero human intervention. Fully autonomous self-correction, testing, and scaling.

## 🤖 ROLE DEFINITIONS (Phase 02)
- **PROPOSER (qwen2.5:0.5b):** Generates initial code proposals based on Task schema. Output: `{"attemptId": "...", "code": "...", "rationale": "..."}`
- **CRITIC (h2o-danube3:4b):** Reviews proposals for security, style, and logic issues. Output: `{"issue": "...", "location": "...", "severity": "CRITICAL|HIGH|MEDIUM|LOW"}`
- **TESTER (Local Python Sandbox):** Executes unit/integration tests. Output: `{"pass_rate": 0.0, "failures": [], "logs_digest": "..."}`
- **ARBITER (mistral):** Evaluates attempts based on scores and critiques. Output: `{"decision": "ACCEPT|RECURSE|EXPLORE_ALT", "winnerId": "..."}`

## 📐 TASK SCHEMA (Phase 03)
```json
{
  "taskId": "string",
  "goal": "string",
  "constraints": {
    "language": "python|js|css",
    "safety": "strict",
    "latency_max": "integer"
  },
  "context": "string"
}
```

## 🕸️ TOPOLOGY (Phase 04)
1. **Task Queue** → Proposer (Fan-out)
2. Proposer → Tester
3. Tester + Critic → Arbiter
4. Arbiter → [ACCEPT → Registry/Deploy] OR [RECURSE → Proposer] OR [EXPLORE_ALT → Proposer]

*TIMESTAMP: 2026-06-07T16:30:00Z*
*AGENT_ID: Gemini-CLI-Architect*
