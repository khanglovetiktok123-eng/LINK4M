async def bypass_link(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-blink-features=AutomationControlled'])
        context = await browser.new_context(
            viewport={"width": 1366, "height": 768},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        await interaction.followup.send("🌐 Đang truy cập link 4m...")

        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        await asyncio.sleep(6)

        # Click nút "Tiếp tục" hoặc "Get Link"
        try:
            await page.get_by_role("button").filter(has_text=re.compile("Tiếp tục|Continue|Get Link|Lấy mã|Lấy link", re.I)).first.click(timeout=10000)
            await asyncio.sleep(5)
        except:
            pass

        # Tìm link nhiệm vụ (xem web)
        content = await page.content()
        task_url_match = re.search(r'href=["\'](.*?(?:view|task|mission|nhiệm|web|earn)[^"\']*)["\']', content, re.I)
        if task_url_match:
            task_link = task_url_match.group(1)
            if not task_link.startswith('http'):
                task_link = "https://link4m.net" + task_link
            await interaction.followup.send(f"📌 **Link nhiệm vụ (xem web):** \n`{task_link}`\n⏳ Mở link này và xem web theo yêu cầu (thường 10-30 giây).")

        await asyncio.sleep(10)  # Đợi timer nhiệm vụ

        # Click lấy mã lần cuối
        try:
            await page.get_by_role("button").filter(has_text=re.compile("Get|Tiếp|Lấy|Submit", re.I)).first.click(timeout=8000)
            await asyncio.sleep(8)
        except:
            pass

        content = await page.content()
        final_url = page.url

        # Tìm mã
        code_match = re.search(r'(?:Mã|Code|Key)[:\s]*([A-Za-z0-9]{6,25})', content, re.I)
        if code_match:
            code = code_match.group(1)
            await browser.close()
            return f"✅ **Thành công!**\n🔑 **Mã:** `{code}`"

        await browser.close()
        return f"🔗 Đã xử lý: {final_url}\n💡 Thử lại sau khi hoàn thành nhiệm vụ xem web."
