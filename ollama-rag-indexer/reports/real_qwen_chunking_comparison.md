# Chunking Strategy Comparison

Generated at: `2026-06-30T09:13:03Z`
Search mode: `dense`

## Chunk Statistics

| Strategy | Chunks | Avg chars | Min | Max | Section coverage | Backend |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| fixed | 391 | 1144.45 | 238 | 1199 | 1.0 | faiss |
| structural | 458 | 875.53 | 13 | 1799 | 1.0 | faiss |

## Retrieval Metrics

| Strategy | Queries | hit@1 | hit@3 | hit@5 | section@3 | MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fixed | 12 | 0.9167 | 1.0 | 1.0 | 1.0 | 0.9583 |
| structural | 12 | 0.8333 | 0.9167 | 1.0 | 0.8333 | 0.8958 |

## Query Details

### fixed

- `How does the Telegram bot connect to MCP servers at runtime?` -> source rank: `1`, section rank: `1`
  - top1: `tg-agent/README.md` / `tg-agent` score `0.8563` dense `0.8563` lexical `0.0`
- `Which Rust module implements MCP client communication and tool calls?` -> source rank: `1`, section rank: `2`
  - top1: `tg-agent/tests/live_connect.rs` / `file prelude` score `0.7231` dense `0.7231` lexical `0.0`
- `Where is the dynamic trip-planning swarm described or implemented?` -> source rank: `1`, section rank: `1`
  - top1: `tg-agent/src/agent/flow.rs` / `function agent_model_env_key` score `0.7474` dense `0.7474` lexical `0.0`
- `How are connected servers and user sessions persisted across restarts?` -> source rank: `1`, section rank: `2`
  - top1: `tg-agent/src/state.rs` / `impl BotState` score `0.5642` dense `0.5642` lexical `0.0`
- `Where does the bot build prompts with profile, memory, and tool context?` -> source rank: `1`, section rank: `2`
  - top1: `tg-agent/src/agent/prompt.rs` / `file prelude` score `0.7324` dense `0.7324` lexical `0.0`
- `Which test covers the live trip planning flow?` -> source rank: `1`, section rank: `1`
  - top1: `tg-agent/tests/live_orchestrator.rs` / `function trip_swarm_clarifies_then_plans` score `0.7429` dense `0.7429` lexical `0.0`
- `What Open-Meteo MCP tools are available for forecasts and weather comparison?` -> source rank: `1`, section rank: `1`
  - top1: `open-meteo-mcp/README.md` / `Weather data` score `0.8671` dense `0.8671` lexical `0.0`
- `Where is weather quality scoring for city comparison implemented?` -> source rank: `1`, section rank: `3`
  - top1: `open-meteo-mcp/src/tools/weather-logic.ts` / `interface Profile` score `0.6626` dense `0.6626` lexical `0.0`
- `Which TypeScript tool implements compare_weather_cities or regional weather analysis?` -> source rank: `1`, section rank: `3`
  - top1: `open-meteo-mcp/README.md` / `Weather data` score `0.742` dense `0.742` lexical `0.0`
- `Where are scheduled weather jobs created, listed, summarized, and cancelled?` -> source rank: `1`, section rank: `1`
  - top1: `open-meteo-mcp/src/tools/schedule.ts` / `function registerScheduleTools` score `0.713` dense `0.713` lexical `0.0`
- `Which code fetches weather forecast data from Open-Meteo APIs?` -> source rank: `1`, section rank: `2`
  - top1: `open-meteo-mcp/README.md` / `open-meteo-mcp` score `0.7706` dense `0.7706` lexical `0.0`
- `Where is geocoding for city names implemented in the weather MCP server?` -> source rank: `2`, section rank: `3`
  - top1: `tg-agent/src/agent/prompt.rs` / `file prelude` score `0.6544` dense `0.6544` lexical `0.0`

### structural

- `How does the Telegram bot connect to MCP servers at runtime?` -> source rank: `1`, section rank: `1`
  - top1: `tg-agent/README.md` / `tg-agent` score `0.8641` dense `0.8641` lexical `0.0`
- `Which Rust module implements MCP client communication and tool calls?` -> source rank: `1`, section rank: `1`
  - top1: `tg-agent/src/mcp_client.rs` / `struct McpClient` score `0.744` dense `0.744` lexical `0.0`
- `Where is the dynamic trip-planning swarm described or implemented?` -> source rank: `1`, section rank: `1`
  - top1: `tg-agent/src/agent/flow.rs` / `function agent_model_env_key` score `0.7515` dense `0.7515` lexical `0.0`
- `How are connected servers and user sessions persisted across restarts?` -> source rank: `4`, section rank: `1`
  - top1: `tg-agent/tests/live_connect.rs` / `function registry_keeps_connection_across_calls` score `0.6384` dense `0.6384` lexical `0.0`
- `Where does the bot build prompts with profile, memory, and tool context?` -> source rank: `1`, section rank: `5`
  - top1: `tg-agent/src/agent/prompt.rs` / `file prelude` score `0.7565` dense `0.7565` lexical `0.0`
- `Which test covers the live trip planning flow?` -> source rank: `1`, section rank: `1`
  - top1: `tg-agent/tests/live_orchestrator.rs` / `function trip_swarm_clarifies_then_plans` score `0.7338` dense `0.7338` lexical `0.0`
- `What Open-Meteo MCP tools are available for forecasts and weather comparison?` -> source rank: `1`, section rank: `1`
  - top1: `open-meteo-mcp/README.md` / `Weather comparison` score `0.8959` dense `0.8959` lexical `0.0`
- `Where is weather quality scoring for city comparison implemented?` -> source rank: `2`, section rank: `2`
  - top1: `open-meteo-mcp/README.md` / `Weather comparison` score `0.7266` dense `0.7266` lexical `0.0`
- `Which TypeScript tool implements compare_weather_cities or regional weather analysis?` -> source rank: `1`, section rank: `1`
  - top1: `open-meteo-mcp/README.md` / `Weather comparison` score `0.7779` dense `0.7779` lexical `0.0`
- `Where are scheduled weather jobs created, listed, summarized, and cancelled?` -> source rank: `1`, section rank: `1`
  - top1: `open-meteo-mcp/README.md` / `Scheduled collection` score `0.7795` dense `0.7795` lexical `0.0`
- `Which code fetches weather forecast data from Open-Meteo APIs?` -> source rank: `1`, section rank: `None`
  - top1: `open-meteo-mcp/README.md` / `open-meteo-mcp` score `0.8472` dense `0.8472` lexical `0.0`
- `Where is geocoding for city names implemented in the weather MCP server?` -> source rank: `1`, section rank: `1`
  - top1: `open-meteo-mcp/src/tools/geocoding.ts` / `function registerGeocoding` score `0.7375` dense `0.7375` lexical `0.0`

## Interpretation

- Fixed chunking is expected to produce more uniform chunk sizes and predictable overlap.
- Structural chunking is expected to preserve headings, pages, functions, and sections more often.
- Prefer the strategy with stronger retrieval metrics unless its chunk sizes are too uneven for the target context window.
