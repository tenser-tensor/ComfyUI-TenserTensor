## TT Context Passthrough *TT_ContextPassthrough*

⚠️ Deprecated: This node will be removed in version 3.0. Please migrate to the new context nodes.

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Pass-through node that forwards context while allowing optional parameter modifications.

### Inputs

| Parameter | Type       | Required | Description                   |
|-----------|------------|----------|-------------------------------|
| `context` | TT_CONTEXT | Yes      | Input context to pass through |

### Outputs

| Parameter | Type       | Description                                 |
|-----------|------------|---------------------------------------------|
| `CONTEXT` | TT_CONTEXT | Context with optionally modified parameters |

### Usage

Use this node to pass context through your workflow while optionally modifying specific parameters without changing the
rest of the context.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
