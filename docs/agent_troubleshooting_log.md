# Agent Troubleshooting Log

This document logs recurring issues encountered by the AI agent during development and the standard operating procedures (SOPs) adopted to resolve them.

## Issue: Incomplete File Reads

- **Date:** 2025-08-04
- **Tool:** `view_file`

### Description

The agent frequently encounters an issue where the `view_file` tool returns only the first line of a requested file, particularly with `.md`, `.ts`, and `.json` files. This prevents the agent from gathering the necessary context to proceed with development tasks, such as understanding architectural requirements or verifying existing code.

### Resolution SOP

To ensure the full file content is retrieved, the following two-step process has been adopted as a standard workaround:

1.  **Initial Read Attempt:** The agent first calls `view_file` with only the `AbsolutePath` argument.
2.  **Forced Full Read:** If the initial attempt returns incomplete content (e.g., only one line), the agent immediately re-calls `view_file` for the same file but includes the `StartLine` and `EndLine` arguments with a wide range (e.g., `StartLine: 1`, `EndLine: 300`).

This procedure has proven to be a reliable method for overcoming the tool's limitation and ensuring development can proceed without being blocked.
