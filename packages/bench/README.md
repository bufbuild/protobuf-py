# Benchmark suite

A collection of external benchmark suites to evaluate protobuf-py performance.

We collect the Protobuf binary test payloads from external suites and for each case,
parse the binary payload into a message of the appropriate type. For parse benchmarks,
this is the operation that is measured. For serialization benchmarks, this message
is then serialized, with the time measured.

Both protobuf-py and `google.protobuf` implementations are benchmarked. Note, the
upb implementation of `google.protobuf` trades increased marshaling performance for
decreased attribute access performance. The pure serialization benchmarks we run
cannot take this into account - to understand real performance, always benchmark your
own specific logic.

## Included suites

We fetch and execute benchmark test cases from:

- [hyperpb](https://github.com/bufbuild/hyperpb-go)
- [buffa](https://github.com/anthropics/buffa)
- [fleetbench](https://github.com/google/fleetbench)
  - C++ code is auto-translated to Python

## Running

Run all benchmarks with `uv run poe bench`. Individual tests can use standard `pytest` query syntax, for example
testing serialization of a single hyperpb case could look like

```shellsession
uv run poe bench -k 'test_serialize and hyperpb:tree_cold.yaml:0'
```

## Updating benchmark cases

To update the cases, update the version we fetch for the particular suite in [generate.py](./scripts/generate.py)
and run `uv run poe generate-bench`. [Go](https://go.dev/doc/install) must be installed to run it.
