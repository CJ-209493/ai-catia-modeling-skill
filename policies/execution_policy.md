# Execution Policy

## User Mode

Use only recipes marked `stable`, `verified_repeatable`, or `live_verified_once`.

Do not generate fresh pycatia code in User Mode. If no verified recipe exists, return `UNSUPPORTED` with a clear explanation and suggest Developer Mode exploration.

## Developer Mode

Developer Mode is required for:

- new pycatia API calls
- boundary probes
- recipe promotion
- failure-memory edits
- verifier expansion

## Execution Gate

Every run must produce:

- Feature Plan
- selected recipe IDs
- runner command or runner module
- `Part.Update` result
- verifier result
- classification
- report

Do not treat a COM object being returned as proof of modeling success.
