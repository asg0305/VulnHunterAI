output_paths = {
    '/home/user/output/OnlineSearch/general-search': {
        'format': "{searchalias}-gen-{date}.json",
        'process_mode': "WebSearch"
    },
    '/home/user/output/OnlineSearch/secure-search': {
        'format': "{searchalias}-sec-{date}.json",
        'process_mode': "WebSearch"
    },
    '/home/user/output/Vulhunter/sec_spider': {
        'format': "sec_spider.jsonl",
        'process_mode': "WebAnalysis"
    },
    '/home/user/output/Vulhunter/gen_spider': {
        'format': "gen_spider.jsonl",
        'process_mode': "WebAnalysis"
    }
},
sec_domains = {
        "www.incibe.es",
        "vulmon.com",
        "nvd.nist.gov"
},
general_domains = {
        "github.com",
        "www.cve.org",
        "book.hacktricks.xyz",
        "exploit-db.com",
        "cvedetails.com"
},
sites = {
        "https://www.incibe.es/incibe-cert/alerta-temprana/vulnerabilidades/",
        "https://www.cve.org/",
        "https://www.cvedetails.com/",
        "https://book.hacktricks.xyz/es",
        "https://vulmon.com/searchpage"
}