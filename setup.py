from distutils.core import setup

import numpy
from Cython.Build import cythonize

# compiling the cython files, no install
# to compile: python3 setup_dev.py build_ext --inplace
# TODO: add packages
setup(
    name="wavelet",
    version='0.0.2',
    author='AP-Atul',
    author_email='atulpatare99@gmail.com',
    ext_modules=cythonize(["./torpido/wavelet/extension/wavelet_transform.pyx",
                           "./torpido/wavelet/extension/base_transform.pyx"]),
    include_dirs=[numpy.get_include()],
    zip_safe=False,
    url='https://github.com/AP-Atul/Torpido',
    long_description=open('README.md').read(),
)
