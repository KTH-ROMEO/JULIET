from enum import Enum

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

class Command_data(Enum):
    HK_UC                                   = [0x01, 0x00, 0xAA, 0xAA]
    HK_FPGA                                 = [0x01, 0x00, 0x55, 0x55] 
    HK_UC_FPGA                              = [0x02, 0x00, 0x55, 0x55, 0xAA, 0xAA] 
    TS_EMPTY                                = [0x00]
    FM_SET_VOLTAGE_LEVEL_SWEEP_MODE         = [Function_ID.SET_SWT_VOL_LVL_ID.value, 
                                                0x04,   
                                                Argument_ID.PROBE_ID_ARG_ID.value,     0x00,  
                                                Argument_ID.STEP_ID_ARG_ID.value,      0x1A,   
                                                Argument_ID.VOL_LVL_ARG_ID.value,      0x22 , 0x2A, 
                                                Argument_ID.GS_TARGET_ARG_ID.value,    0x01]

    FM_GET_VOLTAGE_LEVEL_SWEEP_MODE_FRAM    = [Function_ID.GET_SWT_VOL_LVL_ID.value, 
                                                0x03,   
                                                Argument_ID.PROBE_ID_ARG_ID.value,  0x00,  
                                                Argument_ID.STEP_ID_ARG_ID.value,   0x1A, 
                                                Argument_ID.GS_TARGET_ARG_ID.value, 0x01]
    
    FM_ENABLE_CB_MODE                       = [Function_ID.EN_CB_MODE_ID.value, 0x00]

    FM_SET_CONSTANT_BIAS_VOLTAGE            = [Function_ID.SET_CB_VOL_LVL_ID.value,        
                                                0x02,   
                                                Argument_ID.PROBE_ID_ARG_ID.value,  0x00,  
                                                Argument_ID.VOL_LVL_ARG_ID.value,   0x00, 0x11]

    FM_GET_CURRENT_CONSTANT_BIAS_VALUE      = [Function_ID.GET_CB_VOL_LVL_ID.value,       
                                                0x01,   
                                                Argument_ID.PROBE_ID_ARG_ID.value,  0x00]

    FM_SET_VOLTAGE_LEVEL_SWEEP_MODE_FPGA    = [Function_ID.SET_SWT_VOL_LVL_ID.value, 
                                                0x04,   
                                                Argument_ID.PROBE_ID_ARG_ID.value,     0x00,  
                                                Argument_ID.STEP_ID_ARG_ID.value,      0x1A,   
                                                Argument_ID.VOL_LVL_ARG_ID.value,      0xEC , 0x22, 
                                                Argument_ID.GS_TARGET_ARG_ID.value,    0x00]

    FM_GET_VOLTAGE_LEVEL_SWEEP_MODE_FRAM_FPGA    = [Function_ID.GET_SWT_VOL_LVL_ID.value, 
                                                0x03,   
                                                Argument_ID.PROBE_ID_ARG_ID.value,  0x00,  
                                                Argument_ID.STEP_ID_ARG_ID.value,   0x1A, 
                                                Argument_ID.GS_TARGET_ARG_ID.value, 0x00]