## TT Base Context Passthrough *TT_BaseContextPassthroughNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Passes a TT_CONTEXT object through without modification. Useful as a no-op placeholder or breakpoint in
context-driven pipelines.

### Inputs

| Parameter | Type       | Required | Description                    |
|-----------|------------|----------|--------------------------------|
| `context` | TT_CONTEXT | Yes      | Context object to pass through |

### Outputs

| Parameter | Type       | Description              |
|-----------|------------|--------------------------|
| `CONTEXT` | TT_CONTEXT | Unchanged context object |

### Usage

Use this node when you need a context node in the graph but don't need to modify the context.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
