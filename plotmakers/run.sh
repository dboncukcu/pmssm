python3 plotmakers/t1.py > log/t1.txt &
python3 plotmakers/b1.py > log/b1.txt &
python3 plotmakers/g.py > log/g.txt &
python3 plotmakers/lcsp.py > log/lcsp.txt &
python3 plotmakers/abschi10.py > log/abschi10.txt &
python3 plotmakers/abschipm.py > log/abschipm.txt &
python3 plotmakers/abschi20.py > log/abschi20.txt &
python3 plotmakers/abschi1pmchi10.py > log/abschi1pmchi10.txt &
python3 plotmakers/abschi20chi10.py > log/abschi20chi10.txt &
python3 plotmakers/delta_masses.py > log/delta_masses.txt 
#make sure to wait at thi point that everything finishes, and then run
python3 plotmakers/collect_plots.py