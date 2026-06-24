# Copyright (c) 2025-2026 Buf Technologies, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Generates bootstrap constants for the container-emulation runtime.

Usage: generate_bootstrap <output_file>
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

from protoc import get_protoc_path


def main() -> None:
    """Generate bootstrap constants."""
    if len(sys.argv) != 2:
        sys.stderr.write(f"usage: {sys.argv[0]} <output_file>\n")
        sys.exit(2)

    output_path = Path(sys.argv[1])

    from protobuf._descriptors import DescFieldValueEnum  # noqa: PLC0415
    from protobuf.wkt._gen import descriptor_pb  # noqa: PLC0415
    from protobuf.wkt._gen.descriptor_pb import (  # noqa: PLC0415
        Edition,
        FeatureSet,
        FeatureSetDefaults,
        FieldDescriptorProto,
        MethodOptions,
    )

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp) / "edition_defaults.binpb"
        proc = subprocess.run(  # noqa: S603
            [
                get_protoc_path(),
                f"--edition_defaults_out={tmp_path}",
                "google/protobuf/descriptor.proto",
            ],
            check=False,
        )
        if proc.returncode:
            sys.exit(proc.returncode)

        all_defaults = FeatureSetDefaults.from_binary(tmp_path.read_bytes())

    # Enumerate FeatureSet fields from the descriptor so new fields added in
    # future editions are picked up automatically without editing this script.
    # TODO: This isn't quite right as we're using our already generated `FeatureSet` schema.
    # Revisit further with #413.
    feature_set_desc = next(
        (m for m in descriptor_pb.desc().messages if m.name == "FeatureSet"), None
    )
    if feature_set_desc is None:
        sys.stderr.write(
            "error: FeatureSet message not found in google/protobuf/descriptor.proto\n"
        )
        sys.exit(1)
    feature_fields = [
        f for f in feature_set_desc.fields if isinstance(f.value, DescFieldValueEnum)
    ]

    # Build per-edition feature defaults by merging overridable on top of fixed.
    edition_defaults_map: dict[int, dict[str, tuple[int, str]]] = {}
    for ed_default in all_defaults.defaults:
        edition_num = int(ed_default.edition)
        if edition_num == Edition.UNSTABLE:
            # Skip unsupported UNSTABLE edition, for tests we always collapse it to
            # the latest stable edition.
            continue
        combined: dict[str, tuple[int, str]] = {}
        for field in feature_fields:
            key = field.local_name
            fixed = ed_default.fixed_features
            overridable = ed_default.overridable_features
            val = int(getattr(overridable, key)) if overridable is not None else 0
            if val == 0:
                val = int(getattr(fixed, key)) if fixed is not None else 0
            assert isinstance(field.value, DescFieldValueEnum)  # noqa: S101
            enum_val = field.value.enum._values_by_number.get(val)
            comment = enum_val.local_name if enum_val is not None else str(val)
            combined[key] = (val, comment)
        edition_defaults_map[edition_num] = combined

    feature_key_names = [f.local_name for f in feature_fields]
    min_edition = int(all_defaults.minimum_edition)
    max_edition = int(all_defaults.maximum_edition)

    lines: list[str] = [
        "# Generated from google/protobuf/descriptor.proto. DO NOT EDIT.",
        "# Run `uv run poe bootstrap` to regenerate.",
        "from __future__ import annotations",
        "",
        "from typing import TYPE_CHECKING, Final, Literal",
        "",
        "if TYPE_CHECKING:",
        "    from collections.abc import Mapping",
        "",
        "# google.protobuf.FieldDescriptorProto.Type",
        f"_TYPE_STRING: Final[int] = {int(FieldDescriptorProto.Type.STRING)}",
        f"_TYPE_GROUP: Final[int] = {int(FieldDescriptorProto.Type.GROUP)}",
        f"_TYPE_MESSAGE: Final[int] = {int(FieldDescriptorProto.Type.MESSAGE)}",
        f"_TYPE_BYTES: Final[int] = {int(FieldDescriptorProto.Type.BYTES)}",
        f"_TYPE_ENUM: Final[int] = {int(FieldDescriptorProto.Type.ENUM)}",
        "",
        "# google.protobuf.FieldDescriptorProto.Label",
        f"_LABEL_REQUIRED: Final[int] = {int(FieldDescriptorProto.Label.REQUIRED)}",
        f"_LABEL_REPEATED: Final[int] = {int(FieldDescriptorProto.Label.REPEATED)}",
        "",
        "# google.protobuf.Edition",
        f"_EDITION_PROTO2: Final[int] = {int(Edition.PROTO2)}",
        f"_EDITION_PROTO3: Final[int] = {int(Edition.PROTO3)}",
        f"_EDITION_UNSTABLE: Final[int] = {int(Edition.UNSTABLE)}",
        "",
        "# google.protobuf.FeatureSet.EnumType",
        f"_ENUM_TYPE_OPEN: Final[int] = {int(FeatureSet.EnumType.OPEN)}",
        "",
        "# google.protobuf.FeatureSet.RepeatedFieldEncoding",
        f"_REPEATED_FIELD_ENCODING_PACKED: Final[int] = {int(FeatureSet.RepeatedFieldEncoding.PACKED)}",
        "",
        "# google.protobuf.FeatureSet.MessageEncoding",
        f"_MESSAGE_ENCODING_DELIMITED: Final[int] = {int(FeatureSet.MessageEncoding.DELIMITED)}",
        "",
        "# google.protobuf.MethodOptions.IdempotencyLevel",
        f"_IDEMPOTENCY_UNKNOWN: Final[int] = {int(MethodOptions.IdempotencyLevel.IDEMPOTENCY_UNKNOWN)}",
        "",
        "# Minimum and maximum supported editions",
        f"_MINIMUM_EDITION: Final[int] = {min_edition}  # Edition.{Edition(min_edition).name}",
        f"_MAXIMUM_EDITION: Final[int] = {max_edition}  # Edition.{Edition(max_edition).name}",
        "",
        "_FeatureKey = Literal[",
    ]
    lines.extend(f'    "{key}",' for key in feature_key_names)
    lines.extend(
        [
            "]",
            "",
            "# Sourced from descriptor.proto via protoc --edition_defaults_out.",
            "_feature_defaults: Final[Mapping[int, Mapping[_FeatureKey, int]]] = {",
        ]
    )
    for edition_num in sorted(edition_defaults_map):
        edition_name = Edition(edition_num).name
        lines.append(f"    # {edition_name}")
        lines.append(f"    {edition_num}: {{")
        for key, (val, comment) in edition_defaults_map[edition_num].items():
            lines.append(f'        "{key}": {val},  # {comment}')
        lines.append("    },")
    lines.extend(["}", ""])

    output_path.write_text("\n".join(lines))


if __name__ == "__main__":
    main()
