# Native Feature Policy

Native success requires a native CATIA feature-tree entry and a successful update.

Examples:

- Native Shell requires a `Shell` feature.
- Native Mirror requires a `Mirror` feature.
- Native Circular Pattern requires a `CircPattern` feature.
- Native Rectangular Pattern requires a `RectPattern` feature.
- Native Assembly Constraint requires a Product constraint object.

Explicit copies, manually repeated holes, manually built walls, and positioned products are not native feature success.

Report those as `GEOMETRY_EQUIVALENT` or `PARTIAL_SUCCESS`, depending on the user request.
