# Failure Memory: Part.Update Failed Is Not Success

Many pycatia calls return COM objects before CATIA rebuilds the part.

If `Part.Update` fails:

- do not claim success
- record exception signature
- save failure report if possible
- leave recipe status unchanged
