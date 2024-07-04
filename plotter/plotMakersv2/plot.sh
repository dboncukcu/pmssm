#!/bin/bash

# Hata oluştuğunda script'in durmasını sağla
set -e

# python3 mssmParams.py NoCut
# python3 mssmParams.py DM
# python3 mssmParams.py DeltaEW
# python3 mssmParams.py DM_DeltaEW

python3 survivalPlots2D.py NoCut
python3 survivalPlots2D.py DM
python3 survivalPlots2D.py DeltaEW
python3 survivalPlots2D.py DM_DeltaEW