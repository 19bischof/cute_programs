"Benchmark module to test different ways of fetching html"
#Notice: with too many urls or just bad urls, the program may print errors, but the program will still run normally :)
import os
import cProfile  # Profiles the function call and times
import pstats  # creates Statistics based on the Profile
import asyncio
import re
import grequests  # grequests has to be before requests is imported because it monkeypatches it and imports it
import httpx
import aiohttp
import requests
import time
import random
from url_valid import url_format


with open("urls/urls.txt", "r") as f:
    urls = f.read().split("\n")
for u in urls[:]:
    if not re.match(url_format,u):
        urls.remove(u)
        print("removed [{}]".format(u))

urls = random.sample(urls, 200)
print("number of urls:",len(urls))
timeout = 3
print_exceptions = True
Red = '\u001b[31m'
Reset = '\u001b[0m'


def from_status_code(losc):
    "Decides if connection was succesful or not"
    return [code < 400 for code in losc if not isinstance(code,Exception)]

def print_errors(resps):
    if print_exceptions:
        for r in resps:
            if isinstance(r,Exception):
                print(Red,(type(r),r),Reset)

def time_me(func):
    "Benchmark Decorator"
    import inspect

    def wrapper(*args, **kwargs):
        start_t = time.perf_counter()
        print("{} is starting".format(func.__name__))
        with cProfile.Profile() as pr:  # start Profiling 
            resps = func(*args, **kwargs)
        hit = from_status_code(resps).count(True)
        note = "{}: {:.3f} seconds and {:.2f}% fidelity".format(
            func.__name__, time.perf_counter()-start_t, hit/len(urls)*100)
        st = pstats.Stats(pr)  # create statistics from Profile
        st.sort_stats(pstats.SortKey.TIME)
        st.dump_stats("profiler/"+func.__name__+".profiler")
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
    """uses standard requests module"""
    resps = []
    with requests.Session() as session:
        for url in urls:
            try:    #try is important
                resps.append(session.get(url, timeout=timeout))
            except:
                pass
    print_errors(resps)
    return [r.status_code for r in resps]

@time_me
def fusion():
    "uses requests module with concurrent.future.ThreadPool"
    import concurrent.futures
    resps = []
    with requests.Session() as session:
        #compiling list of futures:
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            list_of_futures = [executor.submit(
                session.get,url,timeout=timeout) for url in urls]
    # yields future when it completes:
    for future in concurrent.futures.as_completed(list_of_futures):
        try: #try is important
            resps.append(future.result())  # returns response objects
        except Exception as e:
            resps.append(e)
            pass
    print_errors(resps)
    return [r.status_code for r in resps if isinstance(r,requests.Response)]

@time_me
def gregarious():
    "using the grequests module"
    with requests.Session() as session:
        reqs = (grequests.get(url, timeout=timeout,session=session) for url in urls)
        resps = grequests.map(reqs)
    print_errors(resps)
    return [resp.status_code for resp in resps if isinstance(resp,requests.Response)]


#may print unicode error: socket module cant stand when url name is too long or so
@time_me
@coro
async def aeiou_http():
    "using the aiohttp module"
    session_timeout = aiohttp.ClientTimeout(sock_connect=timeout,sock_read=timeout,connect=timeout) #making sure there is no session timeout
    conn = aiohttp.TCPConnector(limit=len(urls))
    async with aiohttp.ClientSession(connector=conn) as session:
        #verify_ssl is important for: "https://cdc.gov"
        tasks = (session.get(url,verify_ssl=False,timeout=session_timeout) for url in urls) 
        try:
            resps = await asyncio.gather(*tasks,return_exceptions=True)
        except:
            pass
    
    print_errors(resps)
    return [r.status for r in resps if isinstance(r,aiohttp.ClientResponse)]
    

@time_me
@coro
async def xtra_hot():
    "using the httpx module"
    limits = httpx.Limits() #making sure that there are no pool timeouts, because of the size of urls (occured with 1650)
    async with httpx.AsyncClient(limits = limits,verify=False) as client:
        tasks = (asyncio.ensure_future(client.get(url,timeout=timeout)) for url in urls)
        resps = await asyncio.gather(*tasks,return_exceptions=True)  
    print_errors(resps)
    return [resp.status_code for resp in resps if isinstance(resp,httpx.Response)]

def print_result():
    import re
    dick = {}
    for note in time_me.notes:
        time_taken = re.findall("\d+\.\d+",note)[0]
        name = re.findall("\w+:",note)[0]
        fidelity = re.findall("[\d.]+%",note)[0]
        dick.update({float(time_taken):(name,fidelity)})
    lick = sorted(dick,reverse=True) #returns list of keys; sorts on keys = the time
    print(f"benchmark for {len(urls)} urls:")
    for key in lick:
        print(f"{dick[key][0][:15]}".ljust(15) + f"{key:7.2f}s | {dick[key][1]}")
    
		
if __name__ == "__main__":
    traditional()
    fusion()
    gregarious()
    xtra_hot()
    aeiou_http()
    print_result()

"""
benchmark for 200 urls:
traditional:    179.80s | 80.00%
gregarious:      22.73s | 81.00%
xtra_hot:        12.11s | 91.50%
fusion:           9.71s | 79.50%
aeiou_http:       7.33s | 82.00%
"""
