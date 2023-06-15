import os

ROOT_DIR= os.path.dirname(os.path.dirname(__file__)) + "/"
CONFIG_DIR= ROOT_DIR + "config/"
STRING_DIR= CONFIG_DIR + "strings/"

LOGGING_CONFIG= CONFIG_DIR + "logging_config.yaml"
PLAYER_CONFIG= CONFIG_DIR + "player_config.yaml"
MOB_CONFIG= CONFIG_DIR + "mob_config.yaml"
BUFF_CONFIG= CONFIG_DIR + "buff_config.yaml"

LOG_TEMPLATES= STRING_DIR + "log_templates.yaml"