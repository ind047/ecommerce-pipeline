# Orchestrated E-Commerce Analytics Pipeline

An end-to-end, fully automated data pipeline on **Google Cloud Platform** — from data
generation to an executive dashboard — built to production patterns: serverless,
tested, version-controlled, and reproducible from code.

> Mock e-commerce order data flows through ingestion → cloud storage → warehousing →
> analytics engineering → BI, with **zero manual steps** and data-quality gates at
> every layer.

## Architecture

```
6:00 AM  Cloud Scheduler → Cloud Function (2nd Gen) → ~5,000 orders
         → Parquet (immutable, timestamped) → Google Cloud Storage
                     │ external table (query-in-place)
                     ▼
              BigQuery: raw_orders_external
                     │
7:00 AM  Dataform schedule (GitHub release) → rebuilds models + assertions
                     │
                     ▼
        Dataform (SQLX):  stg_orders (dedup, quarantine, typed)
                          dim_customers ─┐
                          fct_orders  (star schema, day-partitioned,
                          clustered, assertions) ─┘
                     │ live connection
                     ▼
        Data Studio Executive Dashboard (revenue trends, category mix, top customers)

Terraform: bucket, dataset, scheduler & IAM declared as code (init/plan/apply/destroy)
```

## The daily run (fully hands-off)

| Time | What happens |
|---|---|
| **6:00 AM** | Scheduler triggers the function → generates orders → streams Parquet to GCS |
| **7:00 AM** | Dataform pulls the pinned GitHub release → rebuilds models → runs all assertions |
| **All day** | Dashboard queries the fresh, tested tables |

If any assertion fails, the Dataform execution goes red — bad data never reaches
the dashboard silently.

## Tech stack

| Layer | Technology |
|---|---|
| Ingestion | Python, Faker, pandas, Cloud Functions (2nd Gen), Cloud Scheduler |
| Storage | Google Cloud Storage (Parquet, immutable files, lifecycle rules) |
| Warehouse | BigQuery (external tables, partitioning, clustering) |
| Transformation | Dataform (SQLX): staging, star schema, assertions |
| BI | Data Studio (live BigQuery connection) |
| IaC | Terraform |
| Tooling | uv, gcloud/bq CLIs, git |

## Engineering highlights

**Data quality as executable contracts.** Assertions (`uniqueKey`, `nonNull`,
`rowConditions`) are version-controlled SQL that runs with every build. One caught a
genuine distributed-systems bug: seeding Faker for reproducibility caused UUID
sequences to *replay across cold-started containers* — duplicate `order_id`s across
separate Parquet files. The `uniqueKey` assertion flagged it automatically. Fixed at
the source (true `uuid4` for order IDs) *and* defensively in staging (dedup via
`ROW_NUMBER()`).

**Raw vs. serving zones.** Raw data queried in place via a BigQuery *external table*
(federated, zero load jobs); serving tables are native, day-partitioned and clustered.

**Bad batches handled without deletion.** Append-only lake; corrupt files quarantined
declaratively via `_FILE_NAME` filtering at staging — history intact, analytics clean.

**Everything in git.** Generator, function, table definitions, Dataform models,
Terraform — the system is reproducible from the repo.

## Concepts practiced

- Serverless & containerized deploys (Cloud Build → Artifact Registry → Cloud Run)
- Batch vs. streaming trade-offs; immutable file-based lakes
- Star schema design; ELT; partition pruning & clustering
- Dependency graphs, release vs. workspace environments
- IAM: service accounts, least privilege
- IaC: declarative state, plan-before-apply, state management

## Status

- [x] Phases 1–3: ingestion, serverless automation, analytics engineering
- [x] Phase 4: dashboard + scheduled executions + Terraform lifecycle
- [ ] Import existing infrastructure into Terraform (`terraform import`)
- [ ] Streaming variant (Pub/Sub + Dataflow) for comparison