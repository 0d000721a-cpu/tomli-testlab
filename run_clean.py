"""Run in a subprocess to avoid pre-imported tomli"""
import subprocess, sys, os

script = r'''
import coverage, sys, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

cov = coverage.Coverage(source=["tomli"])
cov.start()

import pytest
ec = pytest.main(["-v", "--tb=short"])

cov.stop()
cov.save()

os.makedirs("reports", exist_ok=True)
cov.html_report(directory="reports/coverage_html")
cov.xml_report(outfile="reports/coverage.xml")
total = cov.report(show_missing=True, skip_covered=False)
print(f"\n=== TOTAL COVERAGE: {total:.1f}% ===")
sys.exit(ec)
'''

result = subprocess.run(
    [sys.executable, '-c', script],
    capture_output=True, text=True, timeout=30
)
print(result.stdout[-3000:] if len(result.stdout) > 3000 else result.stdout)
if result.stderr:
    print('STDERR:', result.stderr[-1000:])
print(f'\nExit code: {result.returncode}')
