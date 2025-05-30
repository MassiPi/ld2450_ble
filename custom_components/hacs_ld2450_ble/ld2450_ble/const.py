CHARACTERISTIC_NOTIFY = "0000fff1-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_WRITE = "0000fff2-0000-1000-8000-00805f9b34fb"

CMD_ENABLE_CONFIG = b"\xfd\xfc\xfb\xfa\x04\x00\xff\x00\x01\x00\x04\x03\x02\x01"
ACK_ENABLE_CONFIG_REGEX = b"\xFD\xFC\xFB\xFA\x08\x00\xFF\x01" + b"(?P<ACK_ENABLE_CONFIG_RESULT>..)" + b"\x01\x00\x40\x00\x04\x03\x02\x01"

CMD_DISABLE_CONFIG = b"\xfd\xfc\xfb\xfa\x02\x00\xfe\x00\x04\x03\x02\x01"
ACK_DISABLE_CONFIG_REGEX = b"\xFD\xFC\xFB\xFA\x04\x00\xFE\x01" + b"(?P<ACK_DISABLE_CONFIG_RESULT>..)" + b"\x04\x03\x02\x01"

CMD_ENABLE_SINGLE_TARGET = b"\xfd\xfc\xfb\xfa\x02\x00\x80\x00\x04\x03\x02\x01"
ACK_SINGLE_TARGET_REGEX = b"\xFD\xFC\xFB\xFA\x04\x00\x80\x01" + b"(?P<ACK_SINGLE_TARGET_RESULT>..)" + b"\x04\x03\x02\x01"

CMD_ENABLE_MULTI_TARGET = b"\xfd\xfc\xfb\xfa\x02\x00\x90\x00\x04\x03\x02\x01"
ACK_MULTI_TARGET_REGEX = b"\xFD\xFC\xFB\xFA\x04\x00\x90\x01" + b"(?P<ACK_MULTI_TARGET_RESULT>..)" + b"\x04\x03\x02\x01"

CMD_REBOOT = b"\xFD\xFC\xFB\xFA\x02\x00\xA3\x00\x04\x03\x02\x01"
ACK_REBOOT_REGEX = b"\xFD\xFC\xFB\xFA\x04\x00\xA3\x01" + b"(?P<ACK_REBOOT_RESULT>..)" + b"\x04\x03\x02\x01"

CMD_QUERY_TARGET_MODE = b"\xFD\xFC\xFB\xFA\x02\x00\x91\x00\x04\x03\x02\x01"
ACK_TARGET_MODE_REGEX = b"\xFD\xFC\xFB\xFA\x06\x00\x91\x01" + b"(?P<ACK_TARGET_MODE_RESULT>..)" + b"(?P<ACK_TARGET_MODE_VAL>..)" + b"\x04\x03\x02\x01"

CMD_GET_FW_VER = b"\xFD\xFC\xFB\xFA\x02\x00\xA0\x00\x04\x03\x02\x01"
ACK_FW_VER_REGEX = b"\xFD\xFC\xFB\xFA\x0C\x00\xA0\x01" + b"(?P<ACK_FW_VER_RESULT>..)" + b"(?P<ACK_FW_TYPE>..)" + b"(?P<ACK_FW_VER_VAL>......)" + b"\x04\x03\x02\x01"

CMD_GET_MAC = b"\xFD\xFC\xFB\xFA\x04\x00\xA5\x00\x01\x00\x04\x03\x02\x01"
ACK_MAC_REGEX = b"\xFD\xFC\xFB\xFA\x0A\x00\xA5\x01" + b"(?P<ACK_MAC_RESULT>..)" + b"(?P<ACK_MAC_VAL>......)" + b"\x04\x03\x02\x01"

CMD_AREA = b"\xFD\xFC\xFB\xFA\x02\x00\xC1\x00\x04\x03\x02\x01"
ACK_AREA_REGEX = b"\xFD\xFC\xFB\xFA\x1E\x00\xC1\x01" + b"(?P<ACK_AREA_RESULT>..)" + b"(?P<ACK_AREA_MODE>..)" + b"(?P<ACK_AREA_ONE>........)" + b"(?P<ACK_AREA_TWO>........)" + b"(?P<ACK_AREA_THREE>........)" + b"\x04\x03\x02\x01"

CMD_SET_AREA_PRE = b"\xFD\xFC\xFB\xFA\x1C\x00\xC2\x00" #+2byte mode +3*8byte area config
CMD_SET_AREA_POST = b"\x04\x03\x02\x01"
ACK_SET_AREA_REGEX = b"\xFD\xFC\xFB\xFA\x04\x00\xC2\x01" + b"(?P<ACK_SET_AREA_RESULT>..)" + b"\x04\x03\x02\x01"

frame_start = b"\xaa\xff\x03\x00"
frame_target_one_x = b"(?P<target_one_x>..)"
frame_target_one_y = b"(?P<target_one_y>..)"
frame_target_one_s = b"(?P<target_one_s>..)"
frame_target_one_r = b"(?P<target_one_r>..)"

frame_target_two_x = b"(?P<target_two_x>..)"
frame_target_two_y = b"(?P<target_two_y>..)"
frame_target_two_s = b"(?P<target_two_s>..)"
frame_target_two_r = b"(?P<target_two_r>..)"

frame_target_three_x = b"(?P<target_three_x>..)"
frame_target_three_y = b"(?P<target_three_y>..)"
frame_target_three_s = b"(?P<target_three_s>..)"
frame_target_three_r = b"(?P<target_three_r>..)"

frame_end = b"\x55\xcc"

frame_regex = (
    frame_start
    + frame_target_one_x 
    + frame_target_one_y
    + frame_target_one_s
    + frame_target_one_r
    + frame_target_two_x 
    + frame_target_two_y
    + frame_target_two_s
    + frame_target_two_r
    + frame_target_three_x 
    + frame_target_three_y
    + frame_target_three_s
    + frame_target_three_r
    + frame_end
)