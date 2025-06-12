# PSP Circuit Breaker with Human-readable Configuration

by This Will Be Reflected In Your Promotion Rationale (TWBRIYPR) (Alvaro Duran and Magda Jurcakova)

## Problem

Large merchants who have a Multi-PSP payment system get their operations disrupted when a PSP experiences an outage
or when an unforeseen event causes currency-conversion instability.

This unforunately happens quite frequently. And, most of the time, at night.

Most companies anticipate this problem by having engineers on a 24/7 oncall rotation, but the remediation process
is often manual, and requires either code changes or database write permissions, which poses both security and operational risks.

Engineers can make mistakes, especially at 2am.

The remediation process is actually quite simple to explain: turn off the appropriate provider or providers given a predefined
set of circumstances.

For instance, if PSP 1 is down, the system has to ensure that all payments being process by that PSP are routed to PSP 2.
If there is political turmoil in Country A, we need to ensure that all PSPs that support a given currency are either disconnected,
or configured so that they temporarily reject any payment in that country's currency.

This is not just a nuisance for engineers. Every second the platform is down is potential revenue lost for the whole company.

## Solution: Have an MCP do basic remediations during the night

An engineer shouldn't have to be woken up to handle basic remediations. Believe us, we know.

Magda and Alvaro are part of the Fintech team at Kiwi.com, and we've experienced first-hand what these PSPs are all about.
They don't require much brain power, but that's precisely what we're lacking when it's 2am in the morning. Nobody wants us
to be awake at that time, and yet we have to do it sometimes.

But, for an AI, this is very basic stuff. We can even explain what it has to do on a human-readable document, one that
payment specialists, and not necessarily engineers, can maintain. This is crucial, because the routing logic is always
derived from the expertise of specialists and not necessarily the engineers'.

Thanks to the Model Context Protocol, we can connect to a shared Google Document and our routing table in the database.

## The Technical Challenges

MCP is a very recent protocol, implemented less than a year ago.

- MCPs are meant to be used from Claude/Cursor/etc. There's little support for MCP clients yet.
- We're building this in a way that is automatically triggered, rather than proactively started by a human.
- Lack of official MCP servers for Postgres and, surprisingly, Google Docs.

The architecture consists of:
- A celery task that gets periodically started (every 30 seconds)
- A Postgres MCP (unofficial) server
- A Google Doc MCP (unofficial) server
- Each one inside its own docker instance
- Orchestrated via docker compose

### Have we found a bug in MCP Python SDK?

We were able to reproduce an error that was raised on [Apr 29](https://github.com/tadata-org/fastapi_mcp/issues/124) where
an MCP Client inside a Docker container cannot connect to another container using httpx AsyncClient with streamable-http transport.


## Potential future additions and use cases

- No oncalls
- Faster PSP integration and onboarding

- Notification to the team via Slack
- Metrics and Analytics of PSP to enforce SLAs
- Better logging
- Stepping stone for more automated AI controls, such as bad deployments (Canary AI) and Quality Assurance (QA AI)
- More comprehensive and sophisticated downtime routing, feedback on the document itself.

## Driving the Technical Future of the Model Context Protocol specification

This project pushes the limits on what MCP Servers and Clients can do so far, and can be the testing ground for future improvements on the protocol.


