# Frequently Asked Questions (FAQ)

### Q: Why does M31A only support NVIDIA NIM models?
A: High-assurance autonomous engineering requires verified model alignments, deterministic JSON tool calling, and high-throughput streaming. NVIDIA NIM provides standardized enterprise inference endpoints. Other providers are intentionally retired in production to eliminate multi-provider behavioral discrepancies.

### Q: Where does M31A store its database?
A: In platform user data directories (`~/.local/share/m31a/m31a.db` on Linux). It never commits databases into your repository.

### Q: How do I cancel an autonomous task in progress?
A: In the TUI, press `Ctrl+C`. In CLI mode, send `SIGINT` (Ctrl+C). M31A initiates instant cancellation, terminates child process trees, and seals output spools.

### Q: Can M31A run without an internet connection?
A: LLM reasoning requires internet access to reach the NVIDIA NIM endpoint. However, all deterministic verification checks, compilers, linters, and SQLite transactions execute 100% locally on your machine.
