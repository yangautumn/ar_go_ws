cmake_minimum_required(VERSION 2.8)
add_definitions(-std=c++11)
project(ocam_publisher)

find_package(catkin REQUIRED COMPONENTS cv_bridge image_transport message_generation sensor_msgs)

# add the resized image message
# add_message_files(DIRECTORY msg
#    FILES 
# )

generate_messages(DEPENDENCIES sensor_msgs)

catkin_package(CATKIN_DEPENDS cv_bridge image_transport message_runtime sensor_msgs)

find_package(OpenCV)

include_directories(include ${catkin_INCLUDE_DIRS} ${OpenCV_INCLUDE_DIRS})

# add the image publisher executable
add_executable(ocam_publisher src/ocam_publisher.cpp)
add_dependencies(ocam_publisher ${catkin_EXPORTED_TARGETS} ${${PROJECT_NAME}_EXPORTED_TARGETS})
target_link_libraries(ocam_publisher ${catkin_LIBRARIES} ${OpenCV_LIBRARIES} -lpthread -ludev -lv4l2)

# Mark executables and/or libraries for installation
install(TARGETS ocam_publisher
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
