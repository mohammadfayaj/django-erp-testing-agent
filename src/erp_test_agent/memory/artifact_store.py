"""Artifact store: manages directories for screenshots, traces, videos, reports."""

from __future__ import annotations

from pathlib import Path


class ArtifactStore:
    """Creates and provides the directory layout for run artifacts."""

    def __init__(self, base_dir: Path | str = "./artifacts") -> None:
        self.base_dir = Path(base_dir)

    def _subdir(self, name: str) -> Path:
        path = self.base_dir / name
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def runs_dir(self) -> Path:
        return self._subdir("runs")

    @property
    def screenshots_dir(self) -> Path:
        return self._subdir("screenshots")

    @property
    def traces_dir(self) -> Path:
        return self._subdir("traces")

    @property
    def videos_dir(self) -> Path:
        return self._subdir("videos")

    @property
    def reports_dir(self) -> Path:
        return self._subdir("reports")

    def run_dir(self, run_id: str) -> Path:
        path = self.runs_dir / run_id
        path.mkdir(parents=True, exist_ok=True)
        return path
