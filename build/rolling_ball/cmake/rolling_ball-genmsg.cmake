# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(WARNING "Invoking generate_messages() without having added any message or service file before.
You should either add add_message_files() and/or add_service_files() calls or remove the invocation of generate_messages().")
message(STATUS "rolling_ball: 0 messages, 0 services")

set(MSG_I_FLAGS "")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(rolling_ball_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages

### Generating Services

### Generating Module File
_generate_module_cpp(rolling_ball
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rolling_ball
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(rolling_ball_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(rolling_ball_generate_messages rolling_ball_generate_messages_cpp)

# add dependencies to all check dependencies targets

# target for backward compatibility
add_custom_target(rolling_ball_gencpp)
add_dependencies(rolling_ball_gencpp rolling_ball_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rolling_ball_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages

### Generating Services

### Generating Module File
_generate_module_eus(rolling_ball
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rolling_ball
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(rolling_ball_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(rolling_ball_generate_messages rolling_ball_generate_messages_eus)

# add dependencies to all check dependencies targets

# target for backward compatibility
add_custom_target(rolling_ball_geneus)
add_dependencies(rolling_ball_geneus rolling_ball_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rolling_ball_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages

### Generating Services

### Generating Module File
_generate_module_lisp(rolling_ball
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rolling_ball
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(rolling_ball_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(rolling_ball_generate_messages rolling_ball_generate_messages_lisp)

# add dependencies to all check dependencies targets

# target for backward compatibility
add_custom_target(rolling_ball_genlisp)
add_dependencies(rolling_ball_genlisp rolling_ball_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rolling_ball_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages

### Generating Services

### Generating Module File
_generate_module_nodejs(rolling_ball
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/rolling_ball
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(rolling_ball_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(rolling_ball_generate_messages rolling_ball_generate_messages_nodejs)

# add dependencies to all check dependencies targets

# target for backward compatibility
add_custom_target(rolling_ball_gennodejs)
add_dependencies(rolling_ball_gennodejs rolling_ball_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rolling_ball_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages

### Generating Services

### Generating Module File
_generate_module_py(rolling_ball
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rolling_ball
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(rolling_ball_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(rolling_ball_generate_messages rolling_ball_generate_messages_py)

# add dependencies to all check dependencies targets

# target for backward compatibility
add_custom_target(rolling_ball_genpy)
add_dependencies(rolling_ball_genpy rolling_ball_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rolling_ball_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rolling_ball)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rolling_ball
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET rolling_ball_generate_messages_cpp)
  add_dependencies(rolling_ball_generate_messages_cpp rolling_ball_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rolling_ball)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rolling_ball
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET rolling_ball_generate_messages_eus)
  add_dependencies(rolling_ball_generate_messages_eus rolling_ball_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rolling_ball)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rolling_ball
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET rolling_ball_generate_messages_lisp)
  add_dependencies(rolling_ball_generate_messages_lisp rolling_ball_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/rolling_ball)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/rolling_ball
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET rolling_ball_generate_messages_nodejs)
  add_dependencies(rolling_ball_generate_messages_nodejs rolling_ball_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rolling_ball)
  install(CODE "execute_process(COMMAND \"/usr/bin/python\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rolling_ball\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rolling_ball
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET rolling_ball_generate_messages_py)
  add_dependencies(rolling_ball_generate_messages_py rolling_ball_generate_messages_py)
endif()
