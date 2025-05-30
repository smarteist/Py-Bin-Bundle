cmake_minimum_required(VERSION 3.18)
project(py_bundle LANGUAGES C)

# Constants for tool flags
set(CYTHON_FLAGS
    -3
    --embed
)
set(PYINSTALLER_FLAGS
    --noconfirm
    --onefile
    --optimize 2
)

# Options
set(PY_MAIN "${PROJECT_SOURCE_DIR}/src/main.py")
set(APP_NAME "app")
option(USE_PYINSTALLER "Bundle with PyInstaller" ON)

# Performance flags
# To target ARM, uncomment the following lines and adjust as needed:
# set(CMAKE_C_COMPILER "aarch64-linux-gnu-gcc")
# set(CMAKE_SYSTEM_PROCESSOR arm)
# set(PERF_FLAGS "-O3 -march=armv7-a -flto -fomit-frame-pointer")

set(PERF_FLAGS "-O3 -march=native -flto -fomit-frame-pointer")
set(CMAKE_C_FLAGS       "${CMAKE_C_FLAGS} ${PERF_FLAGS}")
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${PERF_FLAGS}")

# Find tools
find_package(Python3 3.8 REQUIRED COMPONENTS Interpreter Development)
find_program(CYTHON_EXECUTABLE NAMES cython3 cython)
if(NOT CYTHON_EXECUTABLE)
  message(FATAL_ERROR "Cython not found")
endif()

if(USE_PYINSTALLER)
  find_program(PYI_EXECUTABLE NAMES pyinstaller)
  if(NOT PYI_EXECUTABLE)
    message(FATAL_ERROR "PyInstaller not found")
  endif()
endif()

# Generate C from Python
get_filename_component(PY_ABS "${PY_MAIN}" ABSOLUTE)
set(GENERATED_C "${CMAKE_CURRENT_BINARY_DIR}/main.c")
add_custom_command(
  OUTPUT ${GENERATED_C}
  COMMAND ${CYTHON_EXECUTABLE} ${CYTHON_FLAGS} ${PY_ABS} -o ${GENERATED_C}
  DEPENDS ${PY_ABS}
)

# Build executable
add_executable(${APP_NAME} ${GENERATED_C})
target_include_directories(${APP_NAME} PRIVATE ${Python3_INCLUDE_DIRS})
target_link_libraries(${APP_NAME} PRIVATE Python3::Python)

# Bundle with PyInstaller
if(USE_PYINSTALLER)
  add_custom_command(
    OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/dist/${APP_NAME}"
    COMMAND ${PYI_EXECUTABLE} ${PYINSTALLER_FLAGS} --name ${APP_NAME} ${PY_ABS}
    DEPENDS ${APP_NAME}
    VERBATIM
  )
  add_custom_target(bundle ALL DEPENDS "${CMAKE_CURRENT_BINARY_DIR}/dist/${APP_NAME}")
endif()
