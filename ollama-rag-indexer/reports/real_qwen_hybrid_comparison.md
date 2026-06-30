# Chunking Strategy Comparison

Generated at: `2026-06-30T09:13:03Z`
Search mode: `hybrid`

## Chunk Statistics

| Strategy | Chunks | Avg chars | Min | Max | Section coverage | Backend |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| fixed | 391 | 1144.45 | 238 | 1199 | 1.0 | faiss |
| structural | 458 | 875.53 | 13 | 1799 | 1.0 | faiss |

## Retrieval Metrics

| Strategy | Queries | hit@1 | hit@3 | hit@5 | section@3 | MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fixed | 12 | 0.8333 | 1.0 | 1.0 | 0.75 | 0.9167 |
| structural | 12 | 0.8333 | 1.0 | 1.0 | 0.9167 | 0.9167 |

## Query Details

### fixed

- `How does the Telegram bot connect to MCP servers at runtime?` -> source rank: `1`, section rank: `1`
  - top1: `tg-agent/README.md` / `tg-agent` score `1.0` dense `0.8562` lexical `19.6772`
- `Which Rust module implements MCP client communication and tool calls?` -> source rank: `1`, section rank: `None`
  - top1: `tg-agent/tests/live_connect.rs` / `file prelude` score `0.9631` dense `0.7227` lexical `8.2845`
- `Where is the dynamic trip-planning swarm described or implemented?` -> source rank: `1`, section rank: `2`
  - top1: `tg-agent/src/agent/flow.rs` / `file prelude` score `0.9216` dense `0.6923` lexical `14.1878`
- `How are connected servers and user sessions persisted across restarts?` -> source rank: `1`, section rank: `3`
  - top1: `tg-agent/src/state.rs` / `impl BotState` score `0.9554` dense `0.564` lexical `10.0112`
- `Where does the bot build prompts with profile, memory, and tool context?` -> source rank: `1`, section rank: `2`
  - top1: `tg-agent/src/agent/prompt.rs` / `file prelude` score `0.9792` dense `0.7321` lexical `12.9731`
- `Which test covers the live trip planning flow?` -> source rank: `1`, section rank: `1`
  - top1: `tg-agent/tests/live_orchestrator.rs` / `function trip_swarm_clarifies_then_plans` score `0.9729` dense `0.7429` lexical `12.1659`
- `What Open-Meteo MCP tools are available for forecasts and weather comparison?` -> source rank: `1`, section rank: `1`
  - top1: `open-meteo-mcp/README.md` / `Weather data` score `0.9867` dense `0.8671` lexical `15.2255`
- `Where is weather quality scoring for city comparison implemented?` -> source rank: `2`, section rank: `4`
  - top1: `open-meteo-mcp/README.md` / `Weather data` score `0.984` dense `0.65` lexical `18.6398`
- `Which TypeScript tool implements compare_weather_cities or regional weather analysis?` -> source rank: `1`, section rank: `4`
  - top1: `open-meteo-mcp/README.md` / `Weather data` score `1.0` dense `0.7419` lexical `22.2047`
- `Where are scheduled weather jobs created, listed, summarized, and cancelled?` -> source rank: `1`, section rank: `1`
  - top1: `open-meteo-mcp/src/tools/schedule.ts` / `function registerScheduleTools` score `0.959` dense `0.713` lexical `11.7104`
- `Which code fetches weather forecast data from Open-Meteo APIs?` -> source rank: `1`, section rank: `2`
  - top1: `open-meteo-mcp/README.md` / `open-meteo-mcp` score `1.0` dense `0.7705` lexical `22.7104`
- `Where is geocoding for city names implemented in the weather MCP server?` -> source rank: `2`, section rank: `3`
  - top1: `tg-agent/src/agent/prompt.rs` / `file prelude` score `0.9227` dense `0.6543` lexical `9.0432`

### structural

- `How does the Telegram bot connect to MCP servers at runtime?` -> source rank: `1`, section rank: `1`
  - top1: `tg-agent/README.md` / `tg-agent` score `1.0` dense `0.8638` lexical `19.7582`
- `Which Rust module implements MCP client communication and tool calls?` -> source rank: `1`, section rank: `1`
  - top1: `tg-agent/src/mcp_client.rs` / `struct McpClient` score `0.9537` dense `0.7436` lexical `8.4584`
- `Where is the dynamic trip-planning swarm described or implemented?` -> source rank: `1`, section rank: `3`
  - top1: `tg-agent/README.md` / `Features` score `0.9079` dense `0.6697` lexical `15.8819`
- `How are connected servers and user sessions persisted across restarts?` -> source rank: `2`, section rank: `1`
  - top1: `tg-agent/tests/live_connect.rs` / `function registry_keeps_connection_across_calls` score `0.9317` dense `0.6383` lexical `9.1535`
- `Where does the bot build prompts with profile, memory, and tool context?` -> source rank: `1`, section rank: `4`
  - top1: `tg-agent/src/agent/prompt.rs` / `file prelude` score `0.9707` dense `0.7563` lexical `11.6538`
- `Which test covers the live trip planning flow?` -> source rank: `1`, section rank: `1`
  - top1: `tg-agent/tests/live_orchestrator.rs` / `function trip_swarm_clarifies_then_plans` score `0.9806` dense `0.7337` lexical `12.7742`
- `What Open-Meteo MCP tools are available for forecasts and weather comparison?` -> source rank: `1`, section rank: `1`
  - top1: `open-meteo-mcp/README.md` / `Weather comparison` score `1.0` dense `0.8956` lexical `18.0794`
- `Where is weather quality scoring for city comparison implemented?` -> source rank: `2`, section rank: `2`
  - top1: `open-meteo-mcp/README.md` / `Weather comparison` score `1.0` dense `0.7262` lexical `24.7479`
- `Which TypeScript tool implements compare_weather_cities or regional weather analysis?` -> source rank: `1`, section rank: `1`
  - top1: `open-meteo-mcp/README.md` / `Weather comparison` score `1.0` dense `0.7775` lexical `25.4729`
- `Where are scheduled weather jobs created, listed, summarized, and cancelled?` -> source rank: `1`, section rank: `1`
  - top1: `open-meteo-mcp/README.md` / `Scheduled collection` score `1.0` dense `0.7794` lexical `17.0336`
- `Which code fetches weather forecast data from Open-Meteo APIs?` -> source rank: `1`, section rank: `3`
  - top1: `open-meteo-mcp/README.md` / `open-meteo-mcp` score `1.0` dense `0.8472` lexical `17.944`
- `Where is geocoding for city names implemented in the weather MCP server?` -> source rank: `1`, section rank: `1`
  - top1: `open-meteo-mcp/src/tools/geocoding.ts` / `function registerGeocoding` score `1.0` dense `0.7375` lexical `18.9671`

## Interpretation

- Fixed chunking is expected to produce more uniform chunk sizes and predictable overlap.
- Structural chunking is expected to preserve headings, pages, functions, and sections more often.
- Prefer the strategy with stronger retrieval metrics unless its chunk sizes are too uneven for the target context window.
