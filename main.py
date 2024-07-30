from playwright.sync_api import sync_playwright
import csv
from datetime import datetime, timedelta


def initiate_driver():
    # Initialize Playwright and start a Chromium browser instance
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(
        headless=False
    )  # Set headless=True if you don't want a visible browser
    page = browser.new_page()
    return page, playwright, browser


def login(page):
    page.goto("https://www.englandgolf.org/my-golf-login")

    # Click the "Allow all" button
    page.click('//button[text()="Allow all"]')
    page.wait_for_timeout(2000)  # Wait for 2 seconds to ensure page has time to process

    membership = "1015123002"
    pwd = "Shadow!43"

    # Enter membership and password
    page.fill('//input[@type="text"]', membership)
    page.fill('//input[@type="password"]', pwd)
    page.get_by_label("Keep me signed in").check()
    page.press('//input[@type="password"]', "Enter")

    # Wait for the login to process
    page.wait_for_timeout(5000)

def main():
    page, playwright, browser = initiate_driver()
    login(page)

    file_path = "2024_07_18-entries (1).csv"
    output_file = "output.csv"
    header = [
        "Player Name",
        "Played",
        "Course",
        "Marker",
        "Crse Rating",
        "Slope",
        "Adj Gross",
        "PCC",
        "Score Diff",
        "Crse Hdcp",
        "Handicap Index",
    ]
    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)
        # Write the rows of data to the file
        writer.writerow(header)

    with open(file_path, newline="") as f:
        reader = csv.reader(f)
        next(reader)  # Skip the first row (header)
        for row in reader:
            tee_time = datetime.strptime(row[1], "%H:%M") + timedelta(hours=4)
            current_time = datetime.now()
            if current_time.time() >= tee_time.time():
                name = row[3].split(" ")
                search_name = f"{name[0]} {name[-1]}"
                page.wait_for_timeout(5000)
                search_element = page.locator('//input[@id="searchMemberName"]')
                search_element.fill(search_name)
                try:
                    page.locator(
                        f'//a[contains(text(), "{name[0]}") and contains(text(), "{name[-1]}")]'
                    ).click()
                except:
                    page.goto("https://www.englandgolf.org/my-overview")
                    continue
                page.wait_for_timeout(5000)
                played = page.locator(
                    f'(//div[contains(@class, "col-played")])[2]'
                ).inner_text()
                played_date = datetime.strptime(played, "%d/%m/%Y").date()
                today_date = current_time.date()
                if played_date == today_date:
                    data = page.locator(
                        f'(//div[@class="_l-left-col"])[2]'
                    ).text_content()
                    updated_data = [row[3]] + [
                        line.strip() for line in data.split("\n") if line.strip()
                    ]
                    with open(output_file, newline="") as file:
                        reader = csv.reader(file)
                        rows = list(reader)

                    index = None
                    for i, existing_row in enumerate(rows):
                        if existing_row[0] == updated_data[0]:
                            index = i
                            break

                    with open(output_file, "w", newline="") as file:
                        writer = csv.writer(file)
                        if index is not None:
                            # Replace the row
                            rows[index] = updated_data
                        else:
                            # Append new row
                            rows.append(updated_data)
                        writer.writerows(rows)

                page.goto("https://www.englandgolf.org/my-overview")

    page.context.close()  # Close the context, which also closes the page
    browser.close()  # Close the browser instance
    playwright.stop()  # Stop Playwright


if __name__ == "__main__":
    main()
