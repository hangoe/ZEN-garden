"""Plugin loader.

Import plugin modules from a package and update their config dictionaries
according to the user's configuration (as defined in config.json).
"""

import importlib
import importlib.metadata
from types import ModuleType

from zen_garden.plugin_system.events import EventPublisher


def register_plugins(
    plugins_config: dict[str, dict], source_package: str = "zen_garden.plugins"
) -> dict[str, ModuleType]:
    """Import plugin modules and apply provided configurations.

    Upon import all callables are registered to their respective events. The plugin's
    `config` dictionary is updated with the provided configuration.

    Args:
        plugins_config (dict[str, dict]): Mapping of plugin name to config dict.
        source_package (str): Root package where plugin packages live.

    Returns:
        dict[str, ModuleType]: Mapping of plugin name to the imported module.

    Example:

        >>> plugins_config = {"ExamplePlugin": {"param1": "value1", "param2": "value2"}}
        >>> register_plugins(plugins_config)
    """
    entry_points = {
        ep.name: ep
        for ep in importlib.metadata.entry_points(group="zen_garden.plugins")
    }
    output = {}
    for plugin, config in plugins_config.items():
        if plugin in entry_points:
            module = entry_points[plugin].load()
        else:
            module = importlib.import_module(name=f"{source_package}.{plugin}.plugin")
        module.config.update(config)
        output[plugin] = module
    return output


def deregister_plugins():
    EventPublisher.deregister_all()
