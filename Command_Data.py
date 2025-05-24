from enum import Enum

import Global_Variables

class Function_ID(Enum):
    EN_CB_MODE_ID                           = 0xCA
    DIS_CB_MODE_ID                          = 0xC0

    SET_CB_VOL_LVL_ID                       = 0xCB
    GET_CB_VOL_LVL_ID                       = 0xCC

    SWT_ACTIVATE_SWEEP_ID                   = 0xAA

    SET_SWT_VOL_LVL_ID                      = 0xAB
    SET_SWT_STEPS_ID                        = 0xAC
    SET_SWT_SAMPLES_PER_STEP_ID             = 0xAD
    SET_SWT_SAMPLE_SKIP_ID                  = 0xAE
    SET_SWT_SAMPLES_PER_POINT_ID            = 0xAF
    SET_SWT_NPOINTS_ID                      = 0xB0

    GET_SWT_SWEEP_CNT_ID                    = 0xA0
    GET_SWT_VOL_LVL_ID                      = 0xA1
    GET_SWT_STEPS_ID                        = 0xA2
    GET_SWT_SAMPLES_PER_STEP_ID             = 0xA3
    GET_SWT_SAMPLE_SKIP_ID                  = 0xA4
    GET_SWT_SAMPLES_PER_POINT_ID            = 0xA5
    GET_SWT_NPOINTS_ID                      = 0xA6

    COPY_SWT_FRAM_TO_FPGA                   = 0xE0

    REBOOT_DEVICE_ID                        = 0xF3
    JUMP_TO_IMAGE                           = 0xF4
    LOAD_TO_IMAGE                           = 0xF5 
    GET_SENSOR_DATA                           = 0xF6 

class Argument_ID(Enum):

    PROBE_ID_ARG_ID                         = 0x01
    STEP_ID_ARG_ID                          = 0x02
    VOL_LVL_ARG_ID                          = 0x03
    N_STEPS_ARG_ID                          = 0x04
    N_SKIP_ARG_ID                           = 0x05
    N_F_ARG_ID                              = 0x06
    N_POINTS_ARG_ID                         = 0x07
    GS_TARGET_ARG_ID                        = 0x08
    FRAM_TABLE_ID_ARG_ID                    = 0x09
    N_SAMPLES_PER_STEP_ARG_ID               = 0x0A
    IMAGE_INDEX                             = 0x0B

class Command_data(Enum):
    HK_UC                                   = [0x01, 0x00, 0xAA, 0xAA]
    HK_FPGA                                 = [0x01, 0x00, 0x55, 0x55] 
    HK_UC_FPGA                              = [0x02, 0x00, 0x55, 0x55, 0xAA, 0xAA] 
    TS_EMPTY                                = []
    

    FM_GET_VOLTAGE_LEVEL_SWEEP_MODE_FRAM    = [Function_ID.GET_SWT_VOL_LVL_ID.value, 
                                                0x03,   
                                                Argument_ID.PROBE_ID_ARG_ID.value,  0x00,  
                                                Argument_ID.STEP_ID_ARG_ID.value,   0x1A, 
                                                Argument_ID.GS_TARGET_ARG_ID.value, 0x01]
    
    
def get_FM_SET_CONSTANT_BIAS_VOLTAGE():
    return [
        Function_ID.SET_CB_VOL_LVL_ID.value,        
        0x02,   
        Argument_ID.PROBE_ID_ARG_ID.value,  Global_Variables.LANGMUIR_PROBE_ID & 0xFF,  
        Argument_ID.VOL_LVL_ARG_ID.value,   (Global_Variables.CB_MODE_VOLTAGE >> 8) & 0xFF, Global_Variables.CB_MODE_VOLTAGE & 0xFF
        ]

def get_FM_GET_CURRENT_CONSTANT_BIAS_VALUE():
    return [
        Function_ID.GET_CB_VOL_LVL_ID.value,       
        0x01,   
        Argument_ID.PROBE_ID_ARG_ID.value,  Global_Variables.LANGMUIR_PROBE_ID & 0xFF]

def get_FM_SET_VOLTAGE_LEVEL_SWEEP_TABLE():
    return [
        Function_ID.SET_SWT_VOL_LVL_ID.value, 
        0x04,   
        Argument_ID.PROBE_ID_ARG_ID.value,     Global_Variables.LANGMUIR_PROBE_ID & 0xFF,  
        Argument_ID.STEP_ID_ARG_ID.value,      Global_Variables.STEP_ID & 0xFF,   
        Argument_ID.VOL_LVL_ARG_ID.value,      (Global_Variables.SWEEP_TABLE_VOLTAGE >> 8) & 0xFF, Global_Variables.SWEEP_TABLE_VOLTAGE & 0xFF, 
        Argument_ID.GS_TARGET_ARG_ID.value,    Global_Variables.TARGET]

