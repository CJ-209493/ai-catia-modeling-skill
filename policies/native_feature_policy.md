# Native Feature Policy

Native success requires a native CATIA feature-tree entry and a successful update.

For promoted geometric recipes, native success also requires a reviewed CATIA screenshot that visibly matches the intended shape. A hidden, off-body, wrong-direction, or visually absent feature is not a successful recipe promotion.

Examples:

- Native Shell requires a `Shell` feature.
- Native Mirror requires a `Mirror` feature.
- Native Circular Pattern requires a `CircPattern` feature.
- Native Rectangular Pattern requires a `RectPattern` feature.
- Native Assembly Constraint requires a Product constraint object.

Explicit copies, manually repeated holes, manually built walls, and positioned products are not native feature success.

Report those as `GEOMETRY_EQUIVALENT` or `PARTIAL_SUCCESS`, depending on the user request.
