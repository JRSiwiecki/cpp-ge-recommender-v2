import requests
import json
from bs4 import BeautifulSoup

LANGUAGE_CLASSES_FILTER = [
    "Chinese",
    "French",
    "Spanish",
    "German",
]
"""
List of most language classes offered at CPP so that we can avoid adding them
to results.
"""


def scrape_cpp_data(catalog_year: int):
    """
    Scrapes CPP Course Catalog based on given catalog year and returns
    the resulting class areas (such as class areas A1, B2, C3).

    Args:
        catalog_year (str): Year to scrape the correct data for that catalog year.

    Returns:
        ResultSet[Any]: ResultSet containing the scraped data separated by class area.
    """

    if not isinstance(catalog_year, int):
        raise TypeError("Invalid input, catalog_year must be an int.")

    VALID_YEARS = [2021, 2022, 2023]
    """
    Valid years for CPP catalogs.
    """

    if catalog_year not in VALID_YEARS:
        raise ValueError(f"{catalog_year} is not a valid catalog year.")

    CATALOG_URLS = {
        2021: "https://catalog.cpp.edu/preview_program.php?catoid=57&poid=14912",
        2022: "https://catalog.cpp.edu/preview_program.php?catoid=61&poid=15936",
        2023: "https://catalog.cpp.edu/preview_program.php?catoid=65&poid=17161",
    }
    """
    Only valid catalog urls, catalogs before 2021 have some varying structure that
    I will not be dealing with!
    """

    url = CATALOG_URLS.get(catalog_year)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    class_areas = soup.find_all("div", class_="acalog-core")
    return class_areas


def categorize_courses(scraped_class_areas) -> list[dict]:
    """
    Categorizes scraped data into area_map and section_map which contains
    an area's sections and a section's courses respectively.

    Args:
        scraped_class_areas (ResultSet[Any]): Scraped data from the CPP catalog that contains
        all areas for a catalog year.

    Returns:
        list[dict]: A list containing first the area_map and second the section_map.
    """
    # top element is current area
    area_stack = []

    # top element is current section
    section_stack = []

    # contains list of dicts containing sections in that area
    area_map = {}

    # contains list of classes in that section
    section_map = {}

    for class_area in scraped_class_areas:
        area = class_area.find("h2")
        section = class_area.find("h3")

        courses = class_area.find_all("li", class_="acalog-course")

        if area:
            # 5th index contains area letter
            area_stack.insert(0, area.text[5])
            current_area = area_stack[0]

            # edge case as these two don't have sections, just the area
            if current_area == "E":
                current_section = "0. Lifelong Learning and Self-Development"
                section_map[current_section] = []
            elif current_area == "F":
                current_section = "0. Ethnic Studies"
                section_map[current_section] = []

            area_map[current_area] = []

        if section:
            if "Note(s)" in section.text:
                break

            if "(" in section.text:
                end_marker = section.text.index("(") - 1
            else:
                end_marker = section.text.index(":")

            # 0th index contains section number
            section_stack.insert(0, section.text[0:end_marker])
            current_section = section_stack[0]

            section_map[current_section] = []
            area_map[current_area].append(section.text[0:end_marker])

        for course in courses:
            spans = course.find_all("span")

            for span in spans:
                if span:
                    end_marker = span.text.index("(")
                    section_map[current_section].append(span.text[0 : end_marker - 1])

    # hard code solution for E and F
    area_map["E"].append("0. Lifelong Learning and Self-Development")
    area_map["F"].append("0. Ethnic Studies")

    return [area_map, section_map]


def get_opencpp_api_data() -> dict:
    """
    Grabs all course data from the OpenCPP API. This API's source code can be found here:
    https://github.com/ZombiMigz/opencpp-api

    Returns:
        dict: Returns a dictionary/JSON object from the OpenCPP API data.
    """
    response = requests.post("https://cpp-scheduler.herokuapp.com/data/courses/find")
    json_object = json.loads(response.text)
    return json_object


