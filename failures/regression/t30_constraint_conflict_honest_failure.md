# Failure: T30 constraint_conflict

- classification: HONEST_FAILURE
- backend: pycatia
- error_signature: CONSTRAINT_CONFLICT_NOT_RUN
- error_message: 尺寸约束冲突：同一 X 向尺寸不能同时等于 100 mm 和 80 mm。

## Context
{}

## References
{
  "active_body": "part.in_work_object = body before creating each feature",
  "support_plane_reference": "Part.CreateReferenceFromObject(OriginElements.PlaneXY) or recorded offset/construction reference"
}

## Code Snippet
```python

```