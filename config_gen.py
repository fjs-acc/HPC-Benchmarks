
# Online Python - IDE, Editor, Compiler, Interpreter

import sys
import random
paket=sys.argv[1]
compiler=["gcc@12.1.0","aocc"]
#lapack=[""]
blas=["openblas","blis","clblast"]
fftwapi=["fftw","amdfftw"]
mpi=["mvapich2","openmpi","mpich"]
print(random.randrange(1, 10))
ret=""
if (paket=="compiler"):
    paket=compiler[random.randrange(0, len(compiler))]
elif (paket=="blas"):
    paket=blas[random.randrange(0, len(blas))]
elif (paket=="fftw"):
    paket=fftwapi[random.randrange(0, len(fftwapi))]
elif (paket=="mpi"):
    paket=mpi[random.randrange(0, len(mpi))]

print(paket)