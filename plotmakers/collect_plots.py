import config as pltconfig
import os
import shutil

# Kaynak dizin yolu
source_dir = pltconfig.plotsdir
# Hedef dizin yolu
target_dir = os.path.join(pltconfig.plotsdir, 'collected_plots')

# Hedef dizin yoksa oluştur
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

# Kopyalanan dosya sayısını tutacak sayaç
copied_count = 0

# Tüm dosyaları yürütme ve kopyalama
for root, dirs, files in os.walk(source_dir):
    # Hedef dizini dolaşmamak için dizinler listesinden çıkar
    dirs[:] = [d for d in dirs if os.path.join(root, d) != target_dir]
    
    for file in files:
        if file.endswith('.pdf'):
            shutil.copy(os.path.join(root, file), target_dir)
            copied_count += 1
            print("Copied: ", file)

# Toplam kopyalanan dosya sayısını yazdır
print("\n\nTotal files copied:", copied_count)
