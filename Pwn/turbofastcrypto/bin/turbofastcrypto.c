#define PY_SSIZE_T_CLEAN
#include <Python.h>

char IV[64] = "IRS{secrets_are_revealed!!}";

#pragma GCC optimize ("O0")
__attribute__ ((used)) static void print_flag() { system("cat flag"); }

static PyObject *encrypt(PyObject *self, PyObject *args) {
    const char *cmd;
    Py_ssize_t len;
    if (!PyArg_ParseTuple(args, "s#", &cmd, &len)) return NULL;
    for (int i = 0; i < len; i++) IV[i] ^= cmd[i];
    return PyBytes_FromStringAndSize(IV, len);
}

static PyMethodDef mtds[] = {
    {"encrypt", encrypt, METH_VARARGS, "Encrypt a string" },
    { NULL, NULL, 0, NULL }
};

static struct PyModuleDef moddef = {
    PyModuleDef_HEAD_INIT,
    "turbofastcrypto", 
    NULL,
    -1,
    mtds
};

PyMODINIT_FUNC PyInit_turbofastcrypto() { return PyModule_Create(&moddef);}
