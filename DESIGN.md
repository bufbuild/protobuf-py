# Design

An idiomatic Protocol Buffers runtime for Python 3, implemented in Python with zero runtime dependencies.

## Design Principles

**Fully-featured protobuf implementation.**
This is not a subset — the goal is a complete implementation that can replace the official `protobuf` package, with support for editions, extensions, reflection, custom options, ProtoJSON, and unknown field preservation.

**Spec compliant.**
The runtime passes the protobuf conformance test suite for both binary and JSON encodings.

**Pure Python core, zero third-party dependencies.**
There are no required C extensions and no runtime dependencies — install it and use it. A native extension is published
for major platforms and used transparently, no Rust compiler needed. The native extension only accelerates functions,
it does not replace the data model, which uses standard Python classes / attributes.

**Descriptor-centric.**
Descriptors are the single source of truth for all runtime behavior — every message and enum carries its own. Serialization, presence tracking, default values, and reflection all dispatch through descriptors rather than generated code, which keeps the generated layer thin and consolidates logic in one place.

**Pythonic.**
Generated messages should look and feel like hand-written Python classes. You construct them with keyword arguments, access fields as attributes, clone with `copy.replace()`, and get a readable string from `repr()`. There are no `FIELD_NUMBER` class variables, no `HasField()` methods, and no `SerializeToString()`.

**Unified runtime.**
Generated messages and dynamic messages are identical — they share the same base class, the same serialization code, and the same reflection behavior. The only difference is how the descriptor is loaded: from embedded bytes at import time for generated code, or from a `FileDescriptorProto` at runtime for dynamic messages.

**No global registry.**
Types are resolved explicitly via `Registry` instances rather than a process-wide singleton, which avoids the identity conflicts, import-order bugs, and test isolation problems that come with a global registry. A registry is only needed when resolving `google.protobuf.Any` or extensions in ProtoJSON — everywhere else, descriptors are self-contained.

