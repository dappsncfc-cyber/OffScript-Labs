from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('http://localhost:3000', wait_until='commit')

        # Click Free Audit to scroll down
        page.click('a[href="#audit"]')

        # Fill in business name with XSS payload
        page.fill('#audit-business', '<img src=x onerror=alert(1)>')

        # Select business type
        page.select_option('#audit-type', 'hospitality')

        # Wait for the result area to be populated
        page.click('#gemini-preview-btn')
        page.wait_for_selector('.terminal-log')
        page.wait_for_timeout(3500) # Wait for typing effect to finish

        # Ensure the payload was escaped by checking text content vs html content
        result_html = page.inner_html('#audit-ai-result')
        if '<img src=x onerror=alert(1)>' in result_html:
            print("XSS VULNERABILITY STILL PRESENT")
        elif '&lt;img src=x onerror=alert(1)&gt;' in result_html:
            print("XSS VULNERABILITY FIXED (Escaped)")
        else:
            print("Payload not found in result:", result_html)

        browser.close()

run()
