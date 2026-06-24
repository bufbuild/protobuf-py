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
from __future__ import annotations

from license_header._header import DOUBLE_HASH, DOUBLE_SLASH, HASH, make_header, modify

EXPECTED_PY_HEADER = """\
#
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
#
"""

EXPECTED_SH_HEADER = """\
##
## Copyright (c) 2025-2026 Buf Technologies, Inc.
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
##
"""

EXPECTED_PROTO_HEADER = """\
// Copyright (c) 2025-2026 Buf Technologies, Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
"""


# --- Python (#) style ---


def test_make_header_py() -> None:
    result = make_header("Buf Technologies, Inc.", "2025-2026", HASH)
    assert result == EXPECTED_PY_HEADER


def test_modify_py_no_header() -> None:
    content = "import os\n\nx = 1\n"
    result = modify(content, EXPECTED_PY_HEADER, HASH)
    assert result == EXPECTED_PY_HEADER + content


def test_modify_py_correct_header_unchanged() -> None:
    content = EXPECTED_PY_HEADER + "import os\n"
    result = modify(content, EXPECTED_PY_HEADER, HASH)
    assert result == content


def test_modify_py_outdated_header_replaced() -> None:
    old_header = EXPECTED_PY_HEADER.replace("2025-2026", "2024")
    content = old_header + "import os\n"
    result = modify(content, EXPECTED_PY_HEADER, HASH)
    assert result == EXPECTED_PY_HEADER + "import os\n"


def test_modify_py_shebang_preserved() -> None:
    content = "#!/usr/bin/env python\nimport os\n"
    result = modify(content, EXPECTED_PY_HEADER, HASH)
    assert result == "#!/usr/bin/env python\n" + EXPECTED_PY_HEADER + "import os\n"


def test_modify_py_shebang_with_existing_header() -> None:
    old_header = EXPECTED_PY_HEADER.replace("2025-2026", "2024")
    content = "#!/usr/bin/env python\n" + old_header + "import os\n"
    result = modify(content, EXPECTED_PY_HEADER, HASH)
    assert result == "#!/usr/bin/env python\n" + EXPECTED_PY_HEADER + "import os\n"


def test_modify_py_encoding_preserved() -> None:
    content = "# -*- coding: utf-8 -*-\nimport os\n"
    result = modify(content, EXPECTED_PY_HEADER, HASH)
    assert result == "# -*- coding: utf-8 -*-\n" + EXPECTED_PY_HEADER + "import os\n"


def test_modify_py_shebang_and_encoding_preserved() -> None:
    content = "#!/usr/bin/env python\n# -*- coding: utf-8 -*-\nimport os\n"
    result = modify(content, EXPECTED_PY_HEADER, HASH)
    assert result == (
        "#!/usr/bin/env python\n# -*- coding: utf-8 -*-\n"
        + EXPECTED_PY_HEADER
        + "import os\n",
    )


def test_modify_py_empty_file() -> None:
    result = modify("", EXPECTED_PY_HEADER, HASH)
    assert result == EXPECTED_PY_HEADER


# --- Shell (##) style ---


def test_make_header_sh() -> None:
    result = make_header("Buf Technologies, Inc.", "2025-2026", DOUBLE_HASH)
    assert result == EXPECTED_SH_HEADER


def test_modify_sh_no_header() -> None:
    content = "echo hello\n"
    result = modify(content, EXPECTED_SH_HEADER, DOUBLE_HASH)
    assert result == EXPECTED_SH_HEADER + "echo hello\n"


def test_modify_sh_shebang_preserved() -> None:
    content = "#!/bin/bash\necho hello\n"
    result = modify(content, EXPECTED_SH_HEADER, DOUBLE_HASH)
    assert result == "#!/bin/bash\n" + EXPECTED_SH_HEADER + "echo hello\n"


def test_modify_sh_correct_header_unchanged() -> None:
    content = "#!/bin/bash\n" + EXPECTED_SH_HEADER + "echo hello\n"
    result = modify(content, EXPECTED_SH_HEADER, DOUBLE_HASH)
    assert result == content


def test_modify_sh_outdated_header_replaced() -> None:
    old_header = EXPECTED_SH_HEADER.replace("2025-2026", "2024")
    content = "#!/bin/bash\n" + old_header + "echo hello\n"
    result = modify(content, EXPECTED_SH_HEADER, DOUBLE_HASH)
    assert result == "#!/bin/bash\n" + EXPECTED_SH_HEADER + "echo hello\n"


# --- Proto (//) style ---


def test_make_header_proto() -> None:
    result = make_header("Buf Technologies, Inc.", "2025-2026", DOUBLE_SLASH)
    assert result == EXPECTED_PROTO_HEADER


def test_modify_proto_no_header() -> None:
    content = 'syntax = "proto3";\n'
    result = modify(content, EXPECTED_PROTO_HEADER, DOUBLE_SLASH)
    assert result == EXPECTED_PROTO_HEADER + 'syntax = "proto3";\n'


def test_modify_proto_correct_header_unchanged() -> None:
    content = EXPECTED_PROTO_HEADER + "\n" + 'syntax = "proto3";\n'
    result = modify(content, EXPECTED_PROTO_HEADER, DOUBLE_SLASH)
    assert result == content


def test_modify_proto_outdated_header_replaced() -> None:
    old_header = EXPECTED_PROTO_HEADER.replace("2025-2026", "2024")
    content = old_header + "\n" + 'syntax = "proto3";\n'
    result = modify(content, EXPECTED_PROTO_HEADER, DOUBLE_SLASH)
    assert result == EXPECTED_PROTO_HEADER + "\n" + 'syntax = "proto3";\n'
