# sdtp/plugin_loader.py
import importlib.metadata
import logging

def load_external_table_plugins():
    """Scans the environment for packages registering sdtp.tables entry points"""
    entries = importlib.metadata.entry_points(group='sdtp.tables')
    for entry in entries:
        try:
            # This triggers the factory class execution, running its registration logic
            factory_class = entry.load()
            logging.info(f"Successfully loaded external SDTP factory: {entry.name}")
        except Exception as e:
            logging.error(f"Failed to load SDTP table plugin '{entry.name}': {e}")