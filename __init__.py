# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

# import glob
# import re

from .node_mappings import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS, NODES_COUNT, RESET, BRIGHT_GREEN, BRIGHT_CYAN, CYAN, YELLOW


# def count_tt_classes():
#     total = 0
#     for path in sorted(glob.glob("nodes_*.py")):
#         count = sum(1 for line in open(path) if re.match(r"^class TT_", line))
#         total += count
#
#     return total


WEB_DIRECTORY = "./web"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']

print()
SEP = f"{CYAN}{'=' * 60}{RESET}"
print(SEP)
print(f"{YELLOW}TenserTensor ComfyUI Nodes Pack (v1.7.8): {BRIGHT_GREEN}{NODES_COUNT} Nodes Loaded{RESET}")
print(SEP)
print(f"{BRIGHT_CYAN}[V] Repository: https://github.com/tenser-tensor/ComfyUI-TenserTensor{RESET}")
print(f"{BRIGHT_CYAN}[V] ComfyUI Registry: https://registry.comfy.org/publishers/tenser-tensor{RESET}")
print(f"{BRIGHT_CYAN}[V] Please check README file: https://github.com/tenser-tensor/ComfyUI-TenserTensor/blob/main/README.md{RESET}")
print(SEP)
print()
