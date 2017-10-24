# TPUPMC

```
sudo apt-get install texlive-latex-base texlive-latex-recommended texlive-fonts-recommended texlive-latex-extra python-pyqt5 python-matplotlib python-pint python-tk ipython python-h5py python-sphinx git build-essential python-dev

wget https://www.open-mpi.org/software/ompi/v3.0/downloads/openmpi-3.0.0.tar.gz

tar -xvf openmpi-3.0.0.tar.gz 
cd openmpi-3.0.0/
./configure --enable-mpi-thread-multiple --enable-mpirun-prefix-by-default
make -j4
sudo make -j4 install
echo /usr/local/lib | sudo tee -a /etc/ld.so.conf
sudo ldconfig

wget https://support.hdfgroup.org/ftp/HDF5/current18/src/hdf5-1.8.19.tar.gz
tar -zxvf hdf5-1.8.19.tar.gz
cd hdf5-1.8.19/
./configure --enable-parallel --with-pic --enable-linux-lfs --enable-shared --enable-production=yes --disable-sharedlib-rpath --enable-static CC=mpicc FC=mpif90 --prefix=/usr/local
sudo make install
sudo ldconfig
```


