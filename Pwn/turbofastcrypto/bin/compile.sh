# This is not a reproducible build!
python3 setup.py build && \
mv build/lib*/turbofastcrypto* . && \
rm -r build
