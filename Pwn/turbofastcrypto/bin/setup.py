from distutils.core import setup, Extension
NAME='turbofastcrypto'
setup(name=NAME, version='1.0', description='test', ext_modules = [Extension(NAME, sources=[NAME+'.c'])])