**Container emulation for reflection.**
Python defines a well-specified protocol for [emulating container types](https://docs.python.org/3/reference/datamodel.html#emulating-container-types), and messages implement it: `for field in msg` to iterate over set fields, `msg[field]` to get, `msg[field] = v`
to set, `field in msg` to check presence, and `del msg[field]` to clear. This replaces custom reflection methods with something Python developers already understand, and the same mechanism backs both the typed property access in generated code and the dynamic access used by serializers and generic tooling.

**A completely optional but automatic native extension.**
protobuf-py is the idiomatic Python library for Protobuf. It should never cause pain points to Python developers.
Notably, both users and repository contributors should never require Rust or a long build step to use the library.
But users on common platforms, especially Linux, MacOS, and Windows, should have a high performance Protobuf library
without headaches. We accomplish the above by publishing the extension as a separate package, `protobuf-py-ext`, and
only including it as a conditional dependency on platforms we publish wheels for, as a pre-release step in CI, not a
committed change to pyproject.toml.

## Modules

**`protobuf`** is the main entry point, exporting `Message`, `Enum`, `Extension`, `Oneof`, `Registry`, and the descriptor types. Most users import only from here.

**`protobuf._wire`** provides the low-level binary encoding primitives. `BinaryReader` and `BinaryWriter` handle varint encoding, fixed-width types, length-delimited fields, and group delimiters — these are the building blocks that message serialization is built on.

**`protobuf._codegen`** is for generated code only. It provides the machinery to load embedded descriptors at import time and link them to generated classes. Application code should not import from here.

**`protobuf.plugin`** is a protoc plugin framework. It handles the request/response lifecycle so that plugin authors write only a generate callback. See the Plugin Framework section below.

**`protobuf.wkt`** ships the well-known types — `Timestamp`, `Duration`, `Any`, `Struct`, `FieldMask`, wrapper types, and all other types from Google's protobuf standard library. These are pre-generated and distributed with the runtime so users don't need to generate them.

## Messages

The goal is that protobuf messages feel like regular Python classes. A generated message is a subclass of `Message` with typed properties for each field, and under the hood every property delegates to the same container emulation methods on the base class. The base class uses the message's descriptor to determine field types, default values, presence semantics, and oneof groupings.

```python
msg = Person(name="Alice", id=42)
msg.name                        # typed attribute access
msg[Person.desc().field["name"]]  # dynamic access by descriptor
msg.has_field("name")                   # presence check
msg.clear_field("name")                 # clear to default
for field in msg:               # iterate set fields
    print(field.name, msg[field])
```

Field presence follows protobuf semantics: explicit-presence scalar fields distinguish between "set to zero" and "not set," implicit-presence fields treat the zero value as absent, message fields are `None` when unset, and repeated and map fields are empty collections when unset.

Unknown fields are preserved through binary round-trips by default, so a message can pass through an intermediary that doesn't know about newer fields without losing data.

## Serialization

Binary serialization is implemented as a single-pass write using a fork/join pattern for nested messages. When entering a sub-message, the writer reserves a placeholder for the length prefix, writes the sub-message content, then backfills the actual length — avoiding the need to pre-compute message sizes or make a second pass over the data.

Deserialization uses merge semantics: parsing into an existing message overwrites scalars, recursively merges sub-messages, appends to repeated fields, and merges map entries. This is the behavior required by the protobuf spec and enables patterns like merging partial updates.

ProtoJSON serialization and deserialization are complete, including the special encodings required for well-known types like `Timestamp`, `Any`, `Struct`, `Duration`, `FieldMask`, `Value`, and `ListValue`.

## Type System

**Oneofs** are represented as `Oneof` dataclasses with a `field` and `value`, which works naturally with Python's `match` statement for type-safe dispatch:

```python
match msg.result:
    case Oneof(field="value", value=v):
        handle_value(v)
    case Oneof(field="error", value=e):
        handle_error(e)
```

Setting a field that belongs to a oneof automatically clears the other fields in the group.

**Enums** are `IntEnum` subclasses. Open enums (the default in editions and proto3) accept unknown integer values and preserve them for round-tripping, while closed enums (proto2 default) reject unknown values. Exactly matching enum value name prefixes are stripped automatically — `PHONE_TYPE_MOBILE` becomes `PhoneType.MOBILE`. Value names are left unstripped if they would match an existing enum value name or start with a digit. More complex schemes such as case-insensitive matching introduce design decisions like which item to select for stripping, which also need to be communicated to the user.
We elect for the simple scheme that matches usage which passes `buf lint`.

In Python, `bool` is a subclass of `int` - this means it can be used anywhere it can be. Unfortunately, this means invocations like
`Color(True)`, `Color(False)` are possible and equivalent to `Color(1)` and `Color(0)`. A custom metaclass could potentially guard
against this but we will consider this usage too niche to add the complexity for.

**Extensions** are accessed through the same container protocol as fields: `msg[ext]` to get, `msg[ext] = v` to set, `ext in msg` to check presence, and `del msg[ext]` to clear. Extensions are stored as unknown fields on the extended message and parsed lazily on access, which keeps the message class clean and avoids the identity conflicts that come from eagerly registering extensions at import time.

## Well-Known Types

The well-known types are pre-generated and shipped with the runtime. On top of the generated message classes, helper subclasses provide idiomatic Python conversions:

- `Timestamp` converts to and from `datetime`, seconds, and nanoseconds. `Timestamp.now()` creates a timestamp from the current time.
- `Duration` converts to and from `timedelta`, seconds, and nanoseconds.
- `Any` provides `pack()` and `unpack()` for wrapping and unwrapping arbitrary messages.

## Code Generation

The code generation plugin (`protoc-gen-py`) produces one Python file per `.proto` file. Each generated message is a subclass of `Message` with an `__init__` that accepts all fields as keyword arguments with appropriate defaults, a typed property (getter and setter) for each field, and a file-level descriptor object that links the generated classes to their embedded descriptors.

The generated code contains no serialization logic, no presence tracking, and no reflection methods — all of that lives in the base `Message` class and is driven by descriptors.

Generated files import only from a fixed set of sources:

- `protobuf` — public base types (`Message`, `Enum`, `Extension`)
- `protobuf.wkt` — well-known type file descriptors
- Relative sibling `_pb.py` files — cross-file proto dependencies
- stdlib (`__future__`, `typing`)
- `protobuf._codegen` — codegen machinery (`file_desc`, WKT mixins)

`protobuf._codegen` is a private contract between the runtime and the code generator — it does not follow semver and is not meant for application code.
This boundary exists so that upgrading the runtime never breaks existing generated files.
If a breaking change to the codegen contract is needed, a new versioned module (e.g. `protobuf._codegenv2`) can be introduced alongside the old one.

## Plugin Framework

The `protobuf.plugin` package is a reusable protoc plugin framework.
It handles the `CodeGeneratorRequest`/`CodeGeneratorResponse` lifecycle — reading from stdin, parsing options, resolving descriptors, and writing the response — so that plugin authors write only generation logic.

A plugin is a single `run()` call with a generate callback.
The callback receives a `Schema` that provides the files to generate and a factory for output files.
With the framework, `protoc-gen-py` reduces to:

```python
def generate(schema: Schema) -> None:
    for desc in schema.files_to_generate:
        f = schema.generate_file(desc, "_pb.py")
        f.preamble(desc)
        generate_message(f, desc)

def main() -> None:
    run("protoc-gen-py", importlib.metadata.version("protoc-gen-py"), generate)
```

No stdin reading, no descriptor resolution, no response writing — the framework owns all of that.

Plugin authors define their option surface as a plain Python dataclass and the framework handles parsing — no manual argument processing.
A callable escape hatch is available for custom parsing needs.

`Schema` and `File` are `Protocol` types so that plugin code depends only on the interface, not the implementation.
This means a plugin can be tested against stub implementations without importing the framework internals.

## Documentation

Comprehensive documentation is important to guide users as they get started using this framework. Being able to get to something
working easily and smoothly increases the chance a user onboards the framework and explaining details or corner cases can keep
them coming back for more.

There are largely two facets to documentation.

### README.md

The repository level README will commonly be the first documentation a user sees for a project, either because they found the repo or because
they found the package on PyPI, where the README is displayed as well. It must give an explanation of what the project is, and a simple
getting-started to let a user dive in right away even if they don't read anything else. Being a single document without complex structure, it is
not appropriate to go through many different usage patterns or dive into the often confusing details of working with Protocol Buffers.

The README is a simple Markdown file that is edited as text and either previewed with a Markdown viewer such as in an IDE, or in a GitHub
pull request.

### Documentation website

For detailed documentation, we publish a full documentation website, with a link from the GitHub repository and PyPI package.
This can have several pages with navigation in a sidebar, with pages such as Introduction, Installation, About Protobuf, Usage,
API reference, and more. The website is published to GitHub pages, which is automatically available for any GitHub repository
and easy to set up for publishing.

We use the [Zensical](https://Zensical.org/docs/authoring/markdown/) tool for writing docs for the website. It allows writing with Markdown
in a folder called `docs`, and Zensical converts them to HTML in a build step to create the website. Standard Markdown syntax will be rendered with the
Material theme that is commonly used in the Python ecosystem, lending familiarity even to newcomers. There are also many custom
extensions supported such as tabs and should be used where appropriate to make the docs easier to read.

Zensical also supports automatic rendering of docstrings into HTML, which we use to populate the API reference page to allow
easy lookup of the APIs in the project.
All docstrings must use [Google style](https://mkdocstrings.github.io/griffe/reference/docstrings/#google-style), which
Zensical's underlying griffe parser expects.
Use `Args:`, `Returns:`, `Raises:`, `Attributes:`, and `Examples:` sections as appropriate.
Within `Examples:` sections, use fenced `\`\`\`python code blocks or doctest-style `>>>` snippets.

While the Markdown files will often be readable by themselves, they will miss the theming or rendering of special components of
Zensical's build step. Auto-generated pages like the API reference aren't readable at all. To support writing docs, Zensical
provides a local web server that renders pages on the fly, automatically updating based on local changes. The doc writing flow
is largely starting the server with the command `uv run poe docs-serve` and adding / editing Markdown files in the `docs` folder.

## Core Decisions

**Container emulation is the reflection API.**
Container emulation by overriding `__getitem__`, `__setitem__`, etc provides a natural Pythonic API for reflection without
needing a separate API. Standard attribute access continues to work with optimal performance.

**Unset message fields return `None`.**
Python lacks an optional chaining operator (`?.`), so accessing deeply nested message fields requires explicit null checks. We explored returning a read-only "none message" that would allow safe chaining (like Go's nil-receiver behavior), but this would require generating a second type for every message. We also explored auto-vivifying writes on access, but this is not thread-safe. Returning `None` is the simplest correct behavior, and we expect Python may eventually add none-aware operators.

**Extensions are stored as unknown fields.**
Rather than eagerly parsing extensions at deserialization time (like Java), extensions stay in their wire format until explicitly accessed. This is simpler to implement, avoids import-order dependencies, and means a message's size in memory doesn't grow with the number of registered extensions.

**Extension names have a `ext_` prefix**
Extension names match what would be a field name on the message being extended. This often results in short identifiers, for example
in `validate.proto`, `message`, `field`, and `oneof`. As these names provide little context when imported in code, we prefix with
`ext_` to help distinguish them from other names in a user's source code.

**Messages support equality comparison.** `==` compares messages by value: two messages are equal when they have the same type, the same fields set, and the same field values. Extensions and unknown fields are not considered.

**Legacy required fields are validated on serialization, not on parsing.**
Fields with `features.field_presence = LEGACY_REQUIRED` (proto2 `required`) are checked when serializing to binary or ProtoJSON — an error is raised if the field is not set. When parsing from binary or ProtoJSON, missing required fields are silently accepted. This matches protobuf-go, protobuf-es, and the C++ implementation.

### Escaping Python code

**Generated code is always valid Python code.**
There are several syntax conflicts between proto files and generated Python that if treated without escaping can result in
Python code that cannot be executed. We always escape when needed to create valid code that a user can use, by
suffixing keyword conflicts with a `_` to prevent syntax errors, and prefixing identifiers starting with `_` with `pb_`
to ensure the identifier is publicly visible. Protobuf is an interchange format and has no concept of private
visibility.

**No two input strings can result in the same escaped output string.**
If simply applying escaping on conflicts, it can result in the same output for a field that matches the escaped
output. We always apply an injective mapping when escaping to ensure no conflicts in escaped output, for example
`class_` is escaped to `class__` because the value without underscores is reserved. This allows breaking-change
detection to work without issues.

**Attributes never shadow base class attributes. They can shadow builtins.**
It is not strictly required to prevent shadowing, but it makes accessing base class functionality unintuitive to users
and type checkers flag shadowing of class attributes with different type.
Because attributes are always namespaced and builtins are not, it is acceptable to allow them to shadow builtins.

**Message and enum class names are aggressively escaped.**
We do not optimize to keep escaped class names to the absolute minimum. Protobuf has had a long-standing convention for
message and enum names to be `PascalCase`, with it being possible to validate it in the compiler using editions syntax.
The nature of Python is escaping is almost always needed only for `snake_case` names, meaning escaping will almost
never apply to real-world protos. We prioritize simplifying sanitization to allow generating correct, though ugly,
code for the rare cases it will be applied while otherwise having no effect on users.

- builtins we output in generated code are escaped, i.e. `int`, `str`, `list`, etc. These are used in type annotations
  and without special handling would conflict with the class names. It is possible to use aliases to generate type
  annotations that do not collide, but we keep both the implementation and generated code simpler instead.
- Collisions with message attributes are escaped. Top-level names do not need this escaping but nested ones do.
  We keep the implementation and expected escaping behavior consistent for both.
- Prefixes that may collide with other top level names like extension names are always escaped.

**Message fields that match an escaped class name are escaped.**

Soft keywords like `int`, `str` do not have problems being Python attributes, however because the same
when used as a class name is escaped, there can be collisions for names that don't collide in a `.proto`, for
example `enum int {}` and `string int_ = 1` in the same message. We detect when a `_` suffix is present in such
a message field name in the proto, i.e. it can collide with an _escaped_ class name, and escape it with an extra
`_`. This allows message fields to still be usable, for example the common name `bytes`.

**Module names are restricted to alphanumeric.**
Python allows non-ASCII characters in module names and prevents hyphens. To create compilable module names from file paths, 
we at least need to replace hyphens and ensure the module does not start with a digit to prevent being treated as a numeric literal.
We replace all non-alphanumeric + underscore characters with underscore. This will notably replace hyphen, a relatively common
separator in file names, with an underscore. We cannot make this transformation injective to prevent collisions with filenames that
result in the same replaced string. Instead, we have an opt-in to append a hash of the input string when escaping. We do not attempt to escape files
that contain a match to the hash, assuming the probability of such a collision is too low to matter. Because the hash makes file names
look extremely unnatural, this behavior is opt-in with the `escape_module_with_hash` plugin option.

We prefix with `pb_` if the first character is a digit, similar to our prefixing of `_` for other identifiers like message attributes.
Existing `pb_` are also prefixed making it injective.


## Following Upstream Changes

The project tracks upstream `protocolbuffers/protobuf` for the protoc compiler, conformance test suite, well-known type protos, and edition feature defaults.
There is no submodule or automatic sync — upgrades are manual and driven by a single version constant.

All artifacts are pinned via `DEFAULT_PROTOC_VERSION` and `DEFAULT_CONFORMANCE_VERSION` in `packages/upstream-protobuf/`.

- **`protoc` binary** — downloaded from GitHub releases (`protocolbuffers/protobuf`).
  Provides the compiler, well-known type `.proto` files (extracted from protoc's include directory), and edition feature default resolution.
- **Conformance test runner and test protos** — downloaded from the npm `protobuf-conformance` package.
  Used to verify binary and JSON serialization correctness.

Several values from upstream descriptor definitions are duplicated in the runtime to avoid circular imports or for bootstrap reasons.
These must stay in sync when upstream changes.

## Test Conventions

**Prefer parametrized tests over subtests or branching logic.**
Use `@pytest.mark.parametrize` with `pytest.param(..., id=...)` for table-driven tests.
This gives IDE discovery, independent re-runs, and clear failure output for free.

**Use test classes for grouping, not subtests.**
When a test file has many test functions around the same concern, group them in a plain `class Test*:`.
Use flat `def test_*` functions when grouping adds no clarity.

The `.proto` files in `tests/proto/` are designed around three principles:

**One file per protobuf concept.**
Each file covers a single protobuf feature.
`scalars.proto` has every scalar type, `maps.proto` has every valid key type, `lists.proto` has a repeated field for every element type.

**Exhaustive within the domain.**
When a proto covers a concept, it covers all variants.
This means tests can parametrize across all fields of a message without needing to add proto definitions for coverage.

**Specialized over mixed.**
Use `Scalars`, `Lists`, or `Maps` for feature-specific tests.
`MixedFields` exists for tests that genuinely need a sample of every field kind (copy, init, equality, container emulation).
