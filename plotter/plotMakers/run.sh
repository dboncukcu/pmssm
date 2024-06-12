#!/bin/bash

if [ ! -d "logs" ]; then
  mkdir logs
fi

python3 impact1D.py > logs/impact1D.log 2>&1 &

python3 quantile1D.py > logs/quantile1D.log 2>&1 &

python3 quantile2D.py > logs/quantile2D.log 2>&1 &

python3 survival1D.py > logs/survival1D.log 2>&1 &

python3 survival2D.py > logs/survival2D.log 2>&1 &

wait

echo "All plotmakers are done!"