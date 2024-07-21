Perplexity
==========

Async wrapper for `Perplexity android app <https://play.google.com/store/apps/details?id=ai.perplexity.app.android&hl=ru&pli=1>`_ api.

Installing
----------

**Python 3.11 or higher is required**

1. Clone repository into your project

.. code:: sh

    git clone https://github.com/cekmop-npu3/PerplexityAi.git

2. Create virtual environment and activate it

.. code:: sh

    python -m venv venv
    # activate in powershell
    venv\Scripts\activate.ps1
    # activate in cmd
    venv\Scripts\activate.bat

3. Install required libraries

.. code:: sh

    pip install -r requirements.txt


Usage
-------------

1. [OPTIONAL] Create .env file in your project and paste in your token

.. code:: py

    TOKEN=eyJhbGciOiJkaXIiLCJlb...

2. Create .py file and run it. It also can be used without token

.. code:: py

    from Perplexity import Perplexity
    from asyncio import run
    from dotenv import load_dotenv
    from os import getenv


    load_dotenv('.env')


    async def main():
        async with Perplexity(token=getenv('TOKEN')) as chat:
            async for message in chat('Напиши какую-нибудь историю'):
                print(message)
            async for message in chat('Какой сейчас курс биткоина?'):
                print(message)


    if __name__ == '__main__':
        run(main())
