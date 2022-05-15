#include <Python.h>
#include <string.h>
#include <stdio.h>

static PyObject *tts(PyObject *self, PyObject *args)
{
    char *the_text;
    if (!PyArg_ParseTuple(args, "s", &the_text))
    {
        return NULL;
    }
    if (!strcmp(the_text, "text"))
    {
        printf("to\n");
        return PyBytes_FromString("don't pick up the phone, drunk and alone");
    }
    return PyLong_FromLong(0);
}

static PyMethodDef tts_methods[] = {
    {"tts", tts, METH_VARARGS,
     "give to speech when text!"},
    {NULL, NULL, 0, NULL} /* Sentinel */
};

static struct PyModuleDef ttsmodule = {
    PyModuleDef_HEAD_INIT,
    "tts_mom",    /* name of module */
    "tts module", /* module documentation, may be NULL */
    -1,           /* size of per-interpreter state of the module,
                     or -1 if the module keeps state in global variables. */
    tts_methods};

PyMODINIT_FUNC PyInit_tts_mom(void)
{
    return PyModule_Create(&ttsmodule);
}