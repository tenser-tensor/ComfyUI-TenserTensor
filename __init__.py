# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

from .node_mappings import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS, RESET, BRIGHT_GREEN, BRIGHT_CYAN, CYAN, YELLOW

WEB_DIRECTORY = "./web"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']

SEP = f"{CYAN}{'=' * 60}{RESET}"
print(SEP)
print(f"{YELLOW}TenserTensor ComfyUI Nodes Pack (v1.3.1): {BRIGHT_GREEN}38 Nodes Loaded{RESET}")
print(SEP)
print(f"{BRIGHT_CYAN}[V] Repository: https://github.com/tenser-tensor/ComfyUI-TenserTensor{RESET}")
print(f"{BRIGHT_CYAN}[V] ComfyUI Registry: https://registry.comfy.org/publishers/tenser-tensor{RESET}")
print(f"{BRIGHT_CYAN}[V] Please check README file: https://github.com/tenser-tensor/ComfyUI-TenserTensor/blob/main/README.md{RESET}")
print(SEP)
