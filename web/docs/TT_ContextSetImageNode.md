## TT Context Set Image *TT_ContextSetImageNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Sets the image field in an existing context object.

### Inputs

| Parameter | Type       | Required | Description              |
|-----------|------------|----------|--------------------------|
| `context` | TT_CONTEXT | Yes      | Context object to update |
| `image`   | IMAGE      | Yes      | Pixel-space image        |

### Outputs

| Parameter | Type       | Description              |
|-----------|------------|--------------------------|
| `CONTEXT` | TT_CONTEXT | Updated context object   |

### Usage

Use this node to store a decoded or loaded image in the context for use by downstream nodes.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