def recommend_courses(area_section, area_map, section_map, json_object):
    """
    Recommends courses based on the area_section requested, sorts them by
    highest average GPA to lowest average GPA by students who have taken the course.

    Args:
        area_section (list[str]): List containing the area at index 0 and section at index 1.
        area_map (dict): Dict that maps an area to its corresponding sections.
        section_map (dict): Dict that maps a section to its corresponding courses.
        json_object (dict): Dict that contains the scraped data for its corresponding year.

    Returns:
        list: List containing courses for the given area_section sorted by highest average GPA.
    """
    requested_data = area_section

    if len(requested_data) != 2:
        raise ValueError(
            f"Requested area section: {requested_data} must be 2 characters."
        )

    requested_area = requested_data[0].upper()
    requested_section = requested_data[1]

    VALID_AREA_SECTIONS = [
        "A1",
        "A2",
        "A3",
        "B1",
        "B2",
        "B4",
        "B5",
        "C1",
        "C2",
        "C3",
        "D1",
        "D2",
        "D4",
        "E0",
        "F0",
        "E",
        "F",
    ]
    """
    Valid area sections that exist for CPP classes.
    """

    if requested_area not in VALID_AREA_SECTIONS:
        raise ValueError(f"{requested_area} is an invalid area section.")

    if requested_area.isdigit():
        raise ValueError(f"Area: {requested_area} must be a character.")

    if requested_section.isalpha():
        raise ValueError(f"Section: {requested_section} must be a number.")

    if requested_area not in area_map:
        raise ValueError(f"Area: {requested_area} does not exist.")

    found_sections = area_map[requested_area]

    found_classes = []

    for section in found_sections:
        if requested_section in section:
            found_classes = section_map[section]
            break

    if not found_classes:
        raise ValueError("No sections found for this query.")

    course_codes = []

    for found_class in found_classes:
        end_marker = found_class.index("-") - 1
        course_codes.append(found_class[0:end_marker])

    course_gpas = []

    for object in json_object:
        for course_code in course_codes:
            course_label = object["Label"]

            if course_code in course_label:
                course_title = object["CourseTitle"]

                if course_title is None:
                    course_title = get_course_title(found_class)

                # Remove Honors/Activity courses
                if course_title is not None and (
                    "Honors" in course_title or "Activity" in course_title
                ):
                    continue

                # Remove language courses but only when looking in C2 courses
                if area_section == "C2":
                    if course_title is not None and (
                        any(lang in course_title for lang in LANGUAGE_CLASSES_FILTER)
                    ):
                        continue

                course_component = course_label[-1]

                if course_label is not None and (
                    "M" in course_component
                    or "H" in course_component
                    or "L" in course_component
                    or "A" in course_component
                ):
                    continue

                if object["AvgGPA"] is None:
                    course_gpas.append([course_code, course_title, 0])
                    continue

                course_avg_gpa = object["AvgGPA"]

                course_gpas.append(
                    [
                        course_code,
                        course_title,
                        round(float(course_avg_gpa), 2),
                    ]
                )

    # Sort by highest average GPA
    course_gpas = sorted(course_gpas, key=lambda x: x[2], reverse=True)
    return course_gpas


def get_top_courses(area_map, section_map, json_object) -> dict:
    """
    Returns the top five courses for each area section.

    TODO: Perhaps add another argument to return the top X courses for each area?

    Args:
        area_map (dict): Dict that maps an area to its corresponding sections.
        section_map (dict): Dict that maps a section to its corresponding courses.
        json_object (dict): Dict that contains OpenCPP API data about all courses.

    Returns:
        dict: Returns a dict containing the top courses for each area section.
    """
    top_courses = {}

    for area in area_map.keys():
        sections = area_map[area]

        for section in sections:
            found_classes = section_map[section]

            section_courses = []

            # Skip area section B3
            if area not in area_map or (
                area == "B" and section == "3. Laboratory Activity"
            ):
                continue

            for found_class in found_classes:
                end_marker = found_class.index("-") - 1
                course_code = found_class[0:end_marker]

                for object in json_object:
                    course_label = object["Label"]
                    course_title = object["CourseTitle"]

                    if course_title is None:
                        course_title = get_course_title(found_class)

                    # Remove Honors/Activity Courses
                    if course_code in course_label:
                        if course_title is not None and (
                            "Honors" in course_title or "Activity" in course_title
                        ):
                            continue

                        # Remove language courses but only when looking in C2 courses
                        if (
                            section
                            == "2. Literature, Modern Languages, Philosophy and Civilization"
                        ):
                            if course_title is not None and (
                                any(
                                    lang in course_title
                                    for lang in LANGUAGE_CLASSES_FILTER
                                )
                            ):
                                continue

                        course_component = course_label[-1]

                        if course_label is not None and (
                            "M" in course_component
                            or "H" in course_component
                            or "L" in course_component
                            or "A" in course_component
                        ):
                            continue

                        course_average_gpa = object["AvgGPA"]

                        if course_average_gpa is None:
                            course_average_gpa = 0
                        else:
                            course_average_gpa = round(float(course_average_gpa), 2)

                        course_info = {
                            "CourseCode": course_code,
                            "CourseTitle": course_title,
                            "AvgGPA": course_average_gpa,
                        }

                        section_courses.append(course_info)

            section_courses = sorted(
                section_courses, key=lambda x: x["AvgGPA"], reverse=True
            )
            area_section_title = f"{area}{section}"
            top_courses[area_section_title] = section_courses[:5]

    return top_courses


def get_course_title(full_course_name: str) -> str:
    """
    Used in case the data from OpenCPP API doesn't contain a course title,
    grabs course name from scraped CPP catalog data.

    Args:
        full_course_name (str): The full course name, containing typically course code and name.

    Returns:
        str: The course name with the course code removed.
    """

    if not isinstance(full_course_name, str):
        raise TypeError("Invalid full_course_name type, must be a string.")

    # start 2 characters after the " - " separating class code from title
    start_marker = full_course_name.index("-") + 2

    return full_course_name[start_marker:]


def main():
    catalog_year = 2021
    class_areas = scrape_cpp_data(catalog_year)
    categorize_courses(class_areas)


if __name__ == "__main__":
    main()
