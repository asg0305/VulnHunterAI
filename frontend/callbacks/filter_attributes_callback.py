from dash.dependencies import Input, Output
import dash

def register_filter_callback(app):
    @app.callback(
        Output('attributeFilter', 'options'),
        [Input('attributeSearch', 'value')]
    )
    def filter_attributes(search_value):
        all_options = [
            {'label': 'URL', 'value': 'URL.url'},
            {'label': 'Source', 'value': 'URL.source'},
            {'label': 'CVE', 'value': 'CVE.CVE'},
            {'label': 'CVE URL', 'value': 'CVE.url'},
            {'label': 'CVE CVSSv3', 'value': 'CVE.CVSSv3'},
            {'label': 'CVE Description', 'value': 'CVE.description'},
            {'label': 'Exploit URL', 'value': 'Exploit.url'},
            {'label': 'Project Alias', 'value': 'Project.alias'},
            {'label': 'Project Num Sources', 'value': 'Project.source_num'},
            {'label': 'Project Num CVE', 'value': 'Project.cve_num'},
            {'label': 'Project Num Exploits', 'value': 'Project.exploit_num'},
            {'label': 'SrvOS', 'value': 'SrvOS.srv_os'},
            {'label': 'SrvOS Num Sources', 'value': 'SrvOS.source_num'},
            {'label': 'SrvOS Num CVE', 'value': 'SrvOS.cve_num'},
            {'label': 'SrvOS Num Exploits', 'value': 'SrvOS.exploit_num'},
            {'label': 'Version', 'value': 'Version.version'},
            {'label': 'Version Num Sources', 'value': 'Version.source_num'},
            {'label': 'Version Num CVE', 'value': 'Version.cve_num'},
            {'label': 'Version Num Exploits', 'value': 'Version.exploit_num'},
            {'label': 'URL Num CVE', 'value': 'URL.num_cve'},
            {'label': 'URL Num Exploits', 'value': 'URL.num_exploits'},
            {'label': 'CVE Num Exploits', 'value': 'CVE.num_exploits'}
        ]
        if search_value:
            return [option for option in all_options if search_value.lower() in option['label'].lower()]
        return all_options


