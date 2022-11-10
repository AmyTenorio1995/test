import scrapy
from scrapy_splash import SplashRequest
import requests
import random
import names
#from scrapy.crawler import CrawlerProcess
#from twisted.internet import reactor
#from scrapy.crawler import CrawlerRunner
#from scrapy.utils.log import configure_logging
#from scrapy.utils.project import get_project_settings

##GET PROXY FROM PROXYV6
proxyv6_API_key = 'a77f0f08-a83d-4d4e-84f3-12c428971320'
def get_new_proxyv6():
    r = requests.get(f'https://api.proxyv6.net/key/get-new-ip?api_key_rotating={proxyv6_API_key}')
    new_proxyv6 = r.json()
    status_proxyv6 = new_proxyv6['message']
    if status_proxyv6 =='KEY_EXPIRED':
        print('PROXYV6 API KEY EXPIRED. CHECK AND RENEW IT !!!')
        exit()
    elif status_proxyv6 =='GET_IP_TOO_FAST':
        proxy_data = get_current_proxyv6()
        #proxy_ip_v6 = str(proxy_data['data']['host']) + ':' + str(proxy_data['data']['port'])
        #return proxy_ip_v6
        proxy_ip = str(proxy_data['data']['host'])
        proxy_port = str(proxy_data['data']['port'])
        return proxy_ip, proxy_port
    elif status_proxyv6 =='SUCCESS':
        proxy_data = new_proxyv6
        #proxy_ip_v6 = str(proxy_data['data']['host']) + ':' + str(proxy_data['data']['port'])
        #return proxy_ip_v6
        proxy_ip = str(proxy_data['data']['host'])
        proxy_port = str(proxy_data['data']['port'])
        return proxy_ip, proxy_port

def get_current_proxyv6():
    r = requests.get(f'https://api.proxyv6.net/key/get-current-ip?api_key_rotating={proxyv6_API_key}')
    current_proxyv6 = r.json()
    return current_proxyv6


##END GET PROXY FROM PROXYV6
def get_user_agent():    
    #with open(ua_file, "r", encoding='utf-8') as f:
    with open("useragent.txt", "r") as f:
        user_agent_list = f.read().splitlines()
        user_agent = random.choice(user_agent_list)
    return str(user_agent)

# EMAILGENERATOR
def email_gen():
    return str(names.get_first_name()+names.get_last_name())

class Spider1Spider(scrapy.Spider):
    name = 'spider1'
    #allowed_domains = ['m.facebook.com']
    #start_urls = ['http://m.facebook.com/']

    script = '''
    function main(splash, args)
        splash.private_mode_enabled = false
        splash:on_request(function(request)
            request:set_proxy{
                host = "%s",
                port = "%s",
            }
            request:set_header('User-Agent', '%s')
            request:set_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.9')
            end)
        assert(splash:go(args.url))
        assert(splash:wait(2))
        input_email = assert(splash:select("#identify_search_text_input"))
        input_email:focus()
        input_email:send_text("%s@hotmail.com")
        assert(splash:wait(0.5))
        input_email:send_keys("<Enter>")
        assert(splash:wait(3))
        splash:set_viewport_full()
        return {
            html = splash:html(),
            png = splash:png(),
        }
    end
    '''
    
    def start_requests(self):
        user_agent = get_user_agent()
        print('=============================================')
        print(user_agent)
        proxy_ip, proxy_port = get_new_proxyv6()
        print('=============================================')
        print(proxy_ip+':'+proxy_port)
        #email = email_gen()
        email ='tvhrstd_shepardsen_1666071185@tfbnw.net'
        yield SplashRequest(url='https://m.facebook.com//login/identify/?ctx=recover&c=%2Flogin%2F&search_attempts=1&alternate_search=0&show_friend_search_filtered_list=0&birth_month_search=0&city_search=0',callback=self.parse, endpoint='execute',args={
            'lua_source': self.script % (proxy_ip, proxy_port, user_agent, email),
        })

    def parse(self, response):
        #print(response.request.headers)
        #print('=============================================')
        #print(response.headers)
        #print('=============================================')
        rtext = response.text
        
        if (rtext.__contains__("Send code via email")) or (rtext.__contains__("Try entering your password")):
            print("SEND CODE------------------------------")
        elif (rtext.__contains__("The phone number or email address that you've entered doesn't match an account.")):
            print("EMAIL NOT MATCH ------------------------")
        else:
            print("NONONO ------------------------")
            
        #print(rtext)

"""

if __name__ == '__main__':
    RETRIES = 0
    configure_logging()
    runner = CrawlerRunner()
    d = runner.crawl(Spider1Spider)
    def finished():
        global RETRIES
        # do your checks in this callback and run the spider again if needed
        # in this example, we check if the number of retries is less than the required value
        # if not we stop the reactor
        if RETRIES < 2:
            print("LOOPLOOP------------>"+str(RETRIES))
            RETRIES += 1
            d = runner.crawl(Spider1Spider)
            #d.addBoth(lambda _: finished())

        else:
            reactor.stop() # stop the reactor if the condition is not met

    #d.addBoth(lambda _: finished())
    reactor.run()

"""



#scrapy crawl spider1
