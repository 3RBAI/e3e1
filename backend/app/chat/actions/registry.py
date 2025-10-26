"""Action registry for managing browser actions"""

from collections.abc import Callable
from typing import TYPE_CHECKING, Any
from pydantic import BaseModel, ConfigDict


if TYPE_CHECKING:
    pass


class RegisteredAction(BaseModel):
    """Model for a registered action"""

    name: str
    description: str
    function: Callable
    param_model: type[BaseModel]

    # filters: provide specific domains to determine whether the action should be available on the given URL or not
    domains: list[str] | None = None  # e.g. ['*.google.com', 'www.bing.com', 'yahoo.*]

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def prompt_description(self) -> str:
        """Get a description of the action for the prompt in unstructured format"""
        schema = self.param_model.model_json_schema()
        params = []

        if 'properties' in schema:
            for param_name, param_info in schema['properties'].items():
                # Build parameter description
                param_desc = param_name

                # Add type information if available
                if 'type' in param_info:
                    param_type = param_info['type']
                    param_desc += f'={param_type}'

                # Add description as comment if available
                if 'description' in param_info:
                    param_desc += f' ({param_info["description"]})'

                params.append(param_desc)

        # Format: action_name: Description. (param1=type, param2=type, ...)
        if params:
            return f'{self.name}: {self.description}. ({", ".join(params)})'
        else:
            return f'{self.name}: {self.description}'


class ActionModel(BaseModel):
    """Base model for dynamically created action models"""

    model_config = ConfigDict(arbitrary_types_allowed=True, extra='forbid')

    def get_index(self) -> int | None:
        """Get the index of the action"""
        params = self.model_dump(exclude_unset=True).values()
        if not params:
            return None
        for param in params:
            if param is not None and 'index' in param:
                return param['index']
        return None

    def set_index(self, index: int):
        """Overwrite the index of the action"""
        action_data = self.model_dump(exclude_unset=True)
        action_name = next(iter(action_data.keys()))
        action_params = getattr(self, action_name)

        if hasattr(action_params, 'index'):
            action_params.index = index


class ActionRegistry(BaseModel):
    """Model representing the action registry"""

    actions: dict[str, RegisteredAction] = {}

    @staticmethod
    def _match_domains(domains: list[str] | None, url: str) -> bool:
        """Match a list of domain glob patterns against a URL"""
        if domains is None or not url:
            return True

        # Simple domain matching (can be enhanced with glob patterns)
        from urllib.parse import urlparse
        
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            
            for domain_pattern in domains:
                # Simple wildcard matching
                if domain_pattern.startswith('*.'):
                    if domain.endswith(domain_pattern[2:]):
                        return True
                elif domain_pattern.endswith('.*'):
                    if domain.startswith(domain_pattern[:-2]):
                        return True
                elif domain == domain_pattern:
                    return True
        except Exception:
            return False
            
        return False

    def get_prompt_description(self, page_url: str | None = None) -> str:
        """Get a description of all actions for the prompt"""
        if page_url is None:
            return '\n'.join(
                action.prompt_description() 
                for action in self.actions.values() 
                if action.domains is None
            )

        filtered_actions = []
        for action in self.actions.values():
            if not action.domains:
                continue

            if self._match_domains(action.domains, page_url):
                filtered_actions.append(action)

        return '\n'.join(action.prompt_description() for action in filtered_actions)
