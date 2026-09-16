from playwright.sync_api import sync_playwright

PAGES = ['index.html', 'photography.html', 'googlepartnership.html', 'socials.html']

def test_all_links_resolve_and_no_js_errors():
    with sync_playwright() as p:
        browser = p.chromium.launch()

        for page_name in PAGES:
            page = browser.new_page(viewport={'width': 1280, 'height': 800})
            page_errors = []
            page.on('pageerror', lambda err: page_errors.append(err))

            url = f'http://localhost:3000/{page_name}'
            page.goto(url, wait_until='networkidle')

            assert len(page_errors) == 0, f"JS errors on {page_name}: {page_errors}"

            # Check footer legal links
            for modal_name in ['Privacy', 'Terms', 'Cookie']:
                page.evaluate(f'window.open{modal_name}()')
                modal_id = f'{modal_name.lower()}-modal'
                assert page.is_visible(f'#{modal_id}'), f"Modal {modal_name} on {page_name} was not visible!"
                page.evaluate(f'window.close{modal_name}()')
                assert not page.is_visible(f'#{modal_id}'), f"Modal {modal_name} on {page_name} remained visible after close!"

            page.close()

        browser.close()

def test_mobile_menu_drawer_and_link_clicks():
    with sync_playwright() as p:
        browser = p.chromium.launch()

        for page_name in PAGES:
            page = browser.new_page(viewport={'width': 375, 'height': 812})
            url = f'http://localhost:3000/{page_name}'
            page.goto(url, wait_until='networkidle')

            # Mobile menu should be hidden initially
            assert not page.is_visible('#mobile-menu')

            # Click mobile toggle
            page.click('button[aria-label="Toggle mobile menu"]')
            assert page.is_visible('#mobile-menu')

            # Find all links in mobile menu
            mobile_links = page.locator('#mobile-menu a').all()
            assert len(mobile_links) > 0, f"No mobile links found on {page_name}"

            # Verify clicking a mobile link closes the menu
            first_link = mobile_links[0]
            first_link.click()

            # Mobile menu should close
            assert not page.is_visible('#mobile-menu'), f"Mobile menu on {page_name} did not close after link click"

            page.close()

        browser.close()

if __name__ == '__main__':
    test_all_links_resolve_and_no_js_errors()
    test_mobile_menu_drawer_and_link_clicks()
    print("All Playwright navigation tests passed successfully!")
