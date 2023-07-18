import logging
import logging.handlers
import re

from server_utils.logger.formatters.consts import ColorCodes, MainConsts
from server_utils.logger.formatters.style_formatter import StyleFormatter


class ColorFormatter(logging.Formatter):
    arg_colors = [ColorCodes.PURPLE, ColorCodes.LIGHT_BLUE]
    level_fields = MainConsts.LEVEL_FIELDS
    level_to_color = {
        logging.DEBUG: ColorCodes.GREY,
        logging.INFO: ColorCodes.GREEN,
        logging.WARNING: ColorCodes.YELLOW,
        logging.ERROR: ColorCodes.RED,
        logging.CRITICAL: ColorCodes.BOLD_RED,
    }

    def __init__(self, fmt: str):
        super().__init__()
        self.level_to_formatter = {}

        def add_color_format(level: int):
            color = ColorFormatter.level_to_color[level]
            _format = fmt
            search = r"(%([^;]*))"
            _format = re.sub(search, f"{color}\\1{ColorCodes.RESET}", _format)
            formatter = logging.Formatter(_format)
            self.level_to_formatter[level] = formatter

        add_color_format(logging.DEBUG)
        add_color_format(logging.INFO)
        add_color_format(logging.WARNING)
        add_color_format(logging.ERROR)
        add_color_format(logging.CRITICAL)

    def format(self, record):
        orig_msg = record.msg
        orig_args = record.args
        formatter = self.level_to_formatter.get(record.levelno)
        self.rewrite_record(record)
        formatted = formatter.format(record)

        # restore log record to original state for other handlers
        record.msg = orig_msg
        record.args = orig_args
        return formatted

    @staticmethod
    def rewrite_record(record: logging.LogRecord):
        if not StyleFormatter.is_brace_format_style(record):
            return

        msg = record.msg.replace("{", "_{{").replace("}", "_}}")
        placeholder_count = 0

        while True:
            if "_{{" not in msg:
                break
            color_index = placeholder_count % len(ColorFormatter.arg_colors)
            color = ColorFormatter.arg_colors[color_index]
            msg = msg.replace("_{{", color + "{").replace("_}}", "}" + ColorCodes.RESET)
            placeholder_count += 1

        record.msg = msg.format(*record.args)
        record.args = []
