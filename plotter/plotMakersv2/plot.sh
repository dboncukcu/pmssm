#!/bin/bash

set -e

output_dir="output"
mkdir -p "$output_dir"

python3 mssmParams.py NoCut > "$output_dir/mssmParams_NoCut.txt" 2>&1 &
python3 mssmParams.py DM > "$output_dir/mssmParams_DM.txt" 2>&1 &
python3 mssmParams.py DeltaEW > "$output_dir/mssmParams_DeltaEW.txt" 2>&1 &
python3 mssmParams.py DM_DeltaEW > "$output_dir/mssmParams_DM_DeltaEW.txt" 2>&1 &

# python3 survivalPlots2D.py NoCut > "$output_dir/survivalPlots2D_NoCut.txt" 2>&1 &
# python3 survivalPlots2D.py DM > "$output_dir/survivalPlots2D_DM.txt" 2>&1 &
# python3 survivalPlots2D.py DeltaEW > "$output_dir/survivalPlots2D_DeltaEW.txt" 2>&1 &
# python3 survivalPlots2D.py DM_DeltaEW > "$output_dir/survivalPlots2D_DM_DeltaEW.txt" 2>&1 &

wait

echo "Finished."