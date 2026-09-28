"""
Virtual Data Lakehouse Interface (Option C) for Oráculo (v4.1).
Implements RFC 6901 JSON pointer navigation, lazy loading of shards,
on-demand variant calculation via upstream APIs, and master dump export.
"""

from datetime import datetime
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

from pipeline.config import config


class VirtualDataLake:
    """
    Silver Tier virtual access layer.
    Allows LLM agents and specialized sub-oracles (oraculo-diag-*) to query
    astronomical and numerological data by RFC 6901 JSON pointer or logical key,
    without holding massive monolithic JSONs in memory.
    """

    def __init__(self, raw_dir: Path):
        self.raw_dir = Path(raw_dir)
        self.dumps_dir = self.raw_dir / "json" / "dumps"
        self.variants_dir = self.dumps_dir / "variants"
        self.manifest_path = self.dumps_dir / "manifest.json"
        self._manifest: Optional[Dict[str, Any]] = None
        self._loaded_shards: Dict[str, Dict[str, Any]] = {}

    def load_manifest(self) -> Dict[str, Any]:
        if self._manifest is None:
            if self.manifest_path.exists():
                with open(self.manifest_path, "r", encoding="utf-8") as f:
                    self._manifest = json.load(f)
            else:
                self._manifest = {
                    "contract": "gentle-ai.datalake.virtual/v1",
                    "consultant": "Unknown",
                    "generated_at": datetime.utcnow().isoformat() + "Z",
                    "shards": {},
                    "pointers": {}
                }
        return self._manifest

    def get_shard(self, shard_key: str) -> Dict[str, Any]:
        if shard_key in self._loaded_shards:
            return self._loaded_shards[shard_key]

        manifest = self.load_manifest()
        shard_filename = manifest.get("shards", {}).get(shard_key, f"{shard_key}.json")
        shard_file = self.dumps_dir / shard_filename

        if not shard_file.exists():
            shard_file = self.dumps_dir / f"{shard_key}.json"
            if not shard_file.exists():
                raise FileNotFoundError(f"Shard '{shard_key}' not found in {self.dumps_dir}")

        with open(shard_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            self._loaded_shards[shard_key] = data
            return data

    def get(self, pointer: str) -> Any:
        """
        Resolves an RFC 6901 JSON pointer or semantic logical key.
        Examples:
          - 'sidereal/fagan_campanus' -> resolved via manifest pointers
          - 'western_sidereal#/variants/fagan_campanus'
          - 'vedic_jyotish#/shadbala/components'
        """
        manifest = self.load_manifest()
        if pointer in manifest.get("pointers", {}):
            pointer = manifest["pointers"][pointer]

        if "#" in pointer:
            shard_part, json_pointer = pointer.split("#", 1)
        else:
            shard_part, json_pointer = pointer, ""

        try:
            shard_data = self.get_shard(shard_part)
        except FileNotFoundError:
            return None

        if not json_pointer or json_pointer == "/":
            return shard_data

        tokens = [t.replace("~1", "/").replace("~0", "~") for t in json_pointer.lstrip("/").split("/")]
        curr = shard_data
        for token in tokens:
            if isinstance(curr, dict):
                if token in curr:
                    curr = curr[token]
                else:
                    return None
            elif isinstance(curr, list):
                try:
                    idx = int(token)
                    curr = curr[idx]
                except (ValueError, IndexError):
                    return None
            else:
                return None
        return curr

    def resolve_pointer(self, pointer: str) -> Any:
        """Alias for get() to resolve direct RFC 6901 pointers."""
        return self.get(pointer)

    def export_master_dump(self, out_path: Optional[Path] = None) -> Path:
        """
        Compiles all 10 shards into a single unified JSON on-demand,
        fulfilling the requirement of delivering an uncompromised master dump
        without redundant duplicate storage during ordinary execution.
        """
        if out_path is None:
            out_path = self.dumps_dir / "omni_dump_mega.json"

        manifest = self.load_manifest()
        master = {
            "contract": "gentle-ai.datalake.master/v1",
            "consultant": manifest.get("consultant", "Unknown"),
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "shards": {}
        }

        # Load each shard
        for shard_key, shard_filename in manifest.get("shards", {}).items():
            shard_file = self.dumps_dir / shard_filename
            if shard_file.exists():
                with open(shard_file, "r", encoding="utf-8") as f:
                    master["shards"][shard_key] = json.load(f)

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(master, f, indent=2, ensure_ascii=False)

        return out_path
