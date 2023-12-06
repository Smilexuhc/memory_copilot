# TODO(Smile): Fix circular import risk
from .tool_utils import exec_tool, generate_prompts, register_meta
from .article_summary import *
from .base_tools import *
from .intention_detection import *
from .memory_tools import *
from .web_crawler import *
from .file_tools import *

TOOLS = {
    crawl_web.meta.name: crawl_web,
    summarize_article.meta.name: summarize_article,
    submit_result.meta.name: submit_result,
    exit_task.meta.name: exit_task,
    ask_human.meta.name: ask_human,
    get_current_datatime.meta.name: get_current_datatime,
    list_memory.meta.name: list_memory,
    read_file.meta.name: read_file,
    read_pdf.meta.name: read_pdf,
}
