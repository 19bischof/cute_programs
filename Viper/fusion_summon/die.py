"Benchmark module to test different ways of fetching html"

import os
import cProfile  # Profiles the function call and times
import pstats  # creates Statistics based on the Profile
import asyncio
import grequests  # grequests has to be before requests is imported because it monkeypatches it and imports it
import httpx
import aiohttp
import requests
import time
import random

with open("urls/toppy.txt", "r") as f:
    urls = f.read().split("\n")
    urls = urls * 3


urls = random.sample(urls, 30)
timeout = 3


def time_me(func):
    "Benchmark Decorator"
    import inspect

    def wrapper(*args, **kwargs):
        start_t = time.perf_counter()
        print("{} is starting".format(func.__name__))
        with cProfile.Profile() as pr:  # start Profiling 
            resps = func(*args, **kwargs)
        st = pstats.Stats(pr)  # create statistics from Profile
        st.sort_stats(pstats.SortKey.TIME)
        st.dump_stats(".profiler/func.__name__+".profiler")
        hit = resps.count(True)
        note = "{}: {:.2f} seconds and {}% fidelity".format(
            func.__name__, time.perf_counter()-start_t, int(hit/len(urls)*100))
        print(note)
        time_me.notes.append(note)
        print("----------------timeout for 2 seconds----------------")
        time.sleep(2)
    return wrapper


time_me.notes = []


def coro(func):
    "Coroutine Decorator"

    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) 
        #some issue with windows event loop; occured only in aiohttp module when using https
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args,**kwargs))
    wrapper.__name__ = func.__name__
    return wrapper


@time_me
def traditional():
    """uses normal requests module"""
    resps = []
    with requests.Session() as session:
        for url in urls:
            try:
                resps.append(session.get(url, timeout=timeout))
            except:
                pass
    return [resp.ok for resp in resps]

#TODO timeout isnt handled by fusion and maybe others
#or in other words bad urls may lead to exception
@time_me
def fusion():
    "requests module with concurrent.future.ThreadPool"
    import concurrent.futures
    resps = []
    with requests.Session() as session:
        #compiling list of futures:
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(urls)) as executor:
            list_of_futures = [executor.submit(
                session.get(url, timeout=timeout), url) for url in urls]
    # yields future when it completes:
    for future in concurrent.futures.as_completed(list_of_futures):
        try:
            data = future.result()  # returns response objects
            resps.append(data.ok)
        except:
            resps.append(False)
    return resps


@time_me
def gregarious():
    "using the grequests module"
    with requests.Session() as session:
        reqs = (grequests.get(url, timeout=timeout,session=session) for url in urls)
        resps = grequests.map(reqs)
    return [bool(resp) for resp in resps]

@time_me
@coro
async def aeiou_http():
    "using the aiohttp module"

    async def fetch(url, session):
        async with session.get(url) as response:
            return await response.read()

    async with aiohttp.ClientSession() as session:
        try:
            tasks = (asyncio.ensure_future(fetch(url,session)) for url in urls)
            resps = await asyncio.gather(*tasks)
        except:
            pass
    return [bool(resp) for resp in resps]


@time_me
@coro
async def xtra_hot():
    "using the httpx module"
    async with httpx.AsyncClient() as client:
        try:
            tasks = (client.get(url) for url in urls)
            resps = await asyncio.gather(*tasks)
        except:
            pass

    return [bool(resp) for resp in resps]

def print_result():
	for note in time_me.notes:
		print(note)
		
if __name__ == "__main__":
    traditional()
    fusion()
    gregarious()
    xtra_hot()
    aeiou_http()
    print_result()
