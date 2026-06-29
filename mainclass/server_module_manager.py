import os
import json


class ServerModuleManager:
    """Discover and manage post-exploit modules stored under a 'modules/' folder.

    Each subfolder of `modules/` must contain a `config.json` with the keys:
    {"name": "KEYLOGGER", "description": "...", "file_name": "keylogger.py"}

    The manager maps the uppercase `name` to the absolute payload path.
    """

    def __init__(self, modules_directory="modules"):
        self.modules_directory = os.path.abspath(modules_directory)
        self._module_index = {}  # COMMAND -> {"path":..., "description":..., "file_name":...}
        self.discover_modules()

    def discover_modules(self):
        """Scan the modules directory and populate the internal index.

        Missing or malformed modules are skipped silently to keep output tight.
        """
        self._module_index.clear()
        if not os.path.isdir(self.modules_directory):
            return

        for entry in os.listdir(self.modules_directory):
            entry_path = os.path.join(self.modules_directory, entry)
            if not os.path.isdir(entry_path):
                continue

            config_path = os.path.join(entry_path, "config.json")
            if not os.path.isfile(config_path):
                continue

            try:
                with open(config_path, "r", encoding="utf-8") as fh:
                    config = json.load(fh)
                name = str(config.get("name", "")).strip().upper()
                description = str(config.get("description", "")).strip()
                file_name = str(config.get("file_name", "")).strip()
                if not name or not file_name:
                    continue

                payload_path = os.path.join(entry_path, file_name)
                payload_path = os.path.abspath(payload_path)
                if not os.path.exists(payload_path):
                    continue

                placeholders = config.get("placeholders", {})
                if not isinstance(placeholders, dict):
                    placeholders = {}

                controller = config.get("controller", {})
                if not isinstance(controller, dict):
                    controller = {}

                build = config.get("build", {})
                if not isinstance(build, dict):
                    build = {}

                self._module_index[name] = {
                    "path": payload_path,
                    "description": description,
                    "file_name": file_name,
                    "module_folder": entry_path,
                    "placeholders": placeholders,
                    "controller": controller,
                    "build": build,
                }
            except Exception:
                # Keep discovery quiet and robust; malformed configs are ignored
                continue

    def get_module_path(self, command_trigger):
        """Return the absolute path for the given command trigger (case-insensitive).

        Returns None if not found.
        """
        if not command_trigger:
            return None
        return self._module_index.get(command_trigger.strip().upper(), {}).get("path")

    def list_commands(self):
        """Return a list of (command, description) tuples sorted by command."""
        return sorted(((k, v.get("description", "")) for k, v in self._module_index.items()), key=lambda x: x[0])

    def get_module_entry(self, command_trigger):
        """Return a module entry dict for a strict command trigger."""
        if not command_trigger:
            return None
        command = command_trigger.strip().upper()
        entry = self._module_index.get(command)
        if not entry:
            return None
        return {
            "command": command,
            "description": entry.get("description", ""),
            "path": entry.get("path"),
            "file_name": entry.get("file_name"),
            "module_folder": entry.get("module_folder"),
            "placeholders": entry.get("placeholders", {}),
            "controller": entry.get("controller", {}),
            "build": entry.get("build", {}),
        }

    def get_module_entries(self):
        """Return all discovered module entries as a list of dicts."""
        return [self.get_module_entry(command) for command, _ in self.list_commands()]

    def help_menu(self):
        """Return a vertically-compact help menu string describing available modules."""
        lines = []
        lines.append("Available post-exploit modules:")
        for command, description in self.list_commands():
            if description:
                lines.append("  {0} : {1}".format(command, description))
            else:
                lines.append("  {0}".format(command))
        return "\n".join(lines)

    def print_help(self):
        """Print the help menu with tight vertical spacing."""
        print(self.help_menu())

    def get_template_values_path(self, module_entry):
        """Return the stored template values path for a module, if available."""
        if not module_entry or not module_entry.get("module_folder"):
            return None
        return os.path.join(module_entry["module_folder"], "template.json")

    def load_template_values(self, module_entry):
        """Load saved placeholder values for a module."""
        values_path = self.get_template_values_path(module_entry)
        if not values_path or not os.path.isfile(values_path):
            return {}
        try:
            with open(values_path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            if isinstance(data, dict):
                return data
        except Exception:
            pass
        return {}

    def save_template_values(self, module_entry, values):
        """Persist placeholder values for a module."""
        values_path = self.get_template_values_path(module_entry)
        if not values_path or not isinstance(values, dict):
            return False
        try:
            with open(values_path, "w", encoding="utf-8") as fh:
                json.dump(values, fh, indent=2)
            return True
        except Exception:
            return False


if __name__ == "__main__":
    mgr = ServerModuleManager()
    mgr.print_help()
