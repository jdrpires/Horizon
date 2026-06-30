# Roadmap

## Current

- Introduce a generic Collector Framework for external observation ingestion without transport-specific integrations.

## Next

- Design transport-specific collectors behind the generic Collector Framework.
- Design the future Observation Value Model for non-numeric observations.
- Review Experience Profiles and Developer Mode as explicit future capabilities.
- Use JSON persistence as the local adapter until a future storage architecture is approved.
- Improve implementation-level test automation when Python 3.13 and Poetry are available.
- Use the Temporal Memory Engine as the local replay foundation before Event Store architecture is approved.
- Add implementation-only refinements for Observation validation messages and Horizon Lab ergonomics after architectural review.
