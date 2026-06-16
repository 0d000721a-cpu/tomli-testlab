"""Run tests with coverage from scratch"""
import coverage, sys, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

cov = coverage.Coverage(source=['tomli'])
cov.start()

import pytest
exit_code = pytest.main(['-v', '--tb=short'])

cov.stop()
cov.save()

# Generate reports
os.makedirs('reports', exist_ok=True)
cov.html_report(directory='reports/coverage_html')
cov.xml_report(outfile='reports/coverage.xml')

# Print summary
total = cov.report(show_missing=True, skip_covered=False)
print(f'\nCoverage: {total:.1f}%')
print(f'Report: reports/coverage_html/index.html')
print(f'XML: reports/coverage.xml')
sys.exit(exit_code)
