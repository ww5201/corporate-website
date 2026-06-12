import urllib.request
import re

r = urllib.request.urlopen('http://8.138.218.146/', timeout=10)
html = r.read().decode('utf-8', 'replace')

print(f"Total size: {len(html)} bytes")

# Find script section
script_start = html.find('<script>')
script_end = html.rfind('</script>')
if script_start == -1 or script_end == -1:
    print("ERROR: No script tags found!")
else:
    js = html[script_start+8:script_end]
    print(f"JS section: {len(js)} chars")
    
    # Check for key functions
    critical = ['setLang', 'loadData', 'toggleLang', 'toggleSettings', 'toggleMenu',
                'renderProducts', 'renderPortfolio', 'loadCases', 'openLb', 'closeLb',
                'selectPay', 'submitOrder', 'openOrder', 'closeOrder',
                'handleWechatClick', 'showContact']
    for func in critical:
        pattern = f'function {func}'
        found = pattern in js
        print(f"  {func}: {'OK' if found else 'MISSING'}")
    
    # Check for i18n object
    print(f"\n  i18n object: {'OK' if 'i18n = {' in js else 'MISSING'}")
    print(f"  zh section: {'OK' if 'zh: {' in js else 'MISSING'}")
    print(f"  en section: {'OK' if 'en: {' in js else 'MISSING'}")
    
    # Check for key i18n keys
    for key in ['hero_badge', 'nav_home', 'mobile_home', 'lang_label']:
        found = key in js
        print(f"  i18n key '{key}': {'OK' if found else 'MISSING'}")
    
    # Check startup code
    print(f"\n  loadData() call: {'OK' if 'loadData()' in js else 'MISSING'}")
    print(f"  setLang() call: {'OK' if 'setLang(' in js else 'MISSING'}")
    print(f"  loadCases() call: {'OK' if 'loadCases()' in js else 'MISSING'}")
    
    # Check for HTML elements referenced in JS
    print(f"\n  #langDropdown ref: {'found' if 'langDropdown' in js else 'MISSING'}")
    print(f"  #currentLangLabel ref: {'found' if 'currentLangLabel' in js else 'MISSING'}")
    print(f"  #settingsDropdown ref: {'found' if 'settingsDropdown' in js else 'MISSING'}")
    print(f"  #menu ref: {js.count('getElementById') if 'getElementById' in js else 0} getElementById calls")
    
    # Check for syntax issues - count braces in JS only
    opens = js.count('{')
    closes = js.count('}')
    print(f"\n  Braces: {opens}:{closes} {'BALANCED' if opens == closes else 'UNBALANCED!'}")
    
    # Check for common JS errors
    print(f"\n  'undefined' refs: {js.count('undefined')}")
    print(f"  'null' refs: {js.count('null')}")
    
    # Extract first 500 chars of JS to check for syntax errors
    print(f"\nJS first 300 chars:")
    print(js[:300])
