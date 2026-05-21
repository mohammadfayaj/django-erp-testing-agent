"""HTML report generator using Jinja2."""

from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from erp_test_agent.domain.models import RunResult
from erp_test_agent.utils.logging import logger

_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>ERP Test Report – {{ result.run_id }}</title>
<style>
  body { font-family: Arial, sans-serif; margin: 2rem; }
  h1 { color: #333; }
  .passed { color: green; } .failed { color: red; }
  table { border-collapse: collapse; width: 100%; margin-top: 1rem; }
  th, td { border: 1px solid #ccc; padding: 0.5rem 1rem; text-align: left; }
  th { background: #f0f0f0; }
  .badge-passed { background: #d4edda; color: #155724; padding: 2px 8px; border-radius: 4px; }
  .badge-failed { background: #f8d7da; color: #721c24; padding: 2px 8px; border-radius: 4px; }
</style>
</head>
<body>
<h1>ERP Test Report</h1>
<dl>
  <dt>Run ID</dt><dd>{{ result.run_id }}</dd>
  <dt>Plan</dt><dd>{{ result.plan.name }}</dd>
  <dt>Department</dt><dd>{{ result.plan.department }}</dd>
  <dt>Role</dt><dd>{{ result.plan.role }}</dd>
  <dt>Environment</dt><dd>{{ result.plan.environment }}</dd>
  <dt>Status</dt>
  <dd>
    {% if result.status.value == 'passed' %}
    <span class="badge-passed">PASSED</span>
    {% else %}
    <span class="badge-failed">{{ result.status.value | upper }}</span>
    {% endif %}
  </dd>
  <dt>Started</dt><dd>{{ result.started_at }}</dd>
  <dt>Finished</dt><dd>{{ result.finished_at }}</dd>
  <dt>Duration</dt><dd>{{ "%.0f" | format(result.duration_ms) }} ms</dd>
  <dt>Steps Passed</dt><dd class="passed">{{ result.passed }}</dd>
  <dt>Steps Failed</dt><dd class="failed">{{ result.failed }}</dd>
</dl>

<h2>Step Results</h2>
<table>
  <thead>
    <tr>
      <th>#</th><th>Action</th><th>Status</th><th>Attempt</th>
      <th>Duration (ms)</th><th>Error</th><th>Screenshot</th>
    </tr>
  </thead>
  <tbody>
  {% for r in result.step_results %}
    <tr>
      <td>{{ loop.index }}</td>
      <td>{{ r.step.action }}</td>
      <td>
        {% if r.status.value == 'passed' %}
        <span class="badge-passed">PASSED</span>
        {% else %}
        <span class="badge-failed">{{ r.status.value | upper }}</span>
        {% endif %}
      </td>
      <td>{{ r.attempt }}</td>
      <td>{{ "%.0f" | format(r.duration_ms) }}</td>
      <td>{{ r.error or "" }}</td>
      <td>{% if r.screenshot %}<a href="{{ r.screenshot }}">📷</a>{% endif %}</td>
    </tr>
  {% endfor %}
  </tbody>
</table>
</body>
</html>
"""


def render_html_report(result: RunResult, output_path: Path) -> Path:
    """Render an HTML report for *result* and write it to *output_path*."""
    env = Environment(autoescape=select_autoescape())
    template = env.from_string(_TEMPLATE)
    html = template.render(result=result)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    logger.info(f"[html_report] Written: {output_path}")
    return output_path
