import json, yaml, posixpath
import pandas as pd
from io import StringIO

class DataHandler:
    def __init__(self, filesystem, root_path):
        self.filesystem = filesystem
        self.root_path = root_path

    def _join(self, *args):
        return posixpath.join(*args)

    def _resolve_path(self, relative_path):
        return self._join(self.root_path, relative_path)

    def exists(self, relative_path):
        full_path = self._resolve_path(relative_path)
        return self.filesystem.exists(full_path)

    def read_text(self, relative_path):
        full_path = self._resolve_path(relative_path)
        with self.filesystem.open(full_path, "r", encoding='utf-8') as f:
            return f.read()

    def read_binary(self, relative_path):
        full_path = self._resolve_path(relative_path)
        with self.filesystem.open(full_path, "rb") as f:
            return f.read()

    def write_text(self, relative_path, content):
        full_path = self._resolve_path(relative_path)
        with self.filesystem.open(full_path, "w", encoding='utf-8') as f:
            f.write(content)

    def write_binary(self, relative_path, content):
        full_path = self._resolve_path(relative_path)
        with self.filesystem.open(full_path, "wb") as f:
            f.write(content)

    # ---------------------------------------------------------
    # ✔️ KORREKTE LOAD-METHODE (KEIN FileNotFoundError MEHR)
    # ---------------------------------------------------------
    def load(self, relative_path, initial_value=None, **load_args):
        # Datei existiert nicht → initial_value oder [] zurückgeben
        if not self.exists(relative_path):
            return initial_value if initial_value is not None else []

        ext = posixpath.splitext(relative_path)[-1].lower()

        try:
            if ext == ".json":
                return json.loads(self.read_text(relative_path))
            elif ext in [".yaml", ".yml"]:
                return yaml.safe_load(self.read_text(relative_path))
            elif ext == ".csv":
                return pd.read_csv(StringIO(self.read_text(relative_path)), **load_args)
            elif ext == ".txt":
                return self.read_text(relative_path)
            else:
                return self.read_binary(relative_path)
        except Exception:
            return initial_value if initial_value is not None else []

    # ---------------------------------------------------------
    # SAVE-METHODE
    # ---------------------------------------------------------
    def save(self, relative_path, content):
        full_path = self._resolve_path(relative_path)
        parent_dir = posixpath.dirname(full_path)

        if not self.filesystem.exists(parent_dir):
            self.filesystem.mkdirs(parent_dir, exist_ok=True)

        ext = posixpath.splitext(relative_path)[-1].lower()

        if isinstance(content, pd.DataFrame) and ext == ".csv":
            self.write_text(relative_path, content.to_csv(index=False))
        elif isinstance(content, (dict, list)) and ext == ".json":
            self.write_text(relative_path, json.dumps(content, indent=4))
        elif isinstance(content, (dict, list)) and ext in [".yaml", ".yml"]:
            self.write_text(relative_path, yaml.dump(content, default_flow_style=False))
        elif isinstance(content, str) and ext == ".txt":
            self.write_text(relative_path, content)
        elif isinstance(content, bytes):
            self.write_binary(relative_path, content)
        else:
            raise ValueError(f"Unsupported content type for extension {ext}")
