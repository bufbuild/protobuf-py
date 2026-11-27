use std::process::Command;

fn main() {
    pyo3_build_config::use_pyo3_cfgs();
    // The targets embed the interpreter, so they need to find libpython at
    // runtime.
    pyo3_build_config::add_libpython_rpath_link_args();

    // The embedded interpreter cannot find its home from the fuzz target's
    // path, so it uses the one of the interpreter it was built with, and that
    // interpreter's site-packages for protobuf-py's dependencies.
    let python = pyo3_build_config::get()
        .executable()
        .expect("pyo3 found an interpreter");
    let output = Command::new(python)
        .args([
            "-c",
            "import sys, sysconfig; print(sys.base_prefix); print(sysconfig.get_path('purelib'))",
        ])
        .output()
        .expect("the interpreter runs");
    assert!(
        output.status.success(),
        "the interpreter failed: {output:?}"
    );
    let stdout = String::from_utf8(output.stdout).expect("the paths are UTF-8");
    let mut lines = stdout.lines();
    let home = lines.next().expect("the interpreter prints its home");
    let site = lines
        .next()
        .expect("the interpreter prints its site-packages");
    println!("cargo::rustc-env=PROTOBUF_PY_FUZZ_PYTHONHOME={home}");
    println!("cargo::rustc-env=PROTOBUF_PY_FUZZ_SITE={site}");
    let repo = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("../../..")
        .canonicalize()
        .expect("the repository exists");
    println!("cargo::rustc-env=PROTOBUF_PY_FUZZ_REPO={}", repo.display());
    println!("cargo::rerun-if-env-changed=PYO3_PYTHON");
    println!("cargo::rerun-if-env-changed=VIRTUAL_ENV");
}
