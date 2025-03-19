# Script to convert Fang preprint to markdown

## This script was run on March 18th, 2024

```bash
cd ~/code/renier/fico-project/data-fetcher/Fang_preprint
conda activate fang-preprint
mkdir -p logs
python convert_fang_preprint.py mouse_cortex_100um > logs/mouse_cortex_100um.log 2>&1
python convert_fang_preprint.py mouse_hypothalamus_200um > logs/mouse_hypothalamus_200um.log 2>&1
```


```bash
cd ~/code/renier/fico-project/data-fetcher/Fang_preprint
conda activate fang-preprint
mkdir -p logs
python convert_fang_preprint_images.py mouse_hypothalamus_200um > logs/mouse_hypothalamus_200um_images.log 2>&1
```
