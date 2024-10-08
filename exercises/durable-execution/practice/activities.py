import urllib.parse

import aiohttp
from shared import TranslationActivityInput, TranslationActivityOutput
from temporalio import activity


class TranslationActivities:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    @activity.defn
    async def translate_term(
        self, input: TranslationActivityInput
    ) -> TranslationActivityOutput:
        activity.logger.info(f"translate_term invoked with {input}")
        base = f"http://localhost:9999/translate"
        url = f"{base}?term={urllib.parse.quote(input.term)}&lang={input.language_code}"

        async with self.session.get(url) as response:
            if response.status != 200:
                error_message = await response.text()
                raise RuntimeError(error_message)
            response_json = await response.json()
            response = TranslationActivityOutput(**response_json)
            activity.logger.debug(f"Activity completed successfully with {input.term}, {input.language_code}, result: {response}")
            return response
