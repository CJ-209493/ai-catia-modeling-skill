# Verification Policy

Classify after verification, not after code execution.

Required checks:

1. The runner completed without unhandled exception.
2. CATIA `Part.Update` or `Product.Update` succeeded.
3. Feature-tree verifier found the expected native feature.
4. Geometry or parameter verifier checked core dimensions when available.
5. Semantic classifier applied policy exclusions.

If any required check is missing, do not claim `NATIVE_SUCCESS`.

`GEOMETRY_EQUIVALENT` means the shape may look correct, but the required native feature was not verified.

`HONEST_FAILURE` is acceptable when a request is contradictory or CATIA rejects the feature.