def get_FM_GET_VOLTAGE_LEVEL_SWEEP_TABLE():
    return [
        Function_ID.GET_SWT_VOL_LVL_ID.value, 
        0x03,   
        Argument_ID.PROBE_ID_ARG_ID.value,  Global_Variables.LANGMUIR_PROBE_ID & 0xFF,  
        Argument_ID.STEP_ID_ARG_ID.value,   Global_Variables.STEP_ID & 0xFF, 
        Argument_ID.GS_TARGET_ARG_ID.value, Global_Variables.TARGET]

def get_FM_SET_STEPS_SB_MODE():
    return [
        Function_ID.SET_SWT_STEPS_ID.value, 
        0x01,   
        Argument_ID.N_STEPS_ARG_ID.value,   Global_Variables.SB_MODE_NR_STEPS & 0xFF]

def get_FM_GET_STEPS_SB_MODE():
    return [
        Function_ID.GET_SWT_STEPS_ID.value, 
        0x00]

def get_FM_SET_SAMPLES_PER_STEP_SB_MODE():
    return [
        Function_ID.SET_SWT_SAMPLES_PER_STEP_ID.value, 
        0x01,   
        Argument_ID.N_SAMPLES_PER_STEP_ARG_ID.value,  (Global_Variables.SB_MODE_NR_SAMPLES_PER_STEP >> 8) & 0xFF, Global_Variables.SB_MODE_NR_SAMPLES_PER_STEP & 0xFF]

def get_FM_GET_SAMPLES_PER_STEP_SB_MODE():
    return [
        Function_ID.GET_SWT_SAMPLES_PER_STEP_ID.value, 
        0x00]

def get_FM_SET_SKIPPED_SAMPLES_SB_MODE():
    return [
        Function_ID.SET_SWT_SAMPLE_SKIP_ID.value, 
        0x01,   
        Argument_ID.N_SKIP_ARG_ID.value,  (Global_Variables.SB_MODE_NR_SKIPPED_SAMPLES >> 8) & 0xFF, Global_Variables.SB_MODE_NR_SKIPPED_SAMPLES & 0xFF]

def get_FM_GET_SKIPPED_SAMPLES_SB_MODE():
    return [
        Function_ID.GET_SWT_SAMPLE_SKIP_ID.value, 
        0x00]

def get_FM_SET_SAMPLES_PER_POINT():
    return [
        Function_ID.SET_SWT_SAMPLES_PER_POINT_ID.value, 
        0x01,   
        Argument_ID.N_F_ARG_ID.value,  (Global_Variables.SB_MODE_NR_SAMPLES_PER_POINT >> 8) & 0xFF, Global_Variables.SB_MODE_NR_SAMPLES_PER_POINT & 0xFF]

def get_FM_GET_SAMPLES_PER_POINT():
    return [
        Function_ID.GET_SWT_SAMPLES_PER_POINT_ID.value, 
        0x00]

def get_FM_SET_POINTS_PER_STEP():
    return [
        Function_ID.SET_SWT_NPOINTS_ID.value, 
        0x01,   
        Argument_ID.N_POINTS_ARG_ID.value,  (Global_Variables.SB_MODE_NR_POINTS_PER_STEP >> 8) & 0xFF, Global_Variables.SB_MODE_NR_POINTS_PER_STEP & 0xFF]

def get_FM_GET_POINTS_PER_STEP():
    return [
        Function_ID.GET_SWT_NPOINTS_ID.value, 
        0x00]

def get_FM_GET_CPY_SWT_FRAM_TO_FPGA():
    return [
        Function_ID.COPY_SWT_FRAM_TO_FPGA.value, 
        0x02,
        Argument_ID.PROBE_ID_ARG_ID.value, Global_Variables.LANGMUIR_PROBE_ID & 0xFF,
        Argument_ID.FRAM_TABLE_ID_ARG_ID.value, Global_Variables.FRAM_TABLE_ID & 0xFF
        ]

def get_FM_ENABLE_CB_MODE():
    return [
        Function_ID.EN_CB_MODE_ID.value, 
        0x00
        ]

def get_FM_DISABLE_CB_MODE():
    return [
        Function_ID.DIS_CB_MODE_ID.value, 
        0x00
        ]

def get_FM_GEN_SWEEP():
    return [
        Function_ID.SWT_ACTIVATE_SWEEP_ID.value, 
        0x00
        ]

def get_REBOOT_DEVICE():
    return [
        Function_ID.REBOOT_DEVICE_ID.value, 
        0x00
        ]

def get_JUMP_TO_IMAGE():
    return [
        Function_ID.JUMP_TO_IMAGE.value, 
        0x01,
        Argument_ID.IMAGE_INDEX.value, Global_Variables.IMAGE_INDEX & 0xFF,
    ]

def get_LOAD_NEW_IMAGE():
    return [
        Function_ID.LOAD_TO_IMAGE.value, 
        0x00
    ]

def get_SENSOR_DATA():
    return [
        Function_ID.GET_SENSOR_DATA.value, 
        0x00
    ]