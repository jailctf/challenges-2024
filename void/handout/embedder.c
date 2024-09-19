/* vim: set ts=2 sw=2 et: */
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <sys/file.h>
#include <sys/mman.h>
#include <sys/signal.h>

#ifndef DEBUGLVL
#define DEBUGLVL 1
#endif

void overwrite_function(void* fnptr) {
  int pagesize = getpagesize();
  void* page = ((uint64_t)fnptr) & ~(pagesize - 1);
  mprotect(page, pagesize, PROT_READ | PROT_WRITE);
  ((char*)fnptr)[0] = 0xCC;
  mprotect(page, pagesize, PROT_READ | PROT_EXEC);
}

#define STRINGIFY(s) #s
#if DEBUGLVL >= 1
#define overwrite_function_debug(fn) do { \
  puts("Setting " STRINGIFY(fn) " to 0xCC"); \
  overwrite_function(fn); \
} while(0)
#else
#define overwrite_function_debug overwrite_function
#endif

__attribute__((naked)) PyObject* my_PyEval_EvalCode(PyObject* a, PyObject* b, PyObject* c) {
  const void* offseted = PyEval_EvalCode+4;
  void* result;
  __asm__ __volatile__("jmp *%0" : "=r" (result) : "0" (offseted));
}

void sigtrap_handler() {
  puts("You tried using a banned constructor!");
  exit(1);
}

#if DEBUGLVL >= 2
PyObject* cfn_settrace(PyObject* self, PyObject* args) {
  asm("int $3");
  return Py_None;
}

PyMethodDef meth_settrace = {"settrace", _PyCFunction_CAST(cfn_settrace), METH_VARARGS, ""};
#endif

// ASLR should be enough randomness,
// just use a random builtin
uint64_t seed = &PyByteArray_Type;

PyObject* cfn_nextrng(PyObject* self, PyObject* args) {
  if (!PyArg_UnpackTuple(args, "nextrng", 0, 0)) return NULL;

  seed *= 0x123456789abcdef;
  return Py_BuildValue("K", seed);
}

PyMethodDef meth_nextrng = {"nextrng", _PyCFunction_CAST(cfn_nextrng), METH_VARARGS, ""};

