import os
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

    # Valid years for CPP catalogs.
    VALID_YEARS = [2021, 2022, 2023]

    if catalog_year not in VALID_YEARS:
        raise ValueError(f"{catalog_year} is not a valid catalog year.")

    # Only valid catalog urls, catalogs before 2021 have some varying structure that
    # I will not be dealing with!
    CATALOG_URLS = {
        2021: "https://catalog.cpp.edu/preview_program.php?catoid=57&poid=14912",
        2022: "https://catalog.cpp.edu/preview_program.php?catoid=61&poid=15936",
        2023: "https://catalog.cpp.edu/preview_program.php?catoid=65&poid=17161",
    }

    url = CATALOG_URLS.get(catalog_year)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    class_areas = soup.find_all("div", class_="acalog-core")
    return class_areas


def categorize_courses(scraped_class_areas, open_cpp_data, catalog_year: int) -> dict:
    """
    Categorizes scraped data into area_map and section_map which contains
    an area's sections and a section's courses respectively. Maps these to .json
    files by area/section and year.

    Args:
        scraped_class_areas (ResultSet[Any]): Scraped data from the CPP catalog that contains
        all areas for a catalog year.
        open_cpp_data (dict): JSON object containing all course data for CPP.
        catalog_year (int): Requested year to categorize.

    Returns:
        dict[str, Any]: A dict containing class data for the given year, mapped area to its section.
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

    # Create a 'data' folder if it doesn't exist
    data_folder = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(data_folder, exist_ok=True)

    year_data = {
        "year": catalog_year,
        "areas": [],
    }

    for area, sections in area_map.items():
        area_data = {
            "area": area,
            "sections": [],
        }

        for section, courses in section_map.items():
            if section in sections:
                section_data = {
                    "section": section,
                    "courses": [],
                }

                for course in courses:
                    course_data = {
                        "courseCode": course,
                        "averageGPA": None,
                    }

                    # Find the corresponding OpenCPP API data for the course
                    for api_course in open_cpp_data:
                        if (
                            get_course_label(course_data["courseCode"])
                            in api_course["Label"]
                        ):
                            course_data["averageGPA"] = api_course["AvgGPA"]

                    section_data["courses"].append(course_data)

                area_data["sections"].append(section_data)

        year_data["areas"].append(area_data)

    year_file = os.path.join(data_folder, f"course-data-{catalog_year}.json")

    with open(year_file, "w") as data_file:
        json.dump(year_data, data_file, indent=2)

    return year_data


# TODO: Possibly this function will be moved to tRPC/some other server-side function.
def get_opencpp_api_data() -> dict:
    """
    Grabs all course data from the OpenCPP API. This API's source code can be found here:
    https://github.com/ZombiMigz/opencpp-api

    Returns:
        dict: Returns a dictionary/JSON object from the OpenCPP API data.
    """
    response = requests.post("https://api.cppscheduler.com/data/courses/findAll")
    json_object = json.loads(response.text)
    return json_object


# TODO: Possibly this function will be moved to tRPC/some other server-side function.
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

    # Valid area sections that exist for CPP classes.
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


def get_course_label(full_course_name: str) -> str:
    """
    Used to search through OpenCPP API data.

    Args:
        full_course_name (str): The full course name, containing typically course code and name.

    Returns:
        str: The course label with the course name removed.
    """

    if not isinstance(full_course_name, str):
        raise TypeError("Invalid full_course_name type, must be a string.")

    # only want the course label before the " - " separating class code from title
    end_marker = full_course_name.index("-") - 1
    return full_course_name[:end_marker]


def main():
    catalog_years = [2021, 2022, 2023]

    # CURRENTLY THIS IS BROKEN!!!
    # Though data is still current, just doesn't have averageGPAs attached.
    # TODO: WAIT until OpenCPPAPI is back!
    open_cpp_data = get_opencpp_api_data()

    for catalog_year in catalog_years:
        class_areas = scrape_cpp_data(catalog_year)
        categorize_courses(class_areas, open_cpp_data, catalog_year)


if __name__ == "__main__":
    main()
