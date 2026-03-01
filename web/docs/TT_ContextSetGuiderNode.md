## TT Context Set Guider *TT_ContextSetGuiderNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Sets the guider field in an existing context object.

### Inputs

| Parameter | Type       | Required | Description              |
|-----------|------------|----------|--------------------------|
| `context` | TT_CONTEXT | Yes      | Context object to update |
| `guider`  | GUIDER     | Yes      | Guider object            |

### Outputs

| Parameter | Type       | Description            |
|-----------|------------|------------------------|
| `CONTEXT` | TT_CONTEXT | Updated context object |

### Usage

Use this node to inject a guider into an existing context, typically after encoding text with a CLIP encoder node.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