int main(int argc, char** argv) {
  setbuf(stdout, NULL);
  setbuf(stderr, NULL);

  if (argc < 2) {
    puts("Provide filename");
    exit(1);
  }

#ifndef DEBUGLVL >= 2
  printf("system = %p\n", system);
#endif

  signal(SIGTRAP, sigtrap_handler);

  PyConfig config;

  PyConfig_InitIsolatedConfig(&config);
  config.site_import = 0;

  Py_InitializeFromConfig(&config);

  PyObject* builtins_module = PyImport_ImportModule("builtins");
  PyObject* builtins_module_dict = PyObject_GetAttrString(builtins_module, "__dict__");
#define save_builtin(b) PyObject* builtin_##b = PyObject_GetAttrString(builtins_module, STRINGIFY(b))
#if DEBUGLVL >= 2
  save_builtin(print);
  save_builtin(hex);
  save_builtin(id);
#endif
#undef save_builtin
  PyDict_Clear(builtins_module_dict);
#define restore_builtin(b) PyDict_SetItemString(builtins_module_dict, STRINGIFY(b), builtin_##b)
  PyDict_SetItemString(builtins_module_dict, "bytearray", &PyByteArray_Type);
#if DEBUGLVL >= 2
  restore_builtin(print);
  restore_builtin(hex);
  restore_builtin(id);
  PyObject* name_settrace = PyUnicode_FromString(meth_settrace.ml_name);
  PyDict_SetItemString(builtins_module_dict, meth_settrace.ml_name, PyCFunction_New(&meth_settrace, name_settrace));
  Py_XDECREF(name_settrace);
#endif
  PyObject* name_nextrng = PyUnicode_FromString(meth_nextrng.ml_name);
  PyDict_SetItemString(builtins_module_dict, meth_nextrng.ml_name, PyCFunction_New(&meth_nextrng, name_nextrng));
  Py_XDECREF(name_nextrng);

  Py_XDECREF(builtins_module_dict);
  Py_XDECREF(builtins_module);

  PyObject* empty_dict = PyDict_New();

  int fd = open(argv[1], O_RDONLY);
  if (fd < 0) { perror("open"); exit(1); }
  struct stat st;
  fstat(fd, &st);
  const char* mmap_buf = mmap(NULL, st.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
  if (mmap_buf == NULL) { perror("mmap"); exit(1); }
  char* buf = malloc(st.st_size+1);
  memcpy(buf, mmap_buf, st.st_size);
  buf[st.st_size] = '\0';
  PyObject* cod = Py_CompileString(buf, "<code>", Py_file_input);

  PyObject* builtins_str = PyUnicode_FromString("builtins");
  // object.__subclasses__()
  PyObject* subclasses_method = PyObject_GetAttrString(&PyBaseObject_Type, "__subclasses__");
  PyObject* subclasses = PyObject_CallNoArgs(subclasses_method);
  Py_XDECREF(subclasses_method);
  PyObject* subclasses_iter = PyObject_GetIter(subclasses);
  Py_XDECREF(subclasses);
  PyObject* item;
  while ((item = PyIter_Next(subclasses_iter)) != NULL) {
    PyObject* name = PyType_GetName(item);
    PyObject* module = PyObject_GetAttrString(item, "__module__");
    if (PyObject_RichCompareBool(module, builtins_str, Py_EQ) != 1) {
#if DEBUGLVL >= 1
      printf("(%p) Deleting type %s (tp_alloc) from module %s\n", item, PyUnicode_AsUTF8(name), PyUnicode_AsUTF8(module));
#endif
      overwrite_function(((PyTypeObject*)item)->tp_init);
    }
    Py_XDECREF(name);
    Py_XDECREF(item);
  }
  Py_XDECREF(subclasses_iter);
  Py_XDECREF(builtins_str);

  // string
#if DEBUGLVL < 2
  overwrite_function_debug(PyUnicode_FromStringAndSize);
#if DEBUGLVL < 1
  overwrite_function_debug(PyUnicode_FromString);
#endif
  overwrite_function_debug(PyUnicode_FromEncodedObject);
  overwrite_function_debug(PyUnicode_FromObject);
#if DEBUGLVL < 1
  overwrite_function_debug(PyUnicode_FromFormatV);
  overwrite_function_debug(PyUnicode_FromFormat);
#endif
  overwrite_function_debug(PyUnicode_FromOrdinal);
  overwrite_function_debug(PyUnicode_Decode);
  overwrite_function_debug(PyUnicode_DecodeUTF7);
  overwrite_function_debug(PyUnicode_DecodeUTF7Stateful);
  overwrite_function_debug(PyUnicode_DecodeUTF8);
#if DEBUGLVL < 1
  overwrite_function_debug(PyUnicode_DecodeUTF8Stateful);
#endif
  overwrite_function_debug(PyUnicode_DecodeUTF32);
  overwrite_function_debug(PyUnicode_DecodeUTF32Stateful);
  overwrite_function_debug(PyUnicode_DecodeUTF16);
  overwrite_function_debug(PyUnicode_DecodeUTF16Stateful);
  overwrite_function_debug(PyUnicode_DecodeUnicodeEscape);
  overwrite_function_debug(PyUnicode_DecodeRawUnicodeEscape);
  overwrite_function_debug(PyUnicode_DecodeLatin1);
  overwrite_function_debug(PyUnicode_DecodeASCII);
  overwrite_function_debug(PyUnicode_DecodeCharmap);
  overwrite_function_debug(PyUnicode_DecodeLocale);
  overwrite_function_debug(PyUnicode_DecodeLocaleAndSize);
  overwrite_function_debug(PyUnicode_DecodeFSDefault);
  overwrite_function_debug(PyUnicode_DecodeFSDefaultAndSize);
#endif

  // bytes
  overwrite_function_debug(PyBytes_FromFormat);
  overwrite_function_debug(PyBytes_FromFormatV);
  overwrite_function_debug(PyBytes_FromObject);
  overwrite_function_debug(PyBytes_FromString);
#if DEBUGLVL < 1
  // required for print and errors
  overwrite_function_debug(PyBytes_FromStringAndSize);
#endif
  overwrite_function_debug(_PyBytes_FromHex);
  
  // bytearray
  overwrite_function_debug(PyByteArray_FromObject);
  overwrite_function_debug(PyByteArray_FromStringAndSize);

  // tuple
  // overwrite_function_debug(PyTuple_Type.tp);
  // overwrite_function_debug(PyTuple_New);
  // overwrite_function_debug(PyTuple_Pack);
  // overwrite_function_debug(PyTuple_Type.tp_alloc);
  
  // type
  overwrite_function_debug(PyType_GenericNew);
  overwrite_function_debug(PyType_FromMetaclass);
  overwrite_function_debug(PyType_FromModuleAndSpec);
  overwrite_function_debug(PyType_FromSpec);
  overwrite_function_debug(PyType_FromSpecWithBases);
  overwrite_function_debug(PyType_Type.tp_init);
  // overwrite_function_debug(PyType_Type.tp_alloc);

  // dict
  overwrite_function_debug(PyDict_New);

  // exec/eval
  overwrite_function_debug(PyEval_EvalCode);
  overwrite_function_debug(PyEval_EvalCodeEx);

  puts("Running");

  my_PyEval_EvalCode(cod, empty_dict, empty_dict);
  if (Py_FinalizeEx() < 0) {
    exit(120);
  }
  return 0;
}
