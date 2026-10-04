# ==============================================================================
# Pipeline Config for Oráculo (SSoT v4.0 - Python 3.12)
# Multi-environment variable resolution with casing tolerance & masking.
# ==============================================================================
import os
import subprocess
from pathlib import Path
from dataclasses import dataclass, field


def load_env_file(env_path: str = "/etc/environment") -> dict:
    """Reads platform environment variables safely and loads keys into os.environ if not already present."""
    loaded = dict(os.environ)
    p = Path(env_path)
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip("'\"")
                if key and val:
                    loaded[key] = val
                    if key not in os.environ:
                        os.environ[key] = val

    # Source zeropsenv.sh if present
    zp_env = Path("/var/www/zeropsenv.sh")
    if zp_env.exists():
        try:
            env_out = subprocess.check_output(
                ["bash", "-c", "source /var/www/zeropsenv.sh 2>/dev/null && env -0"],
                timeout=5
            )
            for entry in env_out.decode("utf-8", errors="ignore").split("\0"):
                if "=" in entry:
                    zk, zv = entry.split("=", 1)
                    if zk not in os.environ:
                        os.environ[zk] = zv
                        loaded[zk] = zv
        except Exception:
            pass

    return loaded


def _get_key_tolerant(*var_names: str, default: str = "") -> str:
    """Checks multiple variable name variants (UPPER_CASE, camelCase, lowercase)."""
    for v in var_names:
        val = os.getenv(v)
        if val and val.strip():
            return val.strip()
    return default


@dataclass
class PipelineConfig:
    freeastro_api_key: str = field(default_factory=lambda: _get_key_tolerant("FREEASTRO_API_KEY", "FREEASTROAPI_KEY", "freeastroapi_key"))
    astrology_api_key: str = field(default_factory=lambda: _get_key_tolerant("ASTROLOGY_API_IO", "astrology_api_io", "ASTROLOGY_API_KEY", "astrology_apiKey", "astrologyapi_key"))
    vedastro_api_key: str = field(default_factory=lambda: _get_key_tolerant("VEDASTRO_API_KEY", "vedastro_apiKey", "VEDASTRO_KEY"))
    astroway_api_key: str = field(default_factory=lambda: _get_key_tolerant("ASTROWAY_API_KEY", "astroway_apiKey", "ASTROWAY_KEY"))
    kundali_mcp_key: str = field(default_factory=lambda: _get_key_tolerant("KUNDALI_MCP_KEY", "kundali_mcpKey", "KUNDALI_KEY"))
    nasa_api_key: str = field(default_factory=lambda: _get_key_tolerant("NASA_API_KEY", "nasa_apiKey", default="DEMO_KEY"))
    
    # Base URLs
    freeastro_url: str = "https://api.freeastroapi.com"
    astrology_url: str = "https://api.astrology-api.io"
    astroway_url: str = "https://api.astroway.info"
    vedastro_url: str = "https://api.vedastro.org"
    hebcal_url: str = "https://www.hebcal.com"
    nasa_horizons_url: str = "https://ssd.jpl.nasa.gov/api/horizons.api"

    def mask_key(self, key: str) -> str:
        if not key or key == "DEMO_KEY":
            return "<UNSET/DEMO>"
        if len(key) <= 8:
            return "***"
        return f"{key[:4]}...{key[-4:]}"

    def report_status(self) -> dict:
        return {
            "FREEASTRO_API_KEY": self.mask_key(self.freeastro_api_key),
            "ASTROLOGY_API_IO": self.mask_key(self.astrology_api_key),
            "VEDASTRO_API_KEY": self.mask_key(self.vedastro_api_key),
            "ASTROWAY_API_KEY": self.mask_key(self.astroway_api_key),
            "KUNDALI_MCP_KEY": self.mask_key(self.kundali_mcp_key),
            "NASA_API_KEY": self.mask_key(self.nasa_api_key),
        }


# Auto-load on import
load_env_file()
config = PipelineConfig()
