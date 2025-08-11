# Minimum CMake version required
cmake_minimum_required(VERSION 3.18)

# Project definition
project(py_bundle LANGUAGES C)

# --- Configuration ---
set(APP_NAME "my_app")
set(PY_SOURCE_FILE "${PROJECT_SOURCE_DIR}/src/main.py")
set(DIST_DIR "${CMAKE_CURRENT_BINARY_DIR}/dist")

# --- Tool Flags ---
set(CYTHON_FLAGS
        -3
        --embed
        )
set(PYINSTALLER_FLAGS
        --noconfirm
        --onefile
        --clean
        --distpath ${DIST_DIR}
        --hidden-import=requests
        --hidden-import=rich
        --hidden-import=ip
        )

# --- Compiler Optimization ---
set(PERF_FLAGS "-O3 -march=native -flto -fomit-frame-pointer")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${PERF_FLAGS}")
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${PERF_FLAGS}")

# --- Tools Discovery ---
find_package(Python3 3.8 REQUIRED COMPONENTS Interpreter Development)
find_program(CYTHON_EXECUTABLE NAMES cython3 cython REQUIRED)
find_program(PYI_EXECUTABLE NAMES pyinstaller REQUIRED)

# --- Build Path 1: Dynamic Executable ---
set(DYNAMIC_APP_NAME "${APP_NAME}_dynamic")
set(GENERATED_C_DYNAMIC "${CMAKE_CURRENT_BINARY_DIR}/main_dynamic.c")

add_custom_command(
        OUTPUT ${GENERATED_C_DYNAMIC}
        COMMAND ${CYTHON_EXECUTABLE} ${CYTHON_FLAGS} ${PY_SOURCE_FILE} -o ${GENERATED_C_DYNAMIC}
        DEPENDS ${PY_SOURCE_FILE}
        COMMENT "Generate C for dynamic exe"
)

add_executable(${DYNAMIC_APP_NAME} ${GENERATED_C_DYNAMIC})
target_link_libraries(${DYNAMIC_APP_NAME} PRIVATE Python3::Python)
set_target_properties(${DYNAMIC_APP_NAME} PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${DIST_DIR}")

# --- Build Path 1b: Shared Library (.so) ---
set(SHARED_LIB_NAME "${APP_NAME}_lib")
set(GENERATED_C_SHARED "${CMAKE_CURRENT_BINARY_DIR}/main_shared.c")

add_custom_command(
        OUTPUT ${GENERATED_C_SHARED}
        COMMAND ${CYTHON_EXECUTABLE} ${CYTHON_FLAGS} ${PY_SOURCE_FILE} -o ${GENERATED_C_SHARED}
        DEPENDS ${PY_SOURCE_FILE}
        COMMENT "Generate C for shared lib"
)

add_library(${SHARED_LIB_NAME} SHARED ${GENERATED_C_SHARED})
target_link_libraries(${SHARED_LIB_NAME} PRIVATE Python3::Python)
set_target_properties(${SHARED_LIB_NAME}
        PROPERTIES
        OUTPUT_NAME "${SHARED_LIB_NAME}"
        PREFIX ""
        SUFFIX ".so"
        LIBRARY_OUTPUT_DIRECTORY "${DIST_DIR}"
        )

# --- Build Path 2: Static Executable ---
set(STATIC_APP_NAME "${APP_NAME}_static")

add_custom_target(${STATIC_APP_NAME} ALL
        COMMAND ${PYI_EXECUTABLE} ${PYINSTALLER_FLAGS} --name ${STATIC_APP_NAME} ${PY_SOURCE_FILE}
        WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}"
        COMMENT "Create standalone bundle"
        )

# --- Summary Messages ---
message(STATUS "Build with 'cmake --build .'")
message(STATUS "Outputs in: ${DIST_DIR}")
message(STATUS "  - Dynamic exe: ${DIST_DIR}/${DYNAMIC_APP_NAME}")
message(STATUS "  - Shared lib: ${DIST_DIR}/${SHARED_LIB_NAME}.so")
message(STATUS "  - Static exe: ${DIST_DIR}/${STATIC_APP_NAME}")
