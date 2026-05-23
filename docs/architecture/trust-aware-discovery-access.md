# Trust-Aware Discovery and Access Manager

Progressive access levels:

| Level | Access | Use |
|---:|---|---|
| 0 | Manual intake | Rough planning |
| 1 | Docs/architecture | Better risk review |
| 2 | Metadata-only | Schema/dashboard/pipeline/cost assessment |
| 3 | Read-only connections | Accurate recommendations and validation |
| 4 | Managed execution | Approved build/migration/deployment |

Credentials are not ingested. They are submitted through a vault/OAuth flow, stored as secret references, and exposed to agents only as validation status and scope.
