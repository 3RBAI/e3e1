"""Browser actions module for chat service"""

from .models import (
    SearchAction,
    NavigateAction,
    ClickElementAction,
    InputTextAction,
    DoneAction,
    StructuredOutputAction,
    SwitchTabAction,
    CloseTabAction,
    ScrollAction,
    SendKeysAction,
    UploadFileAction,
    ExtractPageContentAction,
    NoParamsAction,
    GetDropdownOptionsAction,
    SelectDropdownOptionAction,
)
from .registry import RegisteredAction, ActionRegistry, ActionModel
from .service import Registry
from .tools import Tools, CodeAgentTools

__all__ = [
    # Models
    "SearchAction",
    "NavigateAction",
    "ClickElementAction",
    "InputTextAction",
    "DoneAction",
    "StructuredOutputAction",
    "SwitchTabAction",
    "CloseTabAction",
    "ScrollAction",
    "SendKeysAction",
    "UploadFileAction",
    "ExtractPageContentAction",
    "NoParamsAction",
    "GetDropdownOptionsAction",
    "SelectDropdownOptionAction",
    # Registry
    "RegisteredAction",
    "ActionRegistry",
    "ActionModel",
    "Registry",
    # Tools
    "Tools",
    "CodeAgentTools",
]
