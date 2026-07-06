# Failure Memory: Product.Position Is Not Assembly Constraint

Setting `Product.Position` can place components visually, but it does not create CATIA assembly constraints.

Required native evidence:

- Product constraints collection exists
- constraint object is created through `Constraints.AddMonoEltCst`, `AddBiEltCst`, or `AddTriEltCst`
- `Product.Update` succeeds
