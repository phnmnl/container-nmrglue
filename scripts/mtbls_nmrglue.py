#!/usr/bin/env python2
# Script for reading RAW Bruker NMR spectra with nmrglue
# Created by Daniel Canueto

import nmrglue as ng
import numpy as np
import os
import zipfile
import csv
import shutil
import sys
import getopt



def main(argv):

   try:
        optlist, args = getopt.getopt(argv, '')

        path="/data/"+args[0]
        
        # Extraction of Bruker folder from zip file
        zip_ref = zipfile.ZipFile(path+".zip", 'r')
        zip_ref.extractall(path)
        zip_ref.close()
        for file in os.listdir(path):
            if file.endswith(".zip"):
                zip_ref = zipfile.ZipFile(path+'/'+file, 'r')
                zip_ref.extractall(path+"/nmr")
                zip_ref.close()

        # Remove __MACOSX folder
        shutil.rmtree(path+"/nmr"+"/__MACOSX")

        # Create ppm scale necessary for pre-processing
        bruker_folders=os.listdir(path+"/nmr")
        dummy, needed_data = ng.bruker.read_pdata(path+"/nmr/"+bruker_folders[0]+'/10/pdata/1')
        dic, data = ng.bruker.read(path+"/nmr/"+bruker_folders[0]+'/10')
        udic = ng.bruker.guess_udic(dic, data)
        uc = ng.fileiobase.unit_conversion(needed_data.size,'True',udic[0]['sw'],udic[0]['obs'],udic[0]['car'])
        ppm = uc.ppm_scale()
        np.savetxt(args[1], ppm, delimiter=",")

        # Preallocation of fid info and dataset of processed spectra
        initial_data=np.zeros((len(bruker_folders),needed_data.size))
        fid_info=np.zeros((len(bruker_folders),9))

        for x in range(0, len(bruker_folders)):
            dic, initial_data[x,:] = ng.bruker.read_pdata(path+"/nmr/"+bruker_folders[x]+'/10/pdata/1')
            fid_info[x,:]=[dic['acqus']['TD'],dic['acqus']['BYTORDA'],dic['acqus']['DIGMOD'],dic['acqus']['DECIM'],dic['acqus']['DSPFVS'],dic['acqus']['SW_h'],dic['acqus']['SW'],dic['acqus']['O1'],1/(2*dic['acqus']['SW_h'])]


        # Create csv dataset
        csv_out = open(args[2],'wb')
        mywriter = csv.writer(csv_out)
        for row in initial_data:
            mywriter.writerow(row)
        csv_out.close()

        # Create fid info dataset
        csv_out = open(args[3],'wb')
        mywriter = csv.writer(csv_out)
        for row in fid_info:
            mywriter.writerow(row)
        csv_out.close()
   except getopt.GetoptError:
          print 'Error'
          sys.exit(2)

        
if __name__ == "__main__":
   main(sys.argv[1:])




