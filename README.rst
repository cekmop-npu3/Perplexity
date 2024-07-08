Perplexity
==========

Async wrapper for `Perplexity android app <https://play.google.com/store/apps/details?id=ai.perplexity.app.android&hl=ru&pli=1>`_ api.

Quick Example
-------------

.. code:: py

    from Perplexity import Perplexity
    from asyncio import run
    
    
    async def main():
        async with Perplexity(token='token') as chat:
            async for message in chat('Напиши какую-нибудь историю'):
                print(message)
            async for message in chat('Какой сейчас курс биткоина?'):
                print(message)
    
    
    if __name__ == '__main__':
        run(main())
