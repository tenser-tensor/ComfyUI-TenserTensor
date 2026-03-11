## TT Image Loader / Resizer *TT_ImageLoaderResizerNode*

*This description was generated with AI assistance. If you spot any errors, please create an issue on GitHub.*

Loads an image from the input directory with optional resizing to a target megapixel count and alpha mask extraction.

### Inputs

| Parameter        | Type    | Required | Description                                                           |
|------------------|---------|----------|-----------------------------------------------------------------------|
| `resize_image`   | BOOLEAN | Yes      | Scale image to target megapixels (Scale) or keep original size (Keep) |
| `resize_method`  | COMBO   | No       | Interpolation method for resizing (advanced)                          |
| `dimension_step` | INT     | No       | Align output dimensions to this step size, 1–256 (advanced)           |
| `megapixels`     | COMBO   | No       | Target resolution in megapixels (advanced)                            |
| `create_mask`    | BOOLEAN | Yes      | Extract alpha channel as mask (Mask) or return empty mask (Empty)     |
| `image`          | COMBO   | Yes      | Image file to load, with upload support                               |

### Outputs

| Parameter | Type  | Description                                        |
|-----------|-------|----------------------------------------------------|
| `IMAGE`   | IMAGE | Loaded (and optionally resized) image tensor       |
| `MASK`    | MASK  | Alpha channel mask, or empty mask if not extracted |

### Usage

Load an image from the input directory and optionally resize it to a target megapixel count. When resizing is enabled, both the image and mask are
scaled together. Use `dimension_step` to snap output dimensions to a specific grid — useful for models that require dimensions divisible by 8 or 64.

---

[View on GitHub](https://github.com/tenser-tensor/ComfyUI-TenserTensor)
