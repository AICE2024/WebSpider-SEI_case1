BOT_NAME = "climate_agent"

SPIDER_MODULES = ["crawler"]
NEWSPIDER_MODULE = "crawler"
REDIRECT_ENABLED = True


ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'crawler.pipelines.SaveToJSONPipeline': 300,
}

LOG_LEVEL = 'INFO'
