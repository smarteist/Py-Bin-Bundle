## Prerequisites

- **CMake** ≥ 3.18  
- **Python 3.8+** (interpreter + dev headers)  
- **Cython** (`cython3`)  
- **(Optional)** PyInstaller (`pyinstaller`) if you want a standalone bundle  

---

## Quick Build

1. **Create a build dir if not exists & enter it**  
   ```bash
   cd build
   ```

2. **Configure**

   ```bash
   cmake ..
   ```
    
3. **Compile**
   
   ```bash
   cmake --build .
   ```
    
4. **(With PyInstaller)**  
    The bundled executable will appear in  
    `build/dist/app`
    

---

## What’s Where

```
.
├── CMakeLists.txt      # Build rules & flags
├── src/
│   └── main.py         # Your Python entry point
└── build/              # All CMake artifacts go here
    ├── app             # Native executable (With cython)
    └── dist/           # PyInstaller bundle (if enabled)
```

- **CMakeLists.txt**: Imports Python3, runs Cython, sets optimization flags, and (optionally) invokes PyInstaller.
    
- **src/main.py**: Your app logic, converted to C via Cython.
    
- **build/**: Houses the generated C files, object files, final executables, and PyInstaller output.
