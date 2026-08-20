"""Zip a Harbor task package so the Shannon QC platform can read it.

PowerShell's Compress-Archive omits directory entries; the QC platform walks the archive by
those entries, fails to find tests/ solution/ environment/, gives up on bundle detection and
reports a misleading "upload contains N JSON files". This writes them explicitly.

    python tools/zip_package.py <task-folder> [--no-evaluations]
"""
import os, sys, zipfile

def build(pkg_dir, out, skip_eval=False):
    parent = os.path.dirname(os.path.abspath(pkg_dir)) or "."
    name = os.path.basename(os.path.abspath(pkg_dir))
    cwd = os.getcwd()
    os.chdir(parent)
    try:
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
            for root, dirs, files in os.walk(name):
                rel = os.path.relpath(root, ".").replace(os.sep, "/")
                if skip_eval and "/evaluations" in "/" + rel:
                    dirs[:] = []
                    continue
                dirs[:] = [d for d in dirs if d not in ("__pycache__", ".pytest_cache")]
                z.writestr(zipfile.ZipInfo(rel + "/"), b"")
                for f in sorted(files):
                    z.write(os.path.join(root, f), rel + "/" + f)
        ns = zipfile.ZipFile(out).namelist()
        d = sum(1 for n in ns if n.endswith("/"))
        print(f"{out}: {d} dir-entries, {len(ns)-d} files")
    finally:
        os.chdir(cwd)

if __name__ == "__main__":
    pkg = sys.argv[1]
    skip = "--no-evaluations" in sys.argv
    out = os.path.abspath(pkg) + ("_REVIEW.zip" if skip else "_FINAL.zip")
    build(pkg, out, skip)
