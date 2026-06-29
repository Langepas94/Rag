# Chunking Strategy Comparison

Generated at: `2026-06-29T17:48:43Z`

## Chunk Statistics

| Strategy | Chunks | Avg chars | Min | Max | Section coverage | Backend |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| fixed | 387 | 1146.12 | 238 | 1199 | 1.0 | faiss |
| structural | 301 | 1369.29 | 15 | 1799 | 1.0 | faiss |

## Retrieval Metrics

| Strategy | Queries | hit@1 | hit@3 | hit@5 | section@3 | MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fixed | 12 | 0.5 | 0.5833 | 0.6667 | 0.25 | 0.5444 |
| structural | 12 | 0.4167 | 0.5 | 0.75 | 0.3333 | 0.5167 |

## Query Details

### fixed

- `How does the Telegram bot connect to MCP servers at runtime?` -> source rank: `1`, section rank: `None`
  - top1: `tg-agent/README.md` / `tg-agent` score `0.8563`
- `Which Rust module implements MCP client communication and tool calls?` -> source rank: `None`, section rank: `None`
  - top1: `tg-agent/tests/live_connect.rs` / `live_connect.rs` score `0.7231`
- `Where is the dynamic trip-planning swarm described or implemented?` -> source rank: `1`, section rank: `None`
  - top1: `tg-agent/src/agent/flow.rs` / `flow.rs` score `0.7474`
- `How are connected servers and user sessions persisted across restarts?` -> source rank: `1`, section rank: `None`
  - top1: `tg-agent/src/state.rs` / `state.rs` score `0.5642`
- `Where does the bot build prompts with profile, memory, and tool context?` -> source rank: `1`, section rank: `None`
  - top1: `tg-agent/src/agent/prompt.rs` / `prompt.rs` score `0.7324`
- `Which test covers the live trip planning flow?` -> source rank: `5`, section rank: `None`
  - top1: `tg-agent/tests/live_orchestrator.rs` / `live_orchestrator.rs` score `0.7429`
- `What Open-Meteo MCP tools are available for forecasts and weather comparison?` -> source rank: `1`, section rank: `None`
  - top1: `open-meteo-mcp/README.md` / `Weather data` score `0.8671`
- `Where is weather quality scoring for city comparison implemented?` -> source rank: `1`, section rank: `1`
  - top1: `open-meteo-mcp/src/tools/weather-logic.ts` / `function gridPoints` score `0.6626`
- `Which TypeScript tool implements compare_weather_cities or regional weather analysis?` -> source rank: `None`, section rank: `None`
  - top1: `open-meteo-mcp/README.md` / `Weather data` score `0.742`
- `Where are scheduled weather jobs created, listed, summarized, and cancelled?` -> source rank: `3`, section rank: `3`
  - top1: `tg-agent/src/llm.rs` / `llm.rs` score `0.6752`
- `Which code fetches weather forecast data from Open-Meteo APIs?` -> source rank: `None`, section rank: `3`
  - top1: `open-meteo-mcp/README.md` / `open-meteo-mcp` score `0.7706`
- `Where is geocoding for city names implemented in the weather MCP server?` -> source rank: `None`, section rank: `None`
  - top1: `tg-agent/src/agent/prompt.rs` / `prompt.rs` score `0.6544`

### structural

- `How does the Telegram bot connect to MCP servers at runtime?` -> source rank: `1`, section rank: `None`
  - top1: `tg-agent/README.md` / `tg-agent` score `0.8641`
- `Which Rust module implements MCP client communication and tool calls?` -> source rank: `5`, section rank: `None`
  - top1: `tg-agent/README.md` / `tg-agent` score `0.6949`
- `Where is the dynamic trip-planning swarm described or implemented?` -> source rank: `1`, section rank: `None`
  - top1: `tg-agent/src/agent/flow.rs` / `flow.rs` score `0.7523`
- `How are connected servers and user sessions persisted across restarts?` -> source rank: `None`, section rank: `1`
  - top1: `open-meteo-mcp/src/notifications.ts` / `function servers` score `0.5803`
- `Where does the bot build prompts with profile, memory, and tool context?` -> source rank: `1`, section rank: `None`
  - top1: `tg-agent/src/agent/prompt.rs` / `prompt.rs` score `0.7178`
- `Which test covers the live trip planning flow?` -> source rank: `4`, section rank: `None`
  - top1: `tg-agent/tests/live_orchestrator.rs` / `live_orchestrator.rs` score `0.7104`
- `What Open-Meteo MCP tools are available for forecasts and weather comparison?` -> source rank: `1`, section rank: `5`
  - top1: `open-meteo-mcp/README.md` / `Weather comparison` score `0.8959`
- `Where is weather quality scoring for city comparison implemented?` -> source rank: `None`, section rank: `2`
  - top1: `open-meteo-mcp/README.md` / `Weather comparison` score `0.7266`
- `Which TypeScript tool implements compare_weather_cities or regional weather analysis?` -> source rank: `4`, section rank: `4`
  - top1: `open-meteo-mcp/README.md` / `Weather comparison` score `0.7779`
- `Where are scheduled weather jobs created, listed, summarized, and cancelled?` -> source rank: `2`, section rank: `2`
  - top1: `open-meteo-mcp/README.md` / `Scheduled collection` score `0.7795`
- `Which code fetches weather forecast data from Open-Meteo APIs?` -> source rank: `None`, section rank: `None`
  - top1: `open-meteo-mcp/README.md` / `open-meteo-mcp` score `0.8472`
- `Where is geocoding for city names implemented in the weather MCP server?` -> source rank: `1`, section rank: `1`
  - top1: `open-meteo-mcp/src/tools/geocoding.ts` / `function registerGeocoding` score `0.7375`

## Interpretation

- Fixed chunking is expected to produce more uniform chunk sizes and predictable overlap.
- Structural chunking is expected to preserve headings, pages, functions, and sections more often.
- Prefer the strategy with stronger retrieval metrics unless its chunk sizes are too uneven for the target context window.
