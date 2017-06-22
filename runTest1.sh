#!/bin/bash

mkdir -p /data
cd /data

# Fetch MTBLS1 study
#apt-get -y install wget
wget -O /data/MTBLS1.zip 'https://www.ebi.ac.uk/metabolights/MTBLS1/files/MTBLS1'

# Fetch test data
wget 'https://raw.githubusercontent.com/phnmnl/container-nmrglue/develop/test_data_spectra.csv.gz'
wget 'https://raw.githubusercontent.com/phnmnl/container-nmrglue/develop/test_data_ppm.csv.gz'
wget 'https://raw.githubusercontent.com/phnmnl/container-nmrglue/develop/test_data_fid.csv.gz'

# Run test
wget -O /data/runTest2.python 'https://raw.githubusercontent.com/phnmnl/container-nmrglue/develop/runTest2.python'
chmod 755 /data/runTest2.python
/data/runTest2.python

# Compare results
if [[ "$(cat data_spectra.csv | head -n 1)" != "$(zcat test_data_spectra.csv.gz | head -n 1)" ]]; then
	echo "Test failed! Results do not match test data."
	exit 1
else
	echo "Test succeeded successfully."
fi


