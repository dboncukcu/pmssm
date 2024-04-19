python3 plotmakers/t1.py > logs/t1.txt &
python3 plotmakers/b1.py > logs/b1.txt &
python3 plotmakers/g.py > logs/g.txt &
python3 plotmakers/lcsp.py > logs/lcsp.txt &
python3 plotmakers/abschi10.py > logs/abschi10.txt &
python3 plotmakers/abschipm.py > logs/abschipm.txt &
python3 plotmakers/abschi20.py > logs/abschi20.txt &
python3 plotmakers/abschi1pmchi10.py > logs/abschi1pmchi10.txt &
python3 plotmakers/abschi20chi10.py > logs/abschi20chi10.txt &
python3 plotmakers/delta_masses.py > logs/delta_masses.txt 
#make sure to wait at thi point that everything finishes, and then run
python3 plotmakers/collect_plots.py
exit