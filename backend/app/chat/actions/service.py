"""Registry service for managing and executing actions"""

import asyncio
import functools
import inspect
import logging
from collections.abc import Callable
from inspect import Parameter, iscoroutinefunction, signature
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, create_model

from .registry import ActionModel, ActionRegistry, RegisteredAction

Context = TypeVar('Context')
logger = logging.getLogger(__name__)


class Registry(Generic[Context]):
    """Service for registering and managing actions"""

    def __init__(self, exclude_actions: list[str] | None = None):
        self.registry = ActionRegistry()
        self.exclude_actions = exclude_actions if exclude_actions is not None else []

    def action(
        self,
        description: str,
        param_model: type[BaseModel] | None = None,
        domains: list[str] | None = None,
        allowed_domains: list[str] | None = None,
    ):
        """Decorator for registering actions"""
        final_domains = allowed_domains if allowed_domains is not None else domains

        def decorator(func: Callable):
            if func.__name__ in self.exclude_actions:
                return func

            # Create param model if not provided
            if param_model is None:
                sig = signature(func)
                params_dict = {}
                for name, param in sig.parameters.items():
                    annotation = param.annotation if param.annotation != Parameter.empty else str
                    default = ... if param.default == Parameter.empty else param.default
                    params_dict[name] = (annotation, default)
                
                actual_param_model = create_model(
                    f'{func.__name__}_Params',
                    __base__=ActionModel,
                    **params_dict
                )
            else:
                actual_param_model = param_model

            # Create wrapper for async execution
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                if iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                else:
                    return await asyncio.to_thread(func, *args, **kwargs)

            action = RegisteredAction(
                name=func.__name__,
                description=description,
                function=async_wrapper,
                param_model=actual_param_model,
                domains=final_domains,
            )
            self.registry.actions[func.__name__] = action

            return async_wrapper

        return decorator

    async def execute_action(
        self,
        action_name: str,
        params: dict,
        **kwargs: Any
    ) -> Any:
        """Execute a registered action"""
        if action_name not in self.registry.actions:
            raise ValueError(f'Action {action_name} not found')

        action = self.registry.actions[action_name]
        
        try:
            validated_params = action.param_model(**params)
            return await action.function(**validated_params.model_dump(), **kwargs)
        except Exception as e:
            logger.error(f'Error executing action {action_name}: {e}')
            raise

    def get_prompt_description(self, page_url: str | None = None) -> str:
        """Get a description of all actions for the prompt"""
        return self.registry.get_prompt_description(page_url=page_url)

    def create_action_model(
        self, 
        include_actions: list[str] | None = None, 
        page_url: str | None = None
    ) -> type[ActionModel]:
        """Creates a Union of individual action models from registered actions"""
        from typing import Union

        available_actions: dict[str, RegisteredAction] = {}
        for name, action in self.registry.actions.items():
            if include_actions is not None and name not in include_actions:
                continue

            if page_url is None:
                if action.domains is None:
                    available_actions[name] = action
                continue

            domain_is_allowed = self.registry._match_domains(action.domains, page_url)
            if domain_is_allowed:
                available_actions[name] = action

        if not available_actions:
            return create_model('EmptyActionModel', __base__=ActionModel)

        individual_action_models: list[type[BaseModel]] = []
        for name, action in available_actions.items():
            individual_model = create_model(
                f'{name.title().replace("_", "")}ActionModel',
                __base__=ActionModel,
                **{name: (action.param_model, ...)}
            )
            individual_action_models.append(individual_model)

        if len(individual_action_models) == 1:
            return individual_action_models[0]

        union_type = Union[tuple(individual_action_models)]
        return create_model('ActionModelUnion', __base__=ActionModel, root=(union_type, ...))
