# Verification Policy

Classify after verification, not after code execution.

Required checks:

1. The runner completed without unhandled exception.
2. CATIA `Part.Update` or `Product.Update` succeeded.
3. Feature-tree verifier found the expected native feature.
4. Geometry or parameter verifier checked core dimensions when available.
5. Semantic classifier applied policy exclusions.
6. For recipe promotion, a CATIA Viewer screenshot must be captured and reviewed. If the screenshot does not visibly match the intended geometric feature, the recipe is not promoted as visually verified even when COM calls, `Part.Update`, and feature-tree checks pass.

If any required check is missing, do not claim `NATIVE_SUCCESS`.

`GEOMETRY_EQUIVALENT` means the shape may look correct, but the required native feature was not verified.

`HONEST_FAILURE` is acceptable when a request is contradictory or CATIA rejects the feature.

Non-geometric Knowledgeware or Assembly recipes may be classified by parameter/product-tree verification. Their screenshots are evidence that CATIA opened the document/tree, not proof of geometric shape.
