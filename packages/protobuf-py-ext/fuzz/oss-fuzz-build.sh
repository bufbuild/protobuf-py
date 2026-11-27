#!/usr/bin/env bash
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

# Builds the fuzz targets into ${OUT} for OSS-Fuzz, from its build.sh.
#
# The targets embed the interpreter they were built with, so this copies its
# standard library and libpython, and the Python packages the targets import,
# into ${OUT}/python where the targets look for them.

set -euo pipefail

DIR="$(CDPATH= cd "$(dirname "${0}")/../../.." && pwd)"
cd "${DIR}/packages/protobuf-py-ext"

PYTHON="$(command -v python3)"
PYTHON_HOME="${OUT}/python/home"
PYTHON_SITE="${OUT}/python/site"
: "${FUZZ_RELEASE:=target/x86_64-unknown-linux-gnu/release}"

export PYO3_PYTHON="${PYTHON}"
# The extension's release profile uses LTO for wheels, which drops the coverage
# instrumentation.
export CARGO_PROFILE_RELEASE_LTO=false
# Finds the copied libpython beside the targets.
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,-rpath,\$ORIGIN/python/home/lib"

cargo fuzz build -O --debug-assertions

for target in $(cargo fuzz list); do
  cp "${FUZZ_RELEASE}/${target}" "${OUT}/"
  # The embedded interpreter is never finalized, so leak detection is off.
  printf '[libfuzzer]\ndetect_leaks=0\n\n[asan]\ndetect_leaks=0\n' > "${OUT}/${target}.options"
done

STDLIB="$("${PYTHON}" -c 'import sysconfig; print(sysconfig.get_path("stdlib"))')"
LIBDIR="$("${PYTHON}" -c 'import sysconfig; print(sysconfig.get_config_var("LIBDIR"))')"
LIBPYTHON="$("${PYTHON}" -c 'import sysconfig; print(sysconfig.get_config_var("INSTSONAME"))')"

rm -rf "${OUT}/python"
mkdir -p "${PYTHON_HOME}/lib" "${PYTHON_SITE}/protobuf_ext"
cp "${LIBDIR}/${LIBPYTHON}" "${PYTHON_HOME}/lib/"
cp -r "${STDLIB}" "${PYTHON_HOME}/lib/"
rm -rf "${PYTHON_HOME}/lib/$(basename "${STDLIB}")/site-packages"

# Installs protobuf-py-pure with its dependencies, since it reads its version
# from its metadata.
"${PYTHON}" -m pip install --target "${PYTHON_SITE}" "${DIR}"
# Only the Python sources, as the targets link the extension.
cp protobuf_ext/*.py "${PYTHON_SITE}/protobuf_ext/"
cp -r "${DIR}/tests/conformance/gen" "${PYTHON_SITE}/"
