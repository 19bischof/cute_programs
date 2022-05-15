from setuptools import setup,Extension

module = Extension("tits",sources=["tts.c"])

setup(name="dong",
version="1.0",
description="big dong",
ext_modules = [module])