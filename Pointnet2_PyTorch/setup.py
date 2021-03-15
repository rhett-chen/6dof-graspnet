import os.path as osp
from setuptools import find_packages, setup

requirements = ["hydra-core==0.11.3", "pytorch-lightning==0.7.1"]
# include_dirs = [osp.realpath('../include'), '/usr/local/cuda-10.2/targets/x86_64-linux/include/']

exec(open(osp.join("pointnet2", "_version.py")).read())

setup(
    name="pointnet2",
    version=__version__,
    author="Erik Wijmans",
    packages=find_packages(),
    # include_dirs=include_dirs,
    install_requires=requirements,
)
