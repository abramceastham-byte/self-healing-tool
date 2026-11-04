# Notes for the agent

- Write a failing test that reproduces the error first, then the smallest fix that makes it pass.
- Do not change public endpoint paths or response field names.
- Run `pytest` before opening a PR; it must pass.
- Never edit files matching `protected_files` in `.selfheal/config.yml`.
- The PR description must explain the cause and fix in plain language.
